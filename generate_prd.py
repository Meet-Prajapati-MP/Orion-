from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import Flowable
from datetime import datetime

# ── Colours ────────────────────────────────────────────────────────────────
GOLD       = colors.HexColor('#E8C547')
NAVY       = colors.HexColor('#0D1B2A')
DARK_GREY  = colors.HexColor('#1C2B3A')
MID_GREY   = colors.HexColor('#4A5568')
LIGHT_GREY = colors.HexColor('#F7F8FA')
WHITE      = colors.white
ACCENT     = colors.HexColor('#6366F1')
SUCCESS    = colors.HexColor('#22C55E')
ERROR_RED  = colors.HexColor('#EF4444')
TABLE_HEAD = colors.HexColor('#0D1B2A')
TABLE_ALT  = colors.HexColor('#F0F4F8')
BORDER_CLR = colors.HexColor('#E2E8F0')

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

# ── Document ────────────────────────────────────────────────────────────────
OUTPUT_PATH = r"M:\Learning FrontEnd\orion\Orion_AI_PRD.pdf"

doc = SimpleDocTemplate(
    OUTPUT_PATH,
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=MARGIN,
    title="Orion AI — Product Requirements Document",
    author="Orion AI Team",
)

# ── Styles ──────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S('CoverTitle', fontSize=42, textColor=GOLD,
                fontName='Helvetica-Bold', alignment=TA_CENTER, leading=50)
cover_sub   = S('CoverSub', fontSize=16, textColor=WHITE,
                fontName='Helvetica', alignment=TA_CENTER, leading=22)
cover_meta  = S('CoverMeta', fontSize=11, textColor=colors.HexColor('#9CA3AF'),
                fontName='Helvetica', alignment=TA_CENTER, leading=18)

h1 = S('H1', fontSize=18, textColor=GOLD, fontName='Helvetica-Bold',
        leading=24, spaceBefore=14, spaceAfter=6)
h2 = S('H2', fontSize=13, textColor=NAVY, fontName='Helvetica-Bold',
        leading=18, spaceBefore=10, spaceAfter=4)
h3 = S('H3', fontSize=11, textColor=DARK_GREY, fontName='Helvetica-Bold',
        leading=16, spaceBefore=8, spaceAfter=3)

body = S('Body', fontSize=9.5, textColor=colors.HexColor('#2D3748'),
         fontName='Helvetica', leading=15, spaceAfter=4)
body_bold = S('BodyBold', fontSize=9.5, textColor=NAVY,
              fontName='Helvetica-Bold', leading=15, spaceAfter=4)
bullet = S('Bullet', fontSize=9.5, textColor=colors.HexColor('#2D3748'),
           fontName='Helvetica', leading=15, leftIndent=14,
           bulletIndent=4, spaceAfter=3)
note = S('Note', fontSize=8.5, textColor=MID_GREY,
         fontName='Helvetica-Oblique', leading=13, spaceAfter=4)
code_style = S('Code', fontSize=8.5, textColor=colors.HexColor('#1A202C'),
               fontName='Courier', leading=13, backColor=LIGHT_GREY,
               leftIndent=10, rightIndent=10, spaceAfter=6,
               borderPadding=(4, 6, 4, 6))
tag_style = S('Tag', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold',
              alignment=TA_CENTER)

# ── Helper: coloured rule ───────────────────────────────────────────────────
def rule(color=GOLD, thickness=1.2, width=1.0):
    return HRFlowable(width=f"{int(width*100)}%", thickness=thickness,
                      color=color, spaceAfter=6, spaceBefore=2)

def section_title(text):
    return [rule(GOLD, 1.5), Paragraph(text, h1), Spacer(1, 2)]

def sub_title(text):
    return [Paragraph(text, h2)]

def body_p(text):
    return Paragraph(text, body)

def bullet_p(text):
    return Paragraph(f"• {text}", bullet)

def sp(n=6):
    return Spacer(1, n)

