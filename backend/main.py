"""
Orion — FastAPI Backend
Seamless, secure, production-ready API for the multi-agent document platform.

Run:  uvicorn main:app --reload --port 8000
"""

import os
import json
import time
import uuid
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

# ── Load .env with explicit path so uvicorn --reload subprocesses find it ──
_env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=_env_path, override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY",   "")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

# Validate keys — placeholder strings count as missing
def _is_real_key(val: str, prefix: str = "") -> bool:
    return bool(val) and not val.startswith("your") and (not prefix or val.startswith(prefix))

GROQ_LIVE    = _is_real_key(GROQ_API_KEY,   "gsk_")
OPENAI_LIVE  = _is_real_key(OPENAI_API_KEY, "sk-")
SERPER_LIVE  = _is_real_key(SERPER_API_KEY)
MAX_REQUESTS_PER_MINUTE = int(os.getenv("RATE_LIMIT_RPM", "10"))

GROQ_SYSTEM_PROMPT = """You are Orion, an expert AI document generator.
When given a user request, produce a comprehensive, well-structured markdown document.
Use headers (##, ###), bullet points, bold text (**bold**), and tables where useful.
Be detailed, specific, and actionable. Write at least 500 words."""

# ── Logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("orion")

# ── FastAPI app ───────────────────────────────────────────
app = FastAPI(
    title="Orion API",
    description="Multi-agent document generation platform",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI at /docs
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ── In-memory rate limiter (swap for Redis in production) ─
_rate_store: dict[str, list[float]] = {}

def check_rate_limit(client_ip: str) -> bool:
    """Returns True if request is allowed, False if rate-limited."""
    now = time.time()
    window = 60.0
    hits = _rate_store.get(client_ip, [])
    hits = [t for t in hits if now - t < window]
    if len(hits) >= MAX_REQUESTS_PER_MINUTE:
        return False
    hits.append(now)
    _rate_store[client_ip] = hits
    return True

# ── In-memory history store ───────────────────────────────
_history: list[dict] = []

# ── Pydantic models ───────────────────────────────────────
class GenerateRequest(BaseModel):
    input: str = Field(..., min_length=3, max_length=1000, description="User's plain-language request")

    @field_validator("input")
    @classmethod
    def sanitize_input(cls, v):
        # Strip whitespace
        v = v.strip()
        # Basic injection prevention
        forbidden = ["<script", "javascript:", "data:text"]
        for f in forbidden:
            if f.lower() in v.lower():
                raise ValueError("Invalid input content")
        return v

class GenerateResponse(BaseModel):
    request_id:    str
    doc_type:      str
    refined_topic: str
    audience:      str
    agents_used:   list[str]
    reasoning:     str
    result:        str
    duration_ms:   int
    demo_mode:     bool

class HealthResponse(BaseModel):
    status:       str
    version:      str
    backend_live: bool
    agents_ready: bool
    timestamp:    str

# ── Startup log ───────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    log.info("=" * 50)
    log.info(f"Orion API starting up")
    log.info(f".env path: {_env_path}  (exists: {_env_path.exists()})")
    log.info(f"GROQ_API_KEY detected: {GROQ_LIVE}  (key starts: {GROQ_API_KEY[:8] + '...' if GROQ_API_KEY else 'EMPTY'})")
    log.info(f"OPENAI_API_KEY detected: {OPENAI_LIVE}")
    log.info(f"Mode: {'GROQ LIVE' if GROQ_LIVE else 'OPENAI+SERPER' if (OPENAI_LIVE and SERPER_LIVE) else 'DEMO'}")
    log.info("=" * 50)

# ── Middleware: request ID + timing ──────────────────────
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()
    response = await call_next(request)
    duration = int((time.perf_counter() - start) * 1000)
    response.headers["X-Request-ID"]    = request_id
    response.headers["X-Response-Time"] = f"{duration}ms"
    response.headers["X-Powered-By"]    = "Orion/1.0"
    return response

# ── Exception handlers ────────────────────────────────────
@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(status_code=404, content={"detail": "Endpoint not found"})

@app.exception_handler(500)
async def server_error(request: Request, exc):
    log.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# ── Streaming generate endpoint (Groq SSE) ────────────────
# Frontend calls this first; falls back to /generate if unavailable.
# Requires GROQ_API_KEY in .env — free at console.groq.com
@app.post("/generate/stream", tags=["Documents"])
async def generate_stream(req: GenerateRequest, request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {MAX_REQUESTS_PER_MINUTE} requests/minute.",
        )

    # ── No real Groq key: stream a friendly demo message ───
    if not GROQ_LIVE:
        async def demo_stream():
            msg = (
                f"# Demo Mode — No API Key\n\n"
                f"**Your request:** {req.input}\n\n"
                f"---\n\n"
                f"Add your **GROQ_API_KEY** to `backend/.env` (free at console.groq.com) "
                f"to get real AI-generated documents streamed live.\n\n"
                f"```\nGROQ_API_KEY=gsk_your_key_here\n```\n\n"
                f"Then restart the backend:\n\n"
                f"```bash\nuvicorn main:app --reload --port 8000\n```"
            )
            for char in msg:
                yield f"data: {json.dumps({'token': char})}\n\n"
                await asyncio.sleep(0.006)
            yield "data: [DONE]\n\n"

        return StreamingResponse(demo_stream(), media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    # ── Groq streaming ─────────────────────────────────────
    from groq import AsyncGroq

    async def groq_stream():
        client = AsyncGroq(api_key=GROQ_API_KEY)
        try:
            stream = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": GROQ_SYSTEM_PROMPT},
                    {"role": "user",   "content": req.input},
                ],
                max_tokens=4096,
                stream=True,
            )
            async for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield f"data: {json.dumps({'token': delta})}\n\n"
        except Exception as e:
            log.error(f"Groq stream error: {e}")
            err_msg = "\n\n**Error:** " + str(e)
            yield "data: " + json.dumps({"token": err_msg}) + "\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(groq_stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── Health check ──────────────────────────────────────────
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    return HealthResponse(
        status="ok",
        version="1.0.0",
        backend_live=True,
        agents_ready=GROQ_LIVE or (OPENAI_LIVE and SERPER_LIVE),
        timestamp=datetime.utcnow().isoformat() + "Z",
    )

