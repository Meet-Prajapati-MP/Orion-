# Orion — Multi-Agent AI Document Platform

One input box. Any document. Powered by CrewAI agents.

---

## Project Structure

```
orion/
├── frontend/          ← React + Vite + Tailwind
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── InputBox.jsx
│   │   │   ├── AgentPipeline.jsx
│   │   │   ├── OutputCard.jsx
│   │   │   ├── CapabilityGrid.jsx
│   │   │   └── HistoryStrip.jsx
│   │   ├── hooks/
│   │   │   └── useGenerate.js
│   │   ├── App.jsx
│   │   ├── api.js
│   │   ├── data.js
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── backend/           ← FastAPI + CrewAI
│   ├── main.py
│   ├── requirements.txt
│   └── .env.example
│
└── README.md
```

---

## Quick Start

### Step 1 — Get API Keys (both free tiers available)

| Key | Where to get | Free tier |
|-----|-------------|-----------|
| `OPENAI_API_KEY` | platform.openai.com | Pay-per-use (~$0.01–0.10 per doc) |
| `SERPER_API_KEY` | serper.dev | 2,500 searches/month free |

---

### Step 2 — Backend Setup

```bash
cd orion/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Open .env and add your OPENAI_API_KEY and SERPER_API_KEY

# Run the server
uvicorn main:app --reload --port 8000
```

Backend starts at: http://localhost:8000
API docs (Swagger): http://localhost:8000/docs

---

### Step 3 — Frontend Setup

Open a new terminal:

```bash
cd orion/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend starts at: http://localhost:3000

---

### Step 4 — Open the app

Go to **http://localhost:3000** and type anything. The agent pipeline fires automatically.

---

## How It Works

```
User types: "I want to start a meal delivery startup targeting working moms"
         ↓
Router Agent (LLM) classifies intent → doc_type: "business_plan"
         ↓
build_crew("business_plan", topic, audience) assembles agents:
  Research Agent → Fact Checker → Strategist → Financial Analyst → Writer
         ↓
Each agent runs its task, passing output to the next
         ↓
Full Business Plan document returned to the UI
```

---

## Demo Mode (no API keys)

The app works without API keys in demo mode:
- The UI shows the full routing + agent animation
- A structured demo response is returned
- Real documents generate once you add API keys

---

## Production Deployment

### Frontend (Vercel / Netlify)
```bash
cd frontend
npm run build         # builds to frontend/dist/
# Deploy the dist/ folder
```

Update `vite.config.js` proxy target to your production backend URL.

### Backend (Railway / Render / EC2)
```bash
# Install
pip install -r requirements.txt

# Run (production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

Set environment variables in your hosting dashboard:
- `OPENAI_API_KEY`
- `SERPER_API_KEY`
- `ALLOWED_ORIGINS=https://your-frontend-domain.com`

---

## Rate Limiting

Default: 10 requests per IP per minute. Configurable via `RATE_LIMIT_RPM` in `.env`.

For production, swap the in-memory store for Redis:
```python
# In main.py, replace _rate_store with redis-py client
import redis
r = redis.Redis(host='localhost', port=6379)
```

---

## Supported Document Types (18 total)

| Type | Agents |
|------|--------|
| Business Plan | Research → Verify → Strategy → Finance → Write |
| Pitch Deck | Research → Strategy → Write |
| Market Research | Research → Verify → Write |
| Competitor Analysis | Research → Verify → Write |
| Product Launch Plan | Research → Strategy → Write |
| Financial Projections | Research → Finance → Write |
| YouTube Strategy | Research → Creative → Write |
| Blog & Newsletter | Research → Creative → Write |
| Social Media Calendar | Research → Creative → Write |
| Study Plan | Research → Coach → Write |
| Career Planning | Research → Coach → Write |
| Research Paper | Research → Verify → Write |
| Campaign Strategy | Research → Strategy → Write |
| Proposal & Pricing | Research → Write |
| Life Goals | Coach → Write |
| Travel Planning | Research → Write |
| Meal Plan | Coach → Write |
| Brainstorm | Research → Strategy → Write |