# ── Table helper ────────────────────────────────────────────────────────────
def make_table(headers, rows, col_widths=None):
    data = [[Paragraph(f"<b>{h}</b>", S('TH', fontSize=9, textColor=WHITE,
             fontName='Helvetica-Bold', leading=13)) for h in headers]]
    for i, row in enumerate(rows):
        data.append([Paragraph(str(c), S(f'TD{i}', fontSize=8.5,
                     textColor=colors.HexColor('#2D3748'),
                     fontName='Helvetica', leading=13)) for c in row])

    avail = PAGE_W - 2 * MARGIN
    if col_widths is None:
        col_widths = [avail / len(headers)] * len(headers)
    else:
        col_widths = [w * mm for w in col_widths]

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ('BACKGROUND',  (0, 0), (-1, 0),  TABLE_HEAD),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, TABLE_ALT]),
        ('GRID',        (0, 0), (-1, -1),  0.4, BORDER_CLR),
        ('VALIGN',      (0, 0), (-1, -1),  'TOP'),
        ('TOPPADDING',  (0, 0), (-1, -1),  5),
        ('BOTTOMPADDING',(0,0), (-1, -1),  5),
        ('LEFTPADDING', (0, 0), (-1, -1),  6),
        ('RIGHTPADDING',(0, 0), (-1, -1),  6),
        ('LINEABOVE',   (0, 1), (-1, 1),   1, GOLD),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t

# ── Cover page ──────────────────────────────────────────────────────────────
class ColorRect(Flowable):
    def __init__(self, w, h, color):
        self.w, self.h, self.color = w, h, color
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.w, self.h, fill=1, stroke=0)

story = []

# Cover background block (simulated via table)
cover_data = [['']]
cover_table = Table(cover_data,
                    colWidths=[PAGE_W - 2*MARGIN],
                    rowHeights=[240])
cover_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), NAVY),
    ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ('TOPPADDING',  (0,0), (-1,-1), 50),
    ('BOTTOMPADDING',(0,0),(-1,-1), 50),
]))
story.append(cover_table)
story.append(sp(20))

story.append(Paragraph("ORION AI", cover_title))
story.append(sp(8))
story.append(Paragraph("Product Requirements Document", cover_sub))
story.append(sp(6))
story.append(rule(GOLD, 1.5, 0.3))
story.append(sp(6))
story.append(Paragraph(
    f"Version 1.0  ·  {datetime.now().strftime('%B %d, %Y')}  ·  Confidential",
    cover_meta))
story.append(sp(12))

meta_rows = [
    ["Product", "Orion AI — Multi-LLM Agent Platform"],
    ["Type", "Responsive Web App (All Devices)"],
    ["LLMs", "Groq (Llama 3.3 70B)  +  OpenAI GPT-4o  +  Claude Sonnet 4.6"],
    ["Status", "Pre-Development  |  MVP Planning"],
    ["Prepared by", "Orion AI Product Team"],
]
meta_table = Table(
    [[Paragraph(f"<b>{r[0]}</b>", S('ML', fontSize=9, fontName='Helvetica-Bold',
       textColor=NAVY)), Paragraph(r[1], body)] for r in meta_rows],
    colWidths=[45*mm, PAGE_W - 2*MARGIN - 45*mm]
)
meta_table.setStyle(TableStyle([
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT_GREY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, BORDER_CLR),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('LINEABOVE', (0,0), (-1,0), 2, GOLD),
    ('LINEBELOW', (0,-1), (-1,-1), 2, GOLD),
]))
story.append(meta_table)
story.append(PageBreak())

# ── Section 1 — Project Overview ────────────────────────────────────────────
story += section_title("01  Project Overview")
story.append(body_p(
    "Orion AI is a multi-LLM intelligent document engine. Users describe any task in plain language "
    "and Orion routes it to the right AI pipeline — instantly producing structured, editable, "
    "exportable documents. Simple questions get instant answers from a single fast model. "
    "Complex tasks run through a 3-stage agent pipeline using Groq, OpenAI GPT-4o, "
    "and Claude Sonnet 4.6 working in sequence."
))
story.append(sp(6))
story.append(make_table(
    ["Field", "Details"],
    [
        ["Core Problem", "Users waste 2–3 hours on documents AI can produce in under 2 minutes"],
        ["Solution", "Smart-routed multi-LLM agent platform with streaming, editing, and export"],
        ["LLMs", "Groq (Llama 3.3 70B) · OpenAI GPT-4o · Claude Sonnet 4.6"],
        ["Platforms", "All devices — Desktop, Tablet, Mobile (responsive web)"],
        ["Auth", "Clerk — Email + Google OAuth"],
        ["Competitive Edge", "3 LLMs in pipeline vs ChatGPT alone — measurably faster and more thorough"],
    ],
    col_widths=[45, 125]
))
story.append(sp(8))