# ── History endpoint ──────────────────────────────────────
@app.get("/history", tags=["Documents"])
async def get_history(limit: int = 10):
    return _history[:limit]

# ── Main generate endpoint ────────────────────────────────
@app.post("/generate", response_model=GenerateResponse, tags=["Documents"])
async def generate(req: GenerateRequest, request: Request):
    # Rate limiting
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {MAX_REQUESTS_PER_MINUTE} requests/minute.",
            headers={"Retry-After": "60"},
        )

    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.perf_counter()

    # Priority: Groq → CrewAI (OpenAI+Serper) → demo
    if GROQ_LIVE:
        mode = "groq"
    elif OPENAI_LIVE and SERPER_LIVE:
        mode = "crewai"
    else:
        mode = "demo"

    log.info(f"[{request_id}] Generate | ip={client_ip} | mode={mode} | input={req.input[:80]!r}")

    try:
        if mode == "groq":
            result = await _run_groq(req.input)
        elif mode == "crewai":
            result = await _run_crewai(req.input, request_id)
        else:
            result = _demo_response(req.input)

        duration_ms = int((time.perf_counter() - start_time) * 1000)
        log.info(f"[{request_id}] Done | {duration_ms}ms | type={result['doc_type']}")

        # Save to history
        _history.insert(0, {
            "id":         request_id,
            "input":      req.input,
            "doc_type":   result["doc_type"],
            "label":      result.get("label", result["doc_type"]),
            "created_at": datetime.utcnow().isoformat() + "Z",
        })
        if len(_history) > 50:
            _history.pop()

        return GenerateResponse(
            request_id=request_id,
            doc_type=result["doc_type"],
            refined_topic=result["refined_topic"],
            audience=result["audience"],
            agents_used=result["agents_used"],
            reasoning=result["reasoning"],
            result=result["result"],
            duration_ms=duration_ms,
            demo_mode=(mode == "demo"),
        )

    except HTTPException:
        raise
    except Exception as e:
        log.error(f"[{request_id}] Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ── Groq runner (non-streaming, for /generate fallback) ───
async def _run_groq(user_input: str) -> dict:
    """Calls Groq API and returns a full response dict (no streaming)."""
    from groq import AsyncGroq
    client = AsyncGroq(api_key=GROQ_API_KEY)
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": GROQ_SYSTEM_PROMPT},
            {"role": "user",   "content": user_input},
        ],
        max_tokens=4096,
    )
    result_text = response.choices[0].message.content
    return {
        "doc_type":      "auto",
        "refined_topic": user_input,
        "audience":      "Everyone",
        "agents_used":   ["Research Agent", "Strategist", "Writer"],
        "reasoning":     "Generated by Groq Llama-3.3-70b",
        "result":        result_text,
    }


# ── CrewAI runner (async wrapper) ─────────────────────────
async def _run_crewai(user_input: str, request_id: str) -> dict:
    """
    Runs the full CrewAI multi-agent pipeline in a thread pool
    so it doesn't block FastAPI's event loop.
    """
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=4) as pool:
        result = await loop.run_in_executor(pool, _crewai_sync, user_input)
    return result


def _crewai_sync(user_input: str) -> dict:
    """Synchronous CrewAI execution — called from thread pool."""
    # Import here so startup is fast even without crewai installed
    from crewai import Agent, Task, Crew, Process
    from crewai_tools import SerperDevTool, WebsiteSearchTool
    from langchain_openai import ChatOpenAI

    os.environ["OPENAI_API_KEY"]  = OPENAI_API_KEY
    os.environ["SERPER_API_KEY"]  = SERPER_API_KEY

    llm         = ChatOpenAI(model="gpt-4o", temperature=0.3)
    llm_fast    = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    search_tool = SerperDevTool()
    web_tool    = WebsiteSearchTool()

    # ── Router agent ───────────────────────────────────────
    router = Agent(
        role="Intent Classification Specialist",
        goal="Classify the user's request into the correct document type. Output ONLY valid JSON.",
        backstory="Expert AI router. Instantly identifies what document type any user wants. Never hallucinates.",
        tools=[],
        llm=llm_fast,
        verbose=False,
        allow_delegation=False,
    )

    SUPPORTED_TYPES = """
    business_plan, pitch_deck, deep_market_research, competitor_analysis,
    product_launch_plan, financial_projections, youtube_strategy, blog_newsletter,
    social_media_calendar, study_plan, career_planning, research_paper,
    client_deliverables, campaign_strategy, proposal_pricing, life_goals,
    travel_planning, cooking_meal_plan, brainstorm, casual_chat
    """

    routing_task = Task(
        description=f"""
        User input: "{user_input}"
        Classify into one type from: {SUPPORTED_TYPES}
        Output ONLY this JSON (no markdown fences):
        {{"doc_type":"<type>","refined_topic":"<clean 1-2 sentence version>","audience":"<who this is for>","complexity":"simple|standard|deep","reasoning":"<1 sentence why>"}}
        """,
        expected_output="Valid JSON object with doc_type, refined_topic, audience, complexity, reasoning",
        agent=router,
    )

    routing_crew = Crew(agents=[router], tasks=[routing_task], process=Process.sequential, verbose=False)
    raw_routing  = str(routing_crew.kickoff()).strip()

    # Parse routing result
    try:
        clean = raw_routing.replace("```json", "").replace("```", "").strip()
        routing = json.loads(clean)
    except Exception:
        routing = {"doc_type": "casual_chat", "refined_topic": user_input,
                   "audience": "Everyone", "complexity": "simple", "reasoning": "Fallback"}

    doc_type = routing.get("doc_type", "casual_chat")
    topic    = routing.get("refined_topic", user_input)
    audience = routing.get("audience", "Everyone")

    # ── Build and run the doc-specific crew ───────────────
    from smart_agent_backend import build_crew, AGENT_MAP
    # Re-create agents with fresh LLM instances
    agents_list, tasks_list = build_crew(doc_type, topic, audience)

    doc_crew = Crew(
        agents=agents_list,
        tasks=tasks_list,
        process=Process.sequential,
        verbose=1,
        memory=True,
    )

    result_text = str(doc_crew.kickoff())

    return {
        "doc_type":      doc_type,
        "refined_topic": topic,
        "audience":      audience,
        "agents_used":   [a.role for a in agents_list],
        "reasoning":     routing.get("reasoning", ""),
        "result":        result_text,
    }