# ── Section 2 — Product Vision ───────────────────────────────────────────────
story += section_title("02  Product Vision")
# Vision statement callout box
vision_table = Table(
    [[Paragraph(
        '"The AI workspace that thinks before it writes — routing your request '
        'to the right agent, in the right mode, in seconds."',
        S('VQ', fontSize=11, fontName='Helvetica-BoldOblique',
          textColor=NAVY, leading=18, alignment=TA_CENTER)
    )]],
    colWidths=[PAGE_W - 2*MARGIN]
)
vision_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFBEA')),
    ('LINEABOVE', (0,0), (-1,0), 3, GOLD),
    ('LINEBELOW', (0,0), (-1,-1), 3, GOLD),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('LEFTPADDING', (0,0), (-1,-1), 20),
    ('RIGHTPADDING', (0,0), (-1,-1), 20),
]))
story.append(vision_table)
story.append(sp(8))
story.append(body_p(
    "Orion AI is <b>not</b> a chatbot. It is an intelligent document engine. You describe what "
    "you need, the smart router decides if it is a simple question or a complex task, assigns "
    "the right agent(s), and produces a professional, editable document you can export instantly. "
    "No prompting skills required — just describe your goal in plain language."
))
story.append(sp(8))

# ── Section 3 — Target Users ─────────────────────────────────────────────────
story += section_title("03  Target Users")
story.append(make_table(
    ["User Type", "Who They Are", "Core Pain Point"],
    [
        ["Professional", "Founders, Marketers, Freelancers, Consultants",
         "Spends 3 hours writing a business plan AI could produce in 2 minutes"],
        ["Student", "University students, researchers, exam preppers",
         "Struggles to structure long-form academic or project documents"],
        ["Casual", "Anyone with a quick question or simple task",
         "ChatGPT gives walls of text; wants clean structured output instantly"],
    ],
    col_widths=[35, 65, 70]
))
story.append(sp(6))
story.append(body_p(
    "<b>Universal truth:</b> Every user shares one pain — the gap between "
    "<i>'I need this'</i> and <i>'this is ready.'</i> Orion closes that gap."
))
story.append(sp(8))

# ── Section 4 — Core Features ────────────────────────────────────────────────
story += section_title("04  Core Features")

# Feature 1
story += sub_title("Feature 1 — Smart Agent Router")
story.append(body_p(
    "Every input is classified <b>before</b> any LLM is called. Two modes exist:"
))
story.append(make_table(
    ["Mode", "Trigger Conditions", "LLM Used", "Typical Response Time"],
    [
        ["Secondary Agent",
         "Input < 12 words OR no document-intent keywords (factual, math, conversational)",
         "Groq only (1 call)", "< 2 seconds"],
        ["Primary Agent",
         "Input contains: plan, write, create, build, strategy, analyze, proposal, outline, schedule, research",
         "Groq + GPT-4o + Claude (3 calls)", "< 8 seconds"],
    ],
    col_widths=[32, 72, 44, 22]
))
story.append(sp(4))
story.append(body_p(
    "<b>Examples:</b> \"What is 2+2?\" → Secondary Agent.  "
    "\"Plan a 5-day trip to Vadodara\" → Primary Agent."
))
story.append(sp(8))

# Feature 2
story += sub_title("Feature 2 — 3-Stage Primary Agent Pipeline")
story.append(body_p("Visible to the user in real-time as animated step cards:"))
story.append(make_table(
    ["Stage", "Agent Name", "LLM", "Responsibility"],
    [
        ["1", "Research Agent", "Groq (Llama 3.3 70B)", "Gather context, define scope, extract key topics"],
        ["2", "Strategist", "OpenAI GPT-4o", "Structure outline, logic, hierarchy"],
        ["3", "Writer", "Claude Sonnet 4.6", "Draft final document with full markdown formatting"],
    ],
    col_widths=[12, 35, 50, 73]
))
story.append(sp(4))
story.append(body_p(
    "Each stage shows as a step card: icon, agent name, status (waiting / active / done), "
    "animated pulse when active, checkmark on completion."
))
story.append(sp(8))

# Feature 3
story += sub_title("Feature 3 — Real-Time Streaming Output")
for t in [
    "Text appears word-by-word as Writer agent produces it (identical to ChatGPT experience)",
    "Uses Server-Sent Events (SSE) from FastAPI backend — no polling",
    "Live character counter visible in output area while streaming",
    '"Stop generating" button cancels stream and keeps text produced so far',
    "Secondary Agent responses stream in under 2 seconds",
]:
    story.append(bullet_p(t))
story.append(sp(8))

# Feature 4
story += sub_title("Feature 4 — Editable Output")
for t in [
    "After generation, full document becomes editable inline — click anywhere to start editing",
    "Floating toolbar on text selection: Bold · Italic · Heading · Bullet list",
    "Changes auto-save to user account history",
    '"Reset to original" button restores the AI-generated version at any time',
    "Edit mode is visually distinct: border glow, cursor changes to text cursor",
]:
    story.append(bullet_p(t))
story.append(sp(8))

# Feature 5
story += sub_title("Feature 5 — Export System")
story.append(make_table(
    ["Button", "Output Format", "Library"],
    [
        ["Copy", "Clipboard text", "navigator.clipboard API"],
        ["Save .md", "Markdown file download", "Blob API (no library needed)"],
        ["Export PDF", "Formatted PDF", "jsPDF (frontend)"],
        ["Export DOCX", "Word document", "docx.js (frontend)"],
    ],
    col_widths=[30, 60, 80]
))
story.append(sp(4))
story.append(body_p(
    "All exports include: document title, generation timestamp, and model attribution footer."
))
story.append(sp(8))

# Feature 6
story += sub_title("Feature 6 — User Accounts (Auth)")
story.append(make_table(
    ["Aspect", "Specification"],
    [
        ["Auth Provider", "Clerk (free tier — handles UI, tokens, session management)"],
        ["Sign-up Methods", "Email + Password · Google OAuth"],
        ["Guest Limit", "3 free generations before sign-up prompt"],
        ["Free Tier", "50 generations/month after sign-up (no credit card required)"],
        ["Account Stores", "History · Edit saves · Model preference · Usage counter"],
        ["Account Page", "Usage counter · History list · Model preference · Delete account"],
    ],
    col_widths=[45, 125]
))
story.append(sp(8))

# Feature 7
story += sub_title("Feature 7 — Model Selector")
story.append(make_table(
    ["Option", "Models Used", "Availability", "Cost Label"],
    [
        ["Auto (Recommended)", "Smart routing — Groq for simple, all 3 for complex", "All users", "Free"],
        ["Groq Fast", "Groq Llama 3.3 70B only", "All users", "Free"],
        ["OpenAI GPT-4o", "GPT-4o for all stages", "Requires own API key", "Standard"],
        ["Claude Sonnet 4.6", "Claude Sonnet 4.6 for all stages", "Requires own API key", "Premium"],
    ],
    col_widths=[38, 68, 38, 26]
))
story.append(sp(8))

# Feature 8
story += sub_title("Feature 8 — Dark / Light Mode")
story.append(make_table(
    ["Token", "Dark Mode", "Light Mode", "Usage"],
    [
        ["Background", "#0D0D0D", "#F8F7F4", "Page background"],
        ["Surface", "#141414", "#FFFFFF", "Cards, panels"],
        ["Accent", "#E8C547 (Gold)", "#6366F1 (Indigo)", "CTAs, active states"],
        ["Text Primary", "#FFFFFF", "#1A1A2E", "Headings"],
        ["Text Secondary", "#9CA3AF", "#6B7280", "Labels, subtext"],
    ],
    col_widths=[35, 35, 35, 65]
))
story.append(sp(4))
story.append(body_p("Toggle in Header (moon/sun icon). Preference saved to localStorage and account."))
story.append(sp(8))

# Feature 9
story += sub_title("Feature 9 — Prompt Template Grid")
for t in [
    "20 pre-built templates shown on idle screen",
    "Category filter tabs: All / Business / Creators / Students / Agencies / Freelancers / Personal / General",
    "Click a card → auto-fills InputBox with a rich starter prompt",
    "Cards show: icon, title, audience badge, description, expected outcome",
    "Mobile: horizontal scroll carousel (1 card visible at a time)",
]:
    story.append(bullet_p(t))