# ── Demo mode response (no API keys) ─────────────────────
def _demo_response(user_input: str) -> dict:
    """Returns a structured demo response without any API calls."""
    lower = user_input.lower()

    # Simple keyword routing
    if any(k in lower for k in ["pitch", "investor", "funding", "seed"]):
        doc_type, label = "pitch_deck", "Pitch Deck"
        agents = ["Research Agent", "Strategist", "Writer"]
    elif any(k in lower for k in ["business plan", "start a", "startup idea"]):
        doc_type, label = "business_plan", "Business Plan"
        agents = ["Research Agent", "Fact Checker", "Strategist", "Financial Analyst", "Writer"]
    elif any(k in lower for k in ["social media", "instagram", "posting", "calendar"]):
        doc_type, label = "social_media_calendar", "Social Media Calendar"
        agents = ["Research Agent", "Creative Strategist", "Writer"]
    elif any(k in lower for k in ["travel", "trip", "itinerary", "vacation"]):
        doc_type, label = "travel_planning", "Travel Itinerary"
        agents = ["Research Agent", "Writer"]
    elif any(k in lower for k in ["study", "exam", "learn", "upsc", "gate"]):
        doc_type, label = "study_plan", "Study Plan"
        agents = ["Research Agent", "Personal Coach", "Writer"]
    elif any(k in lower for k in ["market research", "market size", "industry"]):
        doc_type, label = "deep_market_research", "Market Research"
        agents = ["Research Agent", "Fact Checker", "Writer"]
    elif any(k in lower for k in ["competitor", "competitive", "rivals"]):
        doc_type, label = "competitor_analysis", "Competitor Analysis"
        agents = ["Research Agent", "Fact Checker", "Writer"]
    elif any(k in lower for k in ["financial", "projection", "revenue", "p&l"]):
        doc_type, label = "financial_projections", "Financial Projections"
        agents = ["Research Agent", "Financial Analyst", "Writer"]
    else:
        doc_type, label = "casual_chat", "Quick Answer"
        agents = ["Writer"]

    result = f"""# {label}

**Your request:** {user_input}

---

## ⚠️ Demo Mode — API Keys Not Configured

This is a demo response. To generate real AI-powered documents:

**Step 1:** Add your API keys to `backend/.env`:
```
OPENAI_API_KEY=sk-...
SERPER_API_KEY=your-key
```

**Step 2:** Restart the backend:
```bash
uvicorn main:app --reload --port 8000
```

---

## What the agents would generate

The **{label}** pipeline ({' → '.join(agents)}) would produce a fully researched, structured document based on your request.

**Agent responsibilities:**
{chr(10).join(f'- **{a}**: Handles its specialized domain for this document type' for a in agents)}

---

Get your free API keys:
- **OpenAI:** platform.openai.com
- **Serper (web search):** serper.dev — 2,500 free searches/month
"""

    return {
        "doc_type":      doc_type,
        "refined_topic": user_input,
        "audience":      "Everyone",
        "agents_used":   agents,
        "reasoning":     f"Matched to {label} based on keywords in input",
        "result":        result,
    }


# ── Run directly ──────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