story.append(sp(8))

# Feature 10
story += sub_title("Feature 10 — History")
for t in [
    "Last 20 generations stored per user (persisted to account, not just localStorage)",
    "History strip below InputBox on idle screen — horizontal scroll",
    "Each item: prompt preview (40 chars max) + doc type badge + timestamp",
    "Click item → reloads full output instantly (cached — no new API call)",
    "Delete individual items or clear all history",
]:
    story.append(bullet_p(t))
story.append(PageBreak())

# ── Section 5 — Screen Inventory ─────────────────────────────────────────────
story += section_title("05  Screen Inventory")
story.append(make_table(
    ["Screen", "Route", "Auth Required", "Notes"],
    [
        ["Home / Idle", "/", "No", "Hero + InputBox + Template Grid + History strip"],
        ["Generating (pipeline active)", "/ (phase change)", "No (3 free)", "AgentPipeline visible, InputBox disabled"],
        ["Output (done)", "/ (phase change)", "No (3 free)", "OutputCard with edit + export toolbar"],
        ["Sign Up", "/signup", "No", "Clerk managed UI"],
        ["Login", "/login", "No", "Clerk managed UI"],
        ["Account / Settings", "/account", "Yes", "Usage counter, model preference, API keys"],
        ["History", "/history", "Yes", "Full history list with search"],
        ["404 Not Found", "*", "No", "Redirect to home after 3 seconds"],
    ],
    col_widths=[42, 30, 25, 73]
))
story.append(sp(8))

# ── Section 6 — Key User Flows ───────────────────────────────────────────────
story += section_title("06  Key User Flows")

flows = [
    ("Flow 1 — New User, Complex Task (Primary Agent)", [
        "User lands on homepage → sees Hero, InputBox, Template Grid",
        'Types: "Plan a 5-day trip to Vadodara" → presses Enter',
        "Router classifies input → Primary Agent (contains 'plan', 'trip')",
        "AgentPipeline shows 3 animated steps: Research → Strategist → Writer",
        "OutputCard appears, text streams in word-by-word via SSE",
        "Stream completes → Edit / Export buttons become active",
        "Banner: \"Sign up to save this document\" (if not logged in)",
        "[Optional] User clicks Sign Up → Clerk modal opens inline",
    ]),
    ("Flow 2 — Simple Question (Secondary Agent)", [
        'User types: "What is compound interest?" (9 words, no doc intent)',
        "Router classifies → Secondary Agent",
        "NO pipeline shown — single 'Thinking...' spinner only",
        "Clean answer streams in under 2 seconds",
        "OutputCard shows clean formatted answer (no multi-step header)",
    ]),
    ("Flow 3 — Returning User", [
        "User logs in → lands on home screen",
        "History strip shows last 5 generations with timestamps",
        "User clicks a history item → output reloads instantly (no API call)",
        "User edits a section → changes auto-saved to account",
        "User clicks Export PDF → PDF downloads with document title",
    ]),
    ("Flow 4 — Model Selection", [
        "User clicks model dropdown in Header",
        "Sees: Auto (Recommended) / Groq Fast / GPT-4o / Claude Sonnet 4.6",
        'Selects "Claude Sonnet 4.6" → badge appears below InputBox',
        "Next generation uses Claude Sonnet 4.6 for the Writer stage",
        "Preference saved to account for future sessions",
    ]),
]

for title, steps in flows:
    story += sub_title(title)
    for i, step in enumerate(steps, 1):
        story.append(Paragraph(
            f"<b>{i}.</b> {step}",
            S(f'Step{i}', fontSize=9.5, textColor=colors.HexColor('#2D3748'),
              fontName='Helvetica', leading=15, leftIndent=14, spaceAfter=3)
        ))
    story.append(sp(8))

# ── Section 7 — Success Metrics ──────────────────────────────────────────────
story += section_title("07  Success Metrics")
story.append(make_table(
    ["Metric", "Target", "How to Measure"],
    [
        ["Time to first output (complex)", "< 8 seconds", "Frontend timer: submit → first SSE token received"],
        ["Time to first output (simple)", "< 2 seconds", "Frontend timer: submit → first SSE token received"],
        ["Generation success rate", "> 95%", "Backend error rate logs (non-5xx / total requests)"],
        ["7-day user return rate", "> 40%", "Account login timestamps (Clerk analytics)"],
        ["Export used per session", "> 30%", "Click event tracking on export buttons"],
        ["Sign-up conversion (guest→account)", "> 20%", "Clerk dashboard conversion funnel"],
        ["Mobile sessions", "> 35% of total", "Analytics (user-agent / viewport tracking)"],
        ["Speed vs ChatGPT (complex doc)", "2x faster", "Internal benchmark: same prompt, same doc type"],
    ],
    col_widths=[55, 30, 85]
))
story.append(sp(8))

# ── Section 8 — Out of Scope ─────────────────────────────────────────────────
story += section_title("08  Out of Scope (v1)")
out_of_scope = [
    "Real-time collaboration (multiple users editing the same document simultaneously)",
    "Paid subscription / billing system (v1 is free with API key rate limits only)",
    "Image generation or multimodal inputs",
    "Voice input or text-to-speech output",
    "Plugin / integration marketplace",
    "Direct export to Notion, Linear, Google Docs, or Slack",
    "Custom agent building by end users",
    "Team or workspace accounts (multi-user organisations)",
    "Native mobile app (iOS / Android) — web only, but fully responsive",
    "Offline mode or local LLM support",
]
for item in out_of_scope:
    story.append(bullet_p(item))
story.append(sp(8))

# ── Section 9 — Development Phases ───────────────────────────────────────────
story += section_title("09  Development Phases")
story.append(make_table(
    ["Phase", "Items", "Goal"],
    [
        ["Phase 1\nWeek 1\nCore MVP",
         "• Clerk auth (sign up, login, account page)\n"
         "• Smart router: Secondary vs Primary classification\n"
         "• Secondary agent: single Groq call, instant stream\n"
         "• Fix IPv6 proxy (already done)\n"
         "• localStorage → account-based history\n"
         "• Dark / Light mode toggle",
         "App works end-to-end for logged-in users with real AI output"],
        ["Phase 2\nWeek 2\nFull Pipeline",
         "• 3-stage primary pipeline (Groq + GPT-4o + Claude)\n"
         "• Streaming output (SSE) fully working\n"
         "• Editable output with inline toolbar\n"
         "• PDF + DOCX export\n"
         "• Model selector dropdown\n"
         "• Mobile responsive polish",
         "All core features working. Ready for real user testing"],
        ["Phase 3\nWeek 3+\nPolish",
         "• Framer Motion animations (pipeline steps, card stagger)\n"
         "• Usage counter (50 free/month)\n"
         "• Full history page with search\n"
         "• Error states + retry logic\n"
         "• Performance: < 8s p95 generation time\n"
         "• SEO meta tags + OG image",
         "Production quality. Shareable, performant, and polished"],
    ],
    col_widths=[25, 100, 45]
))
story.append(sp(8))

# ── Section 10 — Privacy & Safety ────────────────────────────────────────────
story += section_title("10  Privacy & Safety")
story.append(make_table(
    ["Rule", "Implementation"],
    [
        ["No guest input stored", "Guest inputs are never persisted — cleared on session end"],
        ["API keys never exposed", "All LLM calls route through FastAPI backend — keys stay server-side"],
        ["Minimal data stored", "Only: userId, prompt text, output text, timestamp, model used"],
        ["Input sanitisation", "Strip HTML tags, 1000 char limit, 10 req/min per IP (unauthenticated)"],
        ["Rate limiting", "10 RPM per IP (guest) · 30 RPM per account (authenticated)"],
        ["Output disclaimer", "Small footer: 'AI-generated content. Verify before use.'"],
        ["No model training", "User inputs are never used to train or fine-tune any model"],
    ],
    col_widths=[50, 120]
))
story.append(sp(8))

# ── Section 11 — Definition of Done ─────────────────────────────────────────
story += section_title("11  Definition of Done")
story += sub_title("A Feature is Done When:")
checks = [
    "Works on Chrome, Firefox, and Safari (latest versions)",
    "Works on mobile at 375px minimum viewport width",
    "Works with all 3 LLMs (Groq, OpenAI, Claude) without errors",
    "Error state is handled — shows user-friendly message, never a blank screen",
    "Loading state is shown at all times — never blank while waiting",
    "Logged-in user can access output from history after full page refresh",
]
for c in checks:
    story.append(bullet_p(c))

story.append(sp(8))
story += sub_title("The Product is Launch-Ready When:")
launch = [
    "All Phase 1 + Phase 2 checklist items are completed",
    "Zero console errors on idle screen and full generation flow",
    "Generation works end-to-end on a real mobile device",
    "Auth flow works: sign up → generate → edit → export",
    "Backend health endpoint returns {agents_ready: true}",
]
for c in launch:
    story.append(bullet_p(c))
story.append(sp(8))

# ── Section 12 — Design System ───────────────────────────────────────────────
story += section_title("12  Design System")

story += sub_title("Colour Tokens")
story.append(make_table(
    ["Token", "Dark Mode", "Light Mode", "Usage"],
    [
        ["bg-primary", "#0D0D0D", "#F8F7F4", "Page background"],
        ["bg-surface", "#141414", "#FFFFFF", "Cards, panels"],
        ["bg-elevated", "#1C1C1C", "#F0EEE9", "Input fields, hover states"],
        ["accent", "#E8C547 Gold", "#6366F1 Indigo", "CTAs, active indicators"],
        ["text-primary", "#FFFFFF", "#1A1A2E", "Headings, important text"],
        ["text-secondary", "#9CA3AF", "#6B7280", "Labels, subtext, placeholders"],
        ["border", "rgba(255,255,255,0.08)", "rgba(0,0,0,0.08)", "Card and input borders"],
        ["success", "#22C55E", "#16A34A", "Agent done, success states"],
        ["error", "#EF4444", "#DC2626", "Error messages, failure states"],
    ],
    col_widths=[32, 38, 38, 62]
))
story.append(sp(8))

story += sub_title("Typography")
story.append(make_table(
    ["Role", "Font", "Sizes", "Inspired by"],
    [
        ["Headings", "Instrument Serif", "28px / 40px", "Framer — editorial, premium feel"],
        ["Body / UI", "Geist", "12 / 14 / 16 / 20px", "Linear / Notion — clean, technical"],
        ["Code / Output", "Geist Mono", "13 / 14px", "Developer-friendly monospace"],
    ],
    col_widths=[30, 40, 40, 60]
))
story.append(sp(8))

story += sub_title("Spacing & Shape")
story.append(make_table(
    ["Property", "Value"],
    [
        ["Base unit", "4px"],
        ["Card padding", "20px"],
        ["Section gaps", "24px"],
        ["Max content width", "860px (centred)"],
        ["Card border radius", "16px"],
        ["Button border radius", "10px"],
        ["Badge / pill radius", "99px"],
        ["Input border radius", "14px"],
    ],
    col_widths=[50, 120]
))
story.append(sp(8))

story += sub_title("Component Design References")
story.append(make_table(
    ["Component", "Inspired by", "Key Characteristic"],
    [
        ["InputBox", "Perplexity", "Large, centred, focused — the hero of the screen"],
        ["Agent Pipeline", "Linear", "Clean step tracker with status icons"],
        ["OutputCard", "Notion", "Clean document canvas, readable typography"],
        ["Template Grid", "Framer", "Icon cards with descriptions and audience tags"],
        ["Header", "Linear", "Minimal, shows live status indicators"],
        ["History Strip", "Notion sidebar", "Compact horizontal scroll, recent items"],
    ],
    col_widths=[38, 35, 97]
))

# ── Footer on every page ─────────────────────────────────────────────────────
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MID_GREY)
    footer_text = f"Orion AI — Product Requirements Document v1.0  ·  {datetime.now().strftime('%B %Y')}  ·  Confidential"
    canvas.drawString(MARGIN, 12*mm, footer_text)
    canvas.drawRightString(PAGE_W - MARGIN, 12*mm, f"Page {doc.page}")
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 14*mm, PAGE_W - MARGIN, 14*mm)
    canvas.restoreState()

doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
print(f"PDF saved to: {OUTPUT_PATH}")
