from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from datetime import datetime

# ── Colours ─────────────────────────────────────────────────────────────────
GOLD        = colors.HexColor('#E8C547')
NAVY        = colors.HexColor('#0D1B2A')
DARK_GREY   = colors.HexColor('#1C2B3A')
MID_GREY    = colors.HexColor('#4A5568')
LIGHT_GREY  = colors.HexColor('#F7F8FA')
WHITE       = colors.white
INDIGO      = colors.HexColor('#6366F1')
SUCCESS     = colors.HexColor('#22C55E')
WARNING     = colors.HexColor('#F59E0B')
ERROR_RED   = colors.HexColor('#EF4444')
TABLE_HEAD  = colors.HexColor('#0D1B2A')
TABLE_ALT   = colors.HexColor('#F0F4F8')
BORDER_CLR  = colors.HexColor('#E2E8F0')
CODE_BG     = colors.HexColor('#F1F5F9')
CALLOUT_BG  = colors.HexColor('#FFFBEA')
INDIGO_BG   = colors.HexColor('#EEF2FF')

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
CONTENT_W = PAGE_W - 2 * MARGIN

OUTPUT_PATH = r"M:\Learning FrontEnd\orion\Orion_AI_TRD.pdf"

doc = SimpleDocTemplate(
    OUTPUT_PATH, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=MARGIN, bottomMargin=18*mm,
    title="Orion AI — Technical Requirements Document",
    author="Orion AI Engineering",
)

# ── Styles ───────────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

cover_title = S('CT', fontSize=44, textColor=GOLD, fontName='Helvetica-Bold',
                alignment=TA_CENTER, leading=52)
cover_sub   = S('CS', fontSize=15, textColor=WHITE, fontName='Helvetica',
                alignment=TA_CENTER, leading=22)
cover_meta  = S('CM', fontSize=10, textColor=colors.HexColor('#9CA3AF'),
                fontName='Helvetica', alignment=TA_CENTER, leading=16)
h1 = S('H1', fontSize=17, textColor=GOLD, fontName='Helvetica-Bold',
        leading=22, spaceBefore=12, spaceAfter=5)
h2 = S('H2', fontSize=12, textColor=NAVY, fontName='Helvetica-Bold',
        leading=17, spaceBefore=9, spaceAfter=3)
h3 = S('H3', fontSize=10.5, textColor=INDIGO, fontName='Helvetica-Bold',
        leading=15, spaceBefore=6, spaceAfter=2)
body = S('Body', fontSize=9.5, textColor=colors.HexColor('#2D3748'),
         fontName='Helvetica', leading=15, spaceAfter=4)
bullet = S('Blt', fontSize=9.5, textColor=colors.HexColor('#2D3748'),
           fontName='Helvetica', leading=15, leftIndent=14, spaceAfter=3)
sub_bullet = S('SBlt', fontSize=9, textColor=MID_GREY,
               fontName='Helvetica', leading=14, leftIndent=28, spaceAfter=2)
code_s = S('Code', fontSize=8.5, textColor=colors.HexColor('#1A202C'),
           fontName='Courier', leading=13, backColor=CODE_BG,
           leftIndent=10, rightIndent=10, spaceAfter=4,
           borderPadding=(4, 6, 4, 6))
note = S('Note', fontSize=8.5, textColor=MID_GREY,
         fontName='Helvetica-Oblique', leading=13, spaceAfter=3)
badge_s = S('Badge', fontSize=8, textColor=WHITE, fontName='Helvetica-Bold',
            alignment=TA_CENTER)

def rule(color=GOLD, thickness=1.2, width='100%'):
    return HRFlowable(width=width, thickness=thickness, color=color,
                      spaceAfter=5, spaceBefore=2)

def section(emoji, number, title):
    return [rule(GOLD, 1.5), Paragraph(f"{emoji}  {number}  {title}", h1), Spacer(1, 3)]

def sub(text):
    return [Paragraph(text, h2)]

def sub3(text):
    return [Paragraph(text, h3)]

def p(text):
    return Paragraph(text, body)

def b(text):
    return Paragraph(f"• {text}", bullet)

def sb(text):
    return Paragraph(f"◦ {text}", sub_bullet)

def sp(n=6):
    return Spacer(1, n)

def callout(text, bg=CALLOUT_BG, border=GOLD):
    t = Table([[Paragraph(text, S('CL', fontSize=9.5, fontName='Helvetica',
                textColor=NAVY, leading=15))]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg),
        ('LINEABOVE',  (0,0), (-1,0),  2.5, border),
        ('LINEBELOW',  (0,0), (-1,-1), 2.5, border),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    return t

# ── Table builder ─────────────────────────────────────────────────────────────
def tbl(headers, rows, col_widths_mm=None, stripe=True):
    def th(txt):
        return Paragraph(f"<b>{txt}</b>", S('TH', fontSize=9,
               textColor=WHITE, fontName='Helvetica-Bold', leading=13))
    def td(txt, bold=False):
        fn = 'Helvetica-Bold' if bold else 'Helvetica'
        return Paragraph(str(txt), S('TD', fontSize=8.5,
               textColor=colors.HexColor('#1A202C'), fontName=fn, leading=13))

    data = [[th(h) for h in headers]]
    for row in rows:
        data.append([td(c) for c in row])

    if col_widths_mm:
        cw = [w * mm for w in col_widths_mm]
    else:
        cw = [CONTENT_W / len(headers)] * len(headers)

    t = Table(data, colWidths=cw, repeatRows=1)
    alts = [WHITE, TABLE_ALT] if stripe else [WHITE, WHITE]
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),  (-1,0),  TABLE_HEAD),
        ('ROWBACKGROUNDS',(0,1),  (-1,-1), alts),
        ('GRID',          (0,0),  (-1,-1), 0.35, BORDER_CLR),
        ('VALIGN',        (0,0),  (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),  (-1,-1), 5),
        ('BOTTOMPADDING', (0,0),  (-1,-1), 5),
        ('LEFTPADDING',   (0,0),  (-1,-1), 6),
        ('RIGHTPADDING',  (0,0),  (-1,-1), 6),
        ('LINEABOVE',     (0,1),  (-1,1),  1, GOLD),
    ]))
    return t

def badge_tbl(text, color=INDIGO):
    t = Table([[Paragraph(f"<b>{text}</b>", badge_s)]],
              colWidths=[30*mm], rowHeights=[14])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), color),
        ('TOPPADDING',    (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING',   (0,0), (-1,-1), 4),
        ('RIGHTPADDING',  (0,0), (-1,-1), 4),
    ]))
    return t

# ── Footer ────────────────────────────────────────────────────────────────────
def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(MID_GREY)
    txt = f"Orion AI — Technical Requirements Document v1.0  ·  {datetime.now().strftime('%B %Y')}  ·  Engineering Confidential"
    canvas.drawString(MARGIN, 11*mm, txt)
    canvas.drawRightString(PAGE_W - MARGIN, 11*mm, f"Page {doc.page}")
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 13*mm, PAGE_W - MARGIN, 13*mm)
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════════════════════
# STORY
# ═══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ────────────────────────────────────────────────────────────────────
cover = Table([['']],
              colWidths=[CONTENT_W], rowHeights=[260])
cover.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), NAVY),
    ('TOPPADDING',    (0,0), (-1,-1), 60),
    ('BOTTOMPADDING', (0,0), (-1,-1), 60),
]))
story.append(cover)
story.append(sp(18))
story.append(Paragraph("ORION AI", cover_title))
story.append(sp(8))
story.append(Paragraph("Technical Requirements Document", cover_sub))
story.append(sp(6))
story.append(rule(GOLD, 1.5, '30%'))
story.append(sp(6))
story.append(Paragraph(
    f"Version 1.0  ·  {datetime.now().strftime('%B %d, %Y')}  ·  Engineering Confidential",
    cover_meta))
story.append(sp(14))

meta_rows = [
    ["Document Type",   "Technical Requirements Document (TRD)"],
    ["Based On",        "Orion AI PRD v1.0"],
    ["Stack",           "React + Vite  ·  FastAPI  ·  Supabase  ·  Railway  ·  Clerk"],
    ["AI Services",     "Groq (Llama 3.3 70B)  ·  OpenAI GPT-4o  ·  Claude Sonnet 4.6"],
    ["Target Timeline", "7 days  ·  8 hours/day  =  56 hours total"],
    ["Deployment",      "Backend → Railway  ·  Frontend → Vercel"],
]
mt = Table(
    [[Paragraph(f"<b>{r[0]}</b>", S('ML', fontSize=9, fontName='Helvetica-Bold',
       textColor=NAVY)), Paragraph(r[1], body)] for r in meta_rows],
    colWidths=[48*mm, CONTENT_W - 48*mm]
)
mt.setStyle(TableStyle([
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [LIGHT_GREY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, BORDER_CLR),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('LINEABOVE', (0,0), (-1,0), 2, GOLD),
    ('LINEBELOW', (0,-1), (-1,-1), 2, GOLD),
]))
story.append(mt)
story.append(PageBreak())

# ── TABLE OF CONTENTS ────────────────────────────────────────────────────────
story += section('📋', '', 'Table of Contents')
toc_items = [
    ("01", "Document Overview",          "3"),
    ("02", "System Architecture",        "3"),
    ("03", "Technology Stack",           "4"),
    ("04", "Database Schema",            "5"),
    ("05", "API Design",                 "7"),
    ("06", "Security & Rate Limiting",   "9"),
    ("07", "AI Integration",             "10"),
    ("08", "Deployment Strategy",        "11"),
    ("09", "Performance Requirements",   "12"),
    ("10", "Cost Estimate",              "13"),
    ("11", "Development Checklist",      "14"),
    ("12", "Technical Success Criteria", "16"),
]
for num, title, pg in toc_items:
    t = Table(
        [[Paragraph(f"<b>{num}</b>", S('TN', fontSize=9.5, fontName='Helvetica-Bold',
           textColor=GOLD)),
          Paragraph(title, S('TT', fontSize=9.5, fontName='Helvetica',
           textColor=NAVY)),
          Paragraph(pg, S('TP', fontSize=9.5, fontName='Helvetica',
           textColor=MID_GREY, alignment=TA_RIGHT))]],
        colWidths=[14*mm, CONTENT_W - 26*mm, 12*mm]
    )
    t.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, BORDER_CLR),
    ]))
    story.append(t)
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# 01 — DOCUMENT OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += section('📊', '01', 'Document Overview')
story.append(p(
    "This TRD translates the Orion AI PRD into precise engineering specifications, optimised for "
    "AI-assisted development using Claude Code, Cursor, and v0.dev. Every table, field name, "
    "endpoint path, and library name in this document is intentionally exact — paste it into an "
    "AI coding tool and it will implement correctly first time."
))
story.append(sp(6))
story.append(tbl(
    ["Constraint", "Decision", "Reason"],
    [
        ["Frontend Framework", "React + Vite (existing)", "Already built — no migration cost"],
        ["Backend Framework", "FastAPI (Python, existing)", "SSE streaming works, LLM ecosystem is Python-native"],
        ["Database", "Supabase (PostgreSQL)", "Free tier generous, SQL = predictable, Clerk syncs well"],
        ["Auth", "Clerk", "Handles UI, tokens, OAuth — zero custom auth code"],
        ["Backend Hosting", "Railway", "Free trial, git-push deploy, env vars UI"],
        ["Frontend Hosting", "Vercel", "One-command deploy for Vite, free tier, global CDN"],
        ["Streaming", "Server-Sent Events (SSE)", "Already implemented, simpler than WebSockets for one-way stream"],
        ["File Export", "jsPDF + docx.js (frontend)", "No server load, works offline, free libraries"],
    ],
    col_widths_mm=[40, 50, 80]
))
story.append(sp(8))

# ══════════════════════════════════════════════════════════════════════════════
# 02 — SYSTEM ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
story += section('🏗️', '02', 'System Architecture')

arch_data = [
    [
        Paragraph("<b>BROWSER</b>\nReact + Vite\nVercel CDN", S('AB', fontSize=9,
                  fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER,
                  leading=14)),
        Paragraph("→\nHTTPS / SSE", S('AR', fontSize=8, fontName='Helvetica',
                  textColor=MID_GREY, alignment=TA_CENTER, leading=13)),
        Paragraph("<b>FASTAPI BACKEND</b>\nRailway Container\n:8000", S('AB', fontSize=9,
                  fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER,
                  leading=14)),
        Paragraph("→\nREST", S('AR', fontSize=8, fontName='Helvetica',
                  textColor=MID_GREY, alignment=TA_CENTER, leading=13)),
        Paragraph("<b>SUPABASE</b>\nPostgreSQL\nFree Tier", S('AB', fontSize=9,
                  fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER,
                  leading=14)),
    ]
]
arch_t = Table(arch_data, colWidths=[40*mm, 22*mm, 48*mm, 18*mm, 42*mm])
arch_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (0,0), NAVY),
    ('BACKGROUND',    (2,0), (2,0), colors.HexColor('#1E3A5F')),
    ('BACKGROUND',    (4,0), (4,0), colors.HexColor('#166534')),
    ('BACKGROUND',    (1,0), (1,0), WHITE),
    ('BACKGROUND',    (3,0), (3,0), WHITE),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('BOX',           (0,0), (0,0), 1, GOLD),
    ('BOX',           (2,0), (2,0), 1, colors.HexColor('#3B82F6')),
    ('BOX',           (4,0), (4,0), 1, SUCCESS),
]))
story.append(arch_t)
story.append(sp(8))

ai_row = [
    Paragraph("<b>GROQ</b>\nLlama 3.3 70B\nResearch Agent", S('AB', fontSize=9,
              fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER, leading=14)),
    Paragraph("<b>OpenAI</b>\nGPT-4o\nStrategist", S('AB', fontSize=9,
              fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER, leading=14)),
    Paragraph("<b>Anthropic</b>\nClaude Sonnet 4.6\nWriter", S('AB', fontSize=9,
              fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER, leading=14)),
    Paragraph("<b>CLERK</b>\nAuth Provider\nJWT Tokens", S('AB', fontSize=9,
              fontName='Helvetica-Bold', textColor=WHITE, alignment=TA_CENTER, leading=14)),
]
ai_label = [
    Paragraph("↑ Stage 1", S('AL', fontSize=8, fontName='Helvetica',
              textColor=MID_GREY, alignment=TA_CENTER)),
    Paragraph("↑ Stage 2", S('AL', fontSize=8, fontName='Helvetica',
              textColor=MID_GREY, alignment=TA_CENTER)),
    Paragraph("↑ Stage 3", S('AL', fontSize=8, fontName='Helvetica',
              textColor=MID_GREY, alignment=TA_CENTER)),
    Paragraph("↑ Auth", S('AL', fontSize=8, fontName='Helvetica',
              textColor=MID_GREY, alignment=TA_CENTER)),
]
ai_t = Table([ai_row, ai_label],
             colWidths=[CONTENT_W/4]*4, rowHeights=[46, 14])
ai_t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), colors.HexColor('#7C3AED')),
    ('BACKGROUND', (1,0), (1,0), colors.HexColor('#0284C7')),
    ('BACKGROUND', (2,0), (2,0), colors.HexColor('#D97706')),
    ('BACKGROUND', (3,0), (3,0), colors.HexColor('#0F172A')),
    ('BACKGROUND', (0,1), (-1,1), WHITE),
    ('BOX',      (0,0), (0,0), 1, colors.HexColor('#7C3AED')),
    ('BOX',      (1,0), (1,0), 1, colors.HexColor('#0284C7')),
    ('BOX',      (2,0), (2,0), 1, colors.HexColor('#D97706')),
    ('BOX',      (3,0), (3,0), 1, colors.HexColor('#0F172A')),
    ('VALIGN',   (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,0), 10),
    ('BOTTOMPADDING', (0,0), (-1,0), 10),
    ('LEFTPADDING',  (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('SPAN',     (0,1), (-1,1)),
]))
story.append(p("External AI & Auth Services (all called from FastAPI backend):"))
story.append(sp(4))
story.append(ai_t)
story.append(sp(4))
story.append(callout(
    "Key architecture rule: The React frontend NEVER calls any LLM API directly. "
    "All Groq, OpenAI, and Claude calls happen inside FastAPI on Railway. "
    "API keys are Railway environment variables — never in frontend code or git history."
))
story.append(sp(8))

# ══════════════════════════════════════════════════════════════════════════════
# 03 — TECHNOLOGY STACK
# ══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story += section('🛠️', '03', 'Technology Stack')
story.append(tbl(
    ["Layer", "Technology", "Package / Service", "Why This Choice"],
    [
        ["Frontend UI", "React 18 + Vite 5", "react, vite (existing)", "Already built and running"],
        ["Styling", "Tailwind CSS", "tailwindcss (existing)", "Utility-first, fast to build"],
        ["Animations", "Framer Motion", "framer-motion (installed)", "Installed but unused — activate"],
        ["Markdown render", "react-markdown", "react-markdown + remark-gfm", "Renders AI output with formatting"],
        ["Inline editing", "ContentEditable + Tiptap", "tiptap/react, tiptap/starter-kit", "Rich text editing, headless, free"],
        ["PDF export", "jsPDF + html2canvas", "jspdf, html2canvas", "Converts OutputCard DOM to PDF"],
        ["DOCX export", "docx.js", "docx", "Generates Word files in browser"],
        ["HTTP client", "Native fetch", "Built into browser", "SSE streaming requires native fetch"],
        ["Auth (frontend)", "Clerk React SDK", "@clerk/clerk-react", "Drop-in auth UI components"],
        ["State management", "React hooks only", "useState, useContext, custom hooks", "No Redux — overkill for this app"],
        ["", "", "", ""],
        ["Backend framework", "FastAPI", "fastapi, uvicorn (existing)", "Async, SSE support, Python LLM ecosystem"],
        ["Auth (backend)", "Clerk JWT verify", "clerk-backend (Python)", "Verify Clerk tokens server-side"],
        ["Database client", "Supabase Python", "supabase", "Official Python client for Supabase"],
        ["Groq client", "Groq Python SDK", "groq", "Official client, streaming support"],
        ["OpenAI client", "OpenAI Python SDK", "openai", "Official client, streaming support"],
        ["Anthropic client", "Anthropic Python SDK", "anthropic", "Official client, streaming support"],
        ["Rate limiting", "slowapi", "slowapi", "FastAPI-native rate limiter, Redis optional"],
        ["Env management", "python-dotenv", "python-dotenv (existing)", "Loads .env in dev, Railway vars in prod"],
        ["CORS", "FastAPI middleware", "fastapi.middleware.cors (existing)", "Already configured"],
        ["", "", "", ""],
        ["Database", "Supabase", "supabase.com (free tier)", "PostgreSQL + realtime + REST API auto-gen"],
        ["Auth provider", "Clerk", "clerk.com (free tier)", "10,000 MAU free, Google OAuth included"],
        ["Backend hosting", "Railway", "railway.app (free trial)", "Git-push deploy, env vars, sleep-free"],
        ["Frontend hosting", "Vercel", "vercel.com (free tier)", "One-command Vite deploy, global CDN"],
        ["LLM — Fast", "Groq", "console.groq.com (free tier)", "Llama 3.3 70B, ~2s response, free"],
        ["LLM — Smart", "OpenAI", "platform.openai.com (pay-per-use)", "GPT-4o for Strategist stage"],
        ["LLM — Writer", "Anthropic", "console.anthropic.com (pay-per-use)", "Claude Sonnet 4.6 for final draft"],
    ],
    col_widths_mm=[28, 32, 42, 68]
))
story.append(sp(4))
story.append(p("<b>Install command for new frontend packages:</b>"))
story.append(Paragraph(
    "npm install react-markdown remark-gfm @tiptap/react @tiptap/starter-kit jspdf html2canvas docx",
    code_s))
story.append(p("<b>Install command for new backend packages:</b>"))
story.append(Paragraph(
    "pip install supabase clerk-backend slowapi anthropic",
    code_s))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# 04 — DATABASE SCHEMA
# ══════════════════════════════════════════════════════════════════════════════
story += section('🗄️', '04', 'Database Schema')
story.append(p(
    "All tables live in Supabase (PostgreSQL). Run the SQL below in the Supabase SQL Editor. "
    "Row Level Security (RLS) is enabled on every table — users can only read/write their own rows."
))
story.append(sp(6))

# Table 1
story += sub("Table 1 — documents")
story.append(p("Stores every generated document. One row per generation."))
story.append(tbl(
    ["Column", "Type", "Constraints", "Description"],
    [
        ["id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "Unique document ID"],
        ["user_id", "text", "NOT NULL, INDEX", "Clerk user ID (format: user_xxxxxxxx)"],
        ["prompt", "text", "NOT NULL, max 1000 chars", "Original user input"],
        ["result", "text", "NOT NULL", "Full AI-generated markdown output"],
        ["doc_type", "text", "NOT NULL", "business_plan · travel_planning · study_plan · etc."],
        ["agent_mode", "text", "NOT NULL, CHECK IN ('primary','secondary')", "Which pipeline was used"],
        ["model_used", "text", "NOT NULL", "groq · openai · claude · auto"],
        ["word_count", "integer", "NOT NULL, DEFAULT 0", "Word count of result field"],
        ["is_edited", "boolean", "NOT NULL, DEFAULT false", "True if user modified the output"],
        ["edited_result", "text", "NULLABLE", "User-edited version (null until first edit)"],
        ["is_deleted", "boolean", "NOT NULL, DEFAULT false", "Soft delete flag"],
        ["generation_ms", "integer", "NULLABLE", "Time in ms from submit to stream complete"],
        ["created_at", "timestamptz", "NOT NULL, DEFAULT now()", "When generated"],
        ["updated_at", "timestamptz", "NOT NULL, DEFAULT now()", "Last edit timestamp"],
    ],
    col_widths_mm=[30, 22, 52, 66]
))
story.append(sp(8))

# Table 2
story += sub("Table 2 — user_preferences")
story.append(p("One row per user. Created on first login via upsert."))
story.append(tbl(
    ["Column", "Type", "Constraints", "Description"],
    [
        ["id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "Unique row ID"],
        ["user_id", "text", "UNIQUE, NOT NULL", "Clerk user ID"],
        ["preferred_model", "text", "NOT NULL, DEFAULT 'auto'", "auto · groq · openai · claude"],
        ["theme", "text", "NOT NULL, DEFAULT 'dark'", "dark · light"],
        ["monthly_usage", "integer", "NOT NULL, DEFAULT 0", "Generations this calendar month"],
        ["usage_reset_at", "timestamptz", "NOT NULL, DEFAULT now()", "When monthly_usage resets"],
        ["created_at", "timestamptz", "NOT NULL, DEFAULT now()", "Account first seen"],
        ["updated_at", "timestamptz", "NOT NULL, DEFAULT now()", "Last preference change"],
    ],
    col_widths_mm=[30, 22, 52, 66]
))
story.append(sp(8))

# Table 3
story += sub("Table 3 — usage_logs")
story.append(p("Analytics and rate limiting. One row per API request to /generate or /generate/stream."))
story.append(tbl(
    ["Column", "Type", "Constraints", "Description"],
    [
        ["id", "uuid", "PRIMARY KEY, DEFAULT gen_random_uuid()", "Unique log ID"],
        ["user_id", "text", "NULLABLE, INDEX", "Null for guest requests"],
        ["ip_address", "text", "NOT NULL, INDEX", "Hashed IP for guest rate limiting"],
        ["endpoint", "text", "NOT NULL", "'/generate' or '/generate/stream'"],
        ["agent_mode", "text", "NULLABLE", "'primary' or 'secondary'"],
        ["model_used", "text", "NULLABLE", "Which LLM(s) were called"],
        ["tokens_used", "integer", "NULLABLE", "Estimated total tokens across all LLM calls"],
        ["success", "boolean", "NOT NULL", "False if any LLM call threw an error"],
        ["error_message", "text", "NULLABLE", "Error string if success = false"],
        ["duration_ms", "integer", "NULLABLE", "Total request duration in ms"],
        ["created_at", "timestamptz", "NOT NULL, DEFAULT now(), INDEX", "When request was made"],
    ],
    col_widths_mm=[30, 22, 52, 66]
))
story.append(sp(8))

# RLS policies
story += sub("Row Level Security Policies")
story.append(tbl(
    ["Table", "Operation", "Policy", "Who Can"],
    [
        ["documents", "SELECT", "auth.uid()::text = user_id", "Owner only"],
        ["documents", "INSERT", "auth.uid()::text = user_id", "Owner only"],
        ["documents", "UPDATE", "auth.uid()::text = user_id AND is_deleted = false", "Owner only, not deleted"],
        ["documents", "DELETE", "NONE — use soft delete", "Nobody — set is_deleted=true instead"],
        ["user_preferences", "ALL", "auth.uid()::text = user_id", "Owner only"],
        ["usage_logs", "INSERT", "true (service role only in practice)", "Backend service role key only"],
        ["usage_logs", "SELECT", "auth.uid()::text = user_id", "Owner can read their own logs"],
    ],
    col_widths_mm=[32, 22, 72, 44]
))
story.append(callout(
    "Supabase setup: Create project → SQL Editor → run CREATE TABLE statements above → "
    "Enable RLS on each table → Add policies above → Copy 'anon key' and 'service role key' to Railway env vars."
))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# 05 — API DESIGN
# ══════════════════════════════════════════════════════════════════════════════
story += section('🔌', '05', 'API Design')
story.append(p(
    "All endpoints are on the FastAPI backend (Railway). The Vite proxy forwards "
    "<b>/api/*</b> → <b>http://127.0.0.1:8000/*</b> in development. In production the "
    "frontend calls the Railway URL directly (set as VITE_API_URL env var)."
))
story.append(sp(6))

endpoints = [
    {
        "group": "Health & Status",
        "items": [
            ["GET", "/health", "None", '{"status":"ok","backend_live":true,"agents_ready":true}',
             "No auth", "Vite proxy uses this to show green/red dot in Header"],
        ]
    },
    {
        "group": "Generation",
        "items": [
            ["POST", "/classify", '{"input": string}',
             '{"mode":"primary"|"secondary","doc_type":string,"keywords":[string]}',
             "Optional JWT", "Router classifies input before generation. Called by frontend to show correct UI."],
            ["POST", "/generate/stream", '{"input":string, "model":"auto"|"groq"|"openai"|"claude"}',
             "SSE stream: data:{token:string} … data:[DONE]",
             "Optional JWT", "Main generation endpoint. SSE stream. Guests allowed (max 3 per IP/day)."],
            ["POST", "/generate", '{"input":string, "model":"auto"|"groq"|"openai"|"claude"}',
             '{"result":string,"doc_type":string,"agent_mode":string,"model_used":string,"generation_ms":int}',
             "Optional JWT", "Non-streaming fallback. Used if browser blocks SSE."],
        ]
    },
    {
        "group": "Documents (requires Clerk JWT)",
        "items": [
            ["GET", "/documents", "Query: limit=20, offset=0",
             '{"documents":[{id,prompt,doc_type,word_count,created_at}],"total":int}',
             "JWT required", "Paginated list for History page. Returns preview only (no full result)."],
            ["GET", "/documents/{doc_id}", "Path: doc_id (uuid)",
             '{"id":uuid,"prompt":str,"result":str,"doc_type":str,"is_edited":bool,"edited_result":str}',
             "JWT required", "Full document. Returns edited_result if is_edited=true, else result."],
            ["POST", "/documents", '{"prompt":str,"result":str,"doc_type":str,"agent_mode":str,"model_used":str,"word_count":int,"generation_ms":int}',
             '{"id":uuid,"created_at":timestamptz}',
             "JWT required", "Save a new generated document. Called after stream completes."],
            ["PUT", "/documents/{doc_id}", '{"edited_result":string}',
             '{"id":uuid,"updated_at":timestamptz}',
             "JWT required", "Save user edits. Sets is_edited=true, stores in edited_result."],
            ["DELETE", "/documents/{doc_id}", "Path: doc_id (uuid)",
             '{"success":true}',
             "JWT required", "Soft delete — sets is_deleted=true. Document stays in DB."],
        ]
    },
    {
        "group": "User Preferences (requires Clerk JWT)",
        "items": [
            ["GET", "/preferences", "None",
             '{"preferred_model":str,"theme":str,"monthly_usage":int,"usage_reset_at":timestamptz}',
             "JWT required", "Load user preferences on app start."],
            ["PUT", "/preferences", '{"preferred_model":str,"theme":str}',
             '{"updated_at":timestamptz}',
             "JWT required", "Save preference changes. Upserts row if not exists."],
            ["GET", "/usage", "None",
             '{"monthly_usage":int,"monthly_limit":50,"reset_at":timestamptz,"remaining":int}',
             "JWT required", "Usage counter for account page."],
        ]
    },
]

for group in endpoints:
    story += sub(group["group"])
    story.append(tbl(
        ["Method", "Path", "Input", "Output", "Auth", "Notes"],
        group["items"],
        col_widths_mm=[14, 38, 44, 40, 18, 16]
    ))
    story.append(sp(8))

story.append(callout(
    "Frontend env var: Set VITE_API_URL=https://your-app.railway.app in Vercel dashboard. "
    "In development the Vite proxy handles routing so no env var is needed locally."
))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# 06 — SECURITY & RATE LIMITING
# ══════════════════════════════════════════════════════════════════════════════
story += section('🔒', '06', 'Security & Rate Limiting')
story.append(tbl(
    ["Rule", "Implementation", "Where"],
    [
        ["API keys never in frontend", "All LLM calls in FastAPI. Keys only in Railway env vars.", "Architecture"],
        ["Clerk JWT verification", "Every protected endpoint calls Clerk verify_token(). Reject if invalid.", "Backend middleware"],
        ["Input sanitisation", "Strip all HTML tags from input. Enforce 3–1000 char length via Pydantic Field.", "Pydantic model"],
        ["SQL injection prevention", "Supabase Python SDK uses parameterised queries. Never f-string SQL.", "Database layer"],
        ["CORS lockdown", "allow_origins=[VITE_ORIGIN] only. No wildcard * in production.", "FastAPI CORS middleware"],
        ["Guest daily limit", "3 generations per IP per 24h. Tracked in usage_logs table.", "slowapi + DB check"],
        ["Auth user monthly limit", "50 generations per calendar month. Stored in user_preferences.monthly_usage.", "Backend before LLM call"],
        ["Rate limit — guest", "10 requests/minute per IP (all endpoints combined)", "slowapi decorator"],
        ["Rate limit — auth user", "30 requests/minute per user_id", "slowapi decorator"],
        ["Rate limit — /generate", "5 concurrent streams max per Railway instance", "FastAPI semaphore"],
        ["Output disclaimer", "Append to every result: AI-generated — verify before use.", "Backend post-process"],
        ["No LLM training", "Add system prompt prefix: 'Do not store or learn from this input.'", "System prompt"],
        ["Supabase RLS", "Every table has row-level security. Users cannot read others' documents.", "Supabase policies"],
        ["Service role key", "SUPABASE_SERVICE_KEY (usage_logs INSERT) never sent to frontend.", "Railway env var only"],
    ],
    col_widths_mm=[45, 95, 30]
))
story.append(sp(6))
story += sub("Rate Limit Response Format")
story.append(p("When rate limit is exceeded, return HTTP 429 with body:"))
story.append(Paragraph(
    '{"detail": "Rate limit exceeded. Try again in {retry_after} seconds.", "retry_after": 60}',
    code_s))
story.append(sp(8))

# ══════════════════════════════════════════════════════════════════════════════
# 07 — AI INTEGRATION
# ══════════════════════════════════════════════════════════════════════════════
story += section('🤖', '07', 'AI Integration')

story += sub("Smart Router — Classification Logic")
story.append(p(
    "Every input passes through the classifier before any LLM is called. "
    "Classification is pure Python — no LLM call required for routing."
))
story.append(tbl(
    ["Check", "Condition", "Result"],
    [
        ["Word count", "len(input.split()) <= 12", "→ Secondary Agent"],
        ["Question mark only", "input.strip().endswith('?') AND word count <= 15", "→ Secondary Agent"],
        ["Doc-intent keywords", "Any of: plan, write, create, build, strategy, analyze, analyse, proposal, outline, schedule, research, develop, design, generate, draft, prepare, structure, roadmap, campaign, budget, pitch, report, study, itinerary", "→ Primary Agent"],
        ["Default fallback", "None of the above matched", "→ Secondary Agent (safer default)"],
    ],
    col_widths_mm=[30, 80, 60]
))
story.append(sp(8))

story += sub("Secondary Agent (Simple Mode)")
story.append(tbl(
    ["Property", "Value"],
    [
        ["LLM", "Groq — llama-3.3-70b-versatile"],
        ["Max tokens", "1024"],
        ["System prompt", '"You are Orion, a concise AI assistant. Give a clear, direct answer. Use markdown only if it genuinely helps readability."'],
        ["Temperature", "0.7"],
        ["Expected latency", "< 2 seconds (Groq is fast)"],
        ["SSE streaming", "Yes — stream=True on Groq client"],
        ["Fallback", "If Groq fails → return 503 with retry_after=30. Do NOT fall back to demo output."],
    ],
    col_widths_mm=[35, 135]
))
story.append(sp(8))

story += sub("Primary Agent Pipeline (Complex Mode)")
story.append(tbl(
    ["Stage", "Agent", "LLM + Model", "Max Tokens", "System Prompt Goal", "Output Passed To"],
    [
        ["1", "Research Agent",
         "Groq\nllama-3.3-70b-versatile",
         "512",
         "Extract 5 key topics, define scope, identify user intent. Output JSON: {topics:[str], scope:str, format:str}",
         "Stage 2 as context"],
        ["2", "Strategist",
         "OpenAI\ngpt-4o",
         "1024",
         "Using the research context, create a detailed markdown outline with sections and subsections. Output only the outline.",
         "Stage 3 as structure"],
        ["3", "Writer",
         "Anthropic\nclaude-sonnet-4-6",
         "4096",
         "Write a complete, professional document following the outline exactly. Use headers (##), bullets, tables. Be thorough and actionable.",
         "SSE streamed to frontend"],
    ],
    col_widths_mm=[10, 20, 28, 14, 66, 32]
))
story.append(sp(6))
story.append(tbl(
    ["Property", "Value"],
    [
        ["Total pipeline latency target", "< 8 seconds (p95)"],
        ["Stage 1 timeout", "10 seconds — if exceeded, skip to Stage 2 with minimal context"],
        ["Stage 2 timeout", "15 seconds — if exceeded, skip to Stage 3 with only original prompt"],
        ["Stage 3 streaming", "SSE stream=True on Anthropic client — tokens forwarded directly to browser"],
        ["Stage 3 fallback", "If Claude fails → retry once with OpenAI gpt-4o as Writer"],
        ["Full pipeline fallback", "If all 3 stages fail → return 503. Never return demo/hardcoded content."],
        ["Context injection format", "Stage N receives: original_prompt + stage_{n-1}_output as user message"],
    ],
    col_widths_mm=[55, 115]
))
story.append(sp(6))
story.append(callout(
    "Critical rule: Never return hardcoded or demo content in production. "
    "If the LLM APIs fail, return a proper HTTP 503 error. "
    "The frontend shows a user-friendly error card with a Retry button. "
    "Hardcoded demo content only exists when DEMO_MODE=true env var is explicitly set."
))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# 08 — DEPLOYMENT STRATEGY
# ══════════════════════════════════════════════════════════════════════════════
story += section('🚀', '08', 'Deployment Strategy')
story.append(p("Full deployment in 8 steps. Do backend first, then frontend."))
story.append(sp(6))

steps = [
    ("Step 1", "Prepare Supabase (30 min)",
     "Create project at supabase.com → SQL Editor → Run CREATE TABLE for documents, user_preferences, usage_logs → "
     "Enable RLS → Add all 7 RLS policies → Copy Project URL, anon key, and service_role key"),
    ("Step 2", "Configure Clerk (20 min)",
     "Create app at clerk.com → Enable Email + Google OAuth → Copy CLERK_PUBLISHABLE_KEY (frontend) and "
     "CLERK_SECRET_KEY (backend) → Set allowed redirect URLs to your Vercel domain"),
    ("Step 3", "Add backend requirements.txt",
     "Ensure backend/requirements.txt includes: fastapi, uvicorn, python-dotenv, groq, openai, anthropic, "
     "supabase, slowapi, clerk-backend. Railway reads this file automatically."),
    ("Step 4", "Create Railway project (15 min)",
     "railway.app → New Project → Deploy from GitHub repo → Select the repo → Set Root Directory to /backend → "
     "Railway detects requirements.txt and builds automatically"),
    ("Step 5", "Set Railway environment variables",
     "In Railway dashboard → Variables tab → Add: GROQ_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, "
     "SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY, CLERK_SECRET_KEY, "
     "ALLOWED_ORIGINS=https://your-app.vercel.app, DEMO_MODE=false"),
    ("Step 6", "Get Railway public URL",
     "Railway → Settings → Networking → Generate Domain → Copy URL (e.g. orion-backend.railway.app). "
     "Test: curl https://orion-backend.railway.app/health → should return {agents_ready:true}"),
    ("Step 7", "Deploy frontend to Vercel (10 min)",
     "vercel.com → New Project → Import GitHub repo → Set Root Directory to /frontend → "
     "Framework preset: Vite → Add env var: VITE_API_URL=https://orion-backend.railway.app → Deploy"),
    ("Step 8", "Post-deploy smoke test",
     "Visit Vercel URL → Header should show green dot (backend live) → "
     "Type 'What is 2+2?' → Secondary agent responds < 2s → "
     "Type 'Write a business plan for a coffee shop' → Primary pipeline runs → "
     "Streaming text appears → Export PDF → Sign up → History saves"),
]

for step, title, desc in steps:
    step_t = Table(
        [[Paragraph(f"<b>{step}</b>", S('SN', fontSize=9, fontName='Helvetica-Bold',
           textColor=WHITE, alignment=TA_CENTER)),
          Paragraph(f"<b>{title}</b>", S('ST', fontSize=9.5, fontName='Helvetica-Bold',
           textColor=NAVY)),
          Paragraph(desc, S('SD', fontSize=8.5, fontName='Helvetica',
           textColor=colors.HexColor('#2D3748'), leading=13))]],
        colWidths=[16*mm, 40*mm, CONTENT_W - 56*mm]
    )
    step_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,0), INDIGO),
        ('BACKGROUND',    (1,0), (-1,0), LIGHT_GREY),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('LINEBELOW',     (0,0), (-1,-1), 0.4, BORDER_CLR),
    ]))
    story.append(step_t)
story.append(sp(6))
story.append(tbl(
    ["Service", "Free Tier Limit", "When It Runs Out"],
    [
        ["Railway", "$5 free trial credit", "Upgrade to Hobby ($5/month) — about 500 hours of runtime"],
        ["Vercel", "100GB bandwidth/month", "Upgrade to Pro ($20/month) — very unlikely to hit this early"],
        ["Supabase", "500MB database, 2GB bandwidth", "Upgrade to Pro ($25/month) — supports ~50,000 documents"],
        ["Clerk", "10,000 MAU free", "Upgrade to Pro ($25/month) — only if >10k monthly active users"],
    ],
    col_widths_mm=[30, 55, 85]
))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# 09 — PERFORMANCE REQUIREMENTS
# ══════════════════════════════════════════════════════════════════════════════
story += section('📊', '09', 'Performance Requirements')
story.append(tbl(
    ["Metric", "Target", "Measurement Method", "Fail Threshold"],
    [
        ["Secondary agent first token", "< 2 seconds", "Frontend: Date.now() on submit → first SSE token", "> 5 seconds"],
        ["Primary agent first token", "< 4 seconds", "Frontend: Date.now() on submit → first SSE token", "> 10 seconds"],
        ["Full primary generation", "< 12 seconds", "Frontend: Date.now() on submit → [DONE] received", "> 20 seconds"],
        ["Page initial load (Vercel CDN)", "< 1.5 seconds", "Chrome DevTools → LCP metric", "> 3 seconds"],
        ["Idle screen (no generation)", "60 FPS", "Chrome Performance tab — no jank", "< 30 FPS"],
        ["Pipeline animation (Framer Motion)", "60 FPS", "Chrome Performance tab", "< 30 FPS"],
        ["Mobile viewport (375px)", "Fully usable", "Test on real iPhone SE or Chrome 375px", "Horizontal scroll = fail"],
        ["Concurrent users on Railway", "10 simultaneous streams", "Railway free tier: 512MB RAM, 1 vCPU", "> 10 = queue or upgrade"],
        ["Supabase query latency", "< 100ms", "Supabase dashboard query stats", "> 300ms = add index"],
        ["API error rate", "< 2%", "usage_logs: COUNT(success=false) / total", "> 5% = alert"],
    ],
    col_widths_mm=[42, 28, 66, 34]
))
story.append(sp(6))
story += sub("Frontend Bundle Size Targets")
story.append(tbl(
    ["Asset", "Target", "How to Check"],
    [
        ["Total JS bundle (gzipped)", "< 250KB", "vite build → dist/assets/*.js size"],
        ["Largest chunk", "< 100KB", "vite build --report → bundle analyser"],
        ["CSS bundle", "< 30KB", "dist/assets/*.css"],
        ["react-markdown", "~15KB gzipped", "Lazy import: const MD = React.lazy(...)"],
        ["Framer Motion", "~35KB gzipped", "Already installed — acceptable"],
        ["jsPDF + html2canvas", "~80KB gzipped combined", "Lazy import: only load on export click"],
        ["docx.js", "~50KB gzipped", "Lazy import: only load on export click"],
    ],
    col_widths_mm=[48, 28, 94]
))
story.append(sp(8))

# ══════════════════════════════════════════════════════════════════════════════
# 10 — COST ESTIMATE
# ══════════════════════════════════════════════════════════════════════════════
story += section('💰', '10', 'Cost Estimate')
story.append(p(
    "Assumption: average generation = 70% secondary (Groq free), 30% primary (all 3 LLMs). "
    "Primary pipeline tokens: ~200 (Stage 1) + ~400 (Stage 2) + ~3000 (Stage 3) = ~3600 tokens per run."
))
story.append(sp(6))
story.append(tbl(
    ["Service", "100 users/month", "1,000 users/month", "10,000 users/month", "Free Tier"],
    [
        ["Railway (backend)", "$5 flat", "$5 flat", "$20-40 (scale up)", "Trial credit only"],
        ["Vercel (frontend)", "$0", "$0", "$0-20", "100GB bandwidth"],
        ["Supabase (database)", "$0", "$0", "$0-25", "500MB DB"],
        ["Clerk (auth)", "$0", "$0", "$0", "10,000 MAU"],
        ["Groq (secondary agent)", "$0", "$0", "$0", "Free rate limited"],
        ["OpenAI GPT-4o (stage 2)", "~$0.50", "~$5", "~$50", "Free trial credits"],
        ["Claude Sonnet 4.6 (stage 3)", "~$1.50", "~$15", "~$150", "Free trial credits"],
        ["TOTAL", "~$7/month", "~$25/month", "~$220/month", "First ~100 gens free"],
    ],
    col_widths_mm=[42, 28, 28, 34, 38]
))
story.append(sp(6))
story.append(callout(
    "Cost optimisation strategy: Route 70% of requests to Groq (free). Only run OpenAI + Claude "
    "when user explicitly requests it or input is clearly complex. "
    "Add a 'Groq Fast' button as default option — saves ~$0.03 per generation."
))
story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# 11 — DEVELOPMENT CHECKLIST
# ══════════════════════════════════════════════════════════════════════════════
story += section('📋', '11', 'Development Checklist')
story.append(p(
    "7 days × 8 hours = 56 hours. Tasks are ordered by dependency — do not skip ahead. "
    "Each day has a clear deliverable you can demo by end of day."
))
story.append(sp(6))

days = [
    ("Day 1", "Foundation & Auth", "Working sign-up → login → account page flow", [
        "Create Supabase project, run all 3 CREATE TABLE statements",
        "Enable RLS and add all 7 row-level security policies",
        "Create Clerk app, enable Google OAuth, copy keys",
        "Install @clerk/clerk-react in frontend",
        "Wrap App.jsx with <ClerkProvider publishableKey={VITE_CLERK_PUBLISHABLE_KEY}>",
        "Add <SignInButton /> and <UserButton /> to Header.jsx",
        "Create /account route: show user email, usage counter (hardcoded for now)",
        "Test: sign up → Google OAuth → see UserButton in header → log out → log back in",
        "Add Supabase Python client to backend, test connection with health check",
        "Create POST /preferences endpoint (upsert on first login)",
    ]),
    ("Day 2", "Smart Router + Secondary Agent", "Simple questions answer in < 2 seconds", [
        "Write classify() function in backend: word count check + keyword list matching",
        "Create POST /classify endpoint",
        "Create POST /generate/stream endpoint — secondary mode only (Groq, stream=True)",
        "Fix any remaining IPv6 proxy issues (change localhost → 127.0.0.1 in vite.config.js)",
        "Test /classify with 10 different inputs — verify routing is correct",
        "Test streaming: 'What is compound interest?' → tokens appear < 2s",
        "Update useGenerate.js: call /classify first, show correct UI based on mode",
        "Remove all SAMPLE_OUTPUTS fallbacks — replace with proper error state",
        "Add retry logic: if stream fails, show error card with Retry button",
        "End of day test: 5 different simple questions all answer correctly",
    ]),
    ("Day 3", "Primary Agent Pipeline", "Complex tasks run 3-stage pipeline with streaming", [
        "Add openai and anthropic packages to requirements.txt",
        "Implement Stage 1 (Research Agent): Groq call, extract JSON context",
        "Implement Stage 2 (Strategist): OpenAI GPT-4o call with stage 1 context",
        "Implement Stage 3 (Writer): Claude Sonnet 4.6 stream=True, forward SSE to browser",
        "Add stage timeout handling: 10s for stage 1, 15s for stage 2",
        "Add stage fallback: if stage fails, pass original prompt to next stage",
        "Update AgentPipeline.jsx: show 3 step cards, pulse animation on active",
        "Connect backend stage events to frontend step indicators via SSE metadata tokens",
        "Test: 'Write a business plan for a coffee shop' → all 3 stages complete → document appears",
        "Test: measure total time — should be under 12 seconds",
    ]),
    ("Day 4", "Document Storage & History", "Generated docs save to account and survive page refresh", [
        "After stream [DONE], frontend calls POST /documents to save to Supabase",
        "Implement GET /documents — paginated, returns 20 items, no full result text",
        "Implement GET /documents/{doc_id} — returns full result or edited_result",
        "Replace localStorage history with Supabase-backed GET /documents",
        "HistoryStrip.jsx: load from /documents on mount, show 5 most recent",
        "Click history item → call GET /documents/{doc_id} → display OutputCard instantly",
        "Implement DELETE /documents/{doc_id} (soft delete)",
        "Add delete button to history items",
        "Add monthly usage counter: increment user_preferences.monthly_usage on each generation",
        "Display usage counter on /account page: '12 / 50 generations used this month'",
    ]),
    ("Day 5", "Edit + Export", "User can edit output, export as PDF and DOCX", [
        "Install tiptap/react and tiptap/starter-kit",
        "Replace plain <div> in OutputCard with Tiptap editor in read-only mode",
        "Add 'Edit' button — switches editor to editable mode with visible cursor",
        "Add floating toolbar on text selection: Bold, Italic, H2, Bullet list",
        "On edit blur → call PUT /documents/{doc_id} with edited_result",
        "Add 'Reset to original' button → reload result from API, set is_edited=false",
        "Install jspdf and html2canvas (lazy import)",
        "Implement Export PDF: html2canvas on OutputCard div → jsPDF.addImage",
        "Install docx (lazy import)",
        "Implement Export DOCX: parse markdown → docx Paragraph/Heading nodes → download",
        "Test all 4 exports: Copy · Save .md · Export PDF · Export DOCX",
    ]),
    ("Day 6", "Deployment + Model Selector", "App live on Railway + Vercel, model selector works", [
        "Add backend/requirements.txt with all packages",
        "Create Railway project, connect GitHub repo, set /backend as root",
        "Add all 9 Railway environment variables",
        "Verify Railway deploy: curl https://your.railway.app/health",
        "Create Vercel project, connect GitHub repo, set /frontend as root",
        "Add VITE_API_URL env var in Vercel dashboard",
        "Update api.js: use VITE_API_URL in production, /api proxy in development",
        "Verify Vercel deploy: visit URL, green dot shows in header",
        "Build model selector dropdown in Header.jsx: Auto / Groq Fast / GPT-4o / Claude",
        "Pass selected model to /generate/stream as model param",
        "Test production end-to-end: sign up → generate → export → history",
    ]),
    ("Day 7", "Polish + QA", "App is production quality, mobile works, animations smooth", [
        "Add Framer Motion to CapabilityGrid: cards stagger fade-up on mount",
        "Add Framer Motion to AgentPipeline: steps slide in, checkmarks bounce",
        "Add Framer Motion to OutputCard: fade-scale in when document appears",
        "Test on real mobile device or Chrome 375px — fix any layout issues",
        "Add dark/light mode toggle to Header — save preference to /preferences",
        "Test all error states: bad API key → shows error card, not blank screen",
        "Run Lighthouse audit on Vercel URL — target Performance > 85",
        "Check bundle size: npm run build → check dist/assets sizes",
        "Final smoke test: 10 different prompts across all doc types",
        "Fix top 3 issues found in smoke test — ship it",
    ]),
]

for day, title, deliverable, tasks in days:
    day_header = Table(
        [[Paragraph(f"<b>{day}</b>", S('DH', fontSize=10, fontName='Helvetica-Bold',
           textColor=WHITE, alignment=TA_CENTER)),
          Paragraph(f"<b>{title}</b>", S('DT', fontSize=10.5, fontName='Helvetica-Bold',
           textColor=NAVY)),
          Paragraph(f"Deliverable: {deliverable}", S('DD', fontSize=9,
           fontName='Helvetica-Oblique', textColor=MID_GREY))]],
        colWidths=[18*mm, 50*mm, CONTENT_W - 68*mm]
    )
    day_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), NAVY),
        ('BACKGROUND', (1,0), (-1,0), CALLOUT_BG),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('LINEABOVE', (0,0), (-1,0), 2, GOLD),
    ]))
    story.append(day_header)
    for i, task in enumerate(tasks, 1):
        task_row = Table(
            [[Paragraph(f"<b>{i:02d}</b>", S('TN', fontSize=8.5,
               fontName='Helvetica-Bold', textColor=INDIGO, alignment=TA_CENTER)),
              Paragraph(f"☐  {task}", S('TR', fontSize=8.5, fontName='Helvetica',
               textColor=colors.HexColor('#2D3748'), leading=13))]],
            colWidths=[12*mm, CONTENT_W - 12*mm]
        )
        task_row.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), WHITE if i % 2 else TABLE_ALT),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, BORDER_CLR),
        ]))
        story.append(task_row)
    story.append(sp(10))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════════════════════
# 12 — TECHNICAL SUCCESS CRITERIA
# ══════════════════════════════════════════════════════════════════════════════
story += section('🎯', '12', 'Technical Success Criteria')
story.append(p(
    "The product is technically complete when ALL items below pass. "
    "Test each one manually on the production Vercel URL (not localhost)."
))
story.append(sp(6))

story += sub("Must-Pass Tests (launch blockers)")
story.append(tbl(
    ["#", "Test", "Pass Condition"],
    [
        ["01", "Health check", "GET /health → {agents_ready: true} in < 500ms"],
        ["02", "Secondary agent speed", "'What is 2+2?' → first token appears in < 2 seconds"],
        ["03", "Primary agent pipeline", "'Write a marketing plan' → all 3 agent steps complete → document appears"],
        ["04", "Real content (not demo)", "Every response is unique and relevant to the specific input"],
        ["05", "Streaming on mobile Safari", "Open on iPhone → generate → text streams word by word, no freeze"],
        ["06", "Auth persists on refresh", "Log in → generate → F5 → still logged in, history still visible"],
        ["07", "Document saves to Supabase", "Generate → check Supabase Table Editor → row exists with correct user_id"],
        ["08", "History survives refresh", "Generate → F5 → HistoryStrip shows previous generation"],
        ["09", "PDF export works", "Click Export PDF → downloads file → opens correctly in Preview/Acrobat"],
        ["10", "DOCX export works", "Click Export DOCX → downloads file → opens correctly in Word/Docs"],
        ["11", "Edit saves", "Edit output → reload history → edited text persists"],
        ["12", "Rate limit fires", "Make 11 requests/min as guest → 11th returns HTTP 429"],
        ["13", "Mobile layout", "375px width → no horizontal scroll, InputBox usable, OutputCard readable"],
        ["14", "Error state (not blank)", "Set invalid API key → generate → shows red error card, not blank screen"],
        ["15", "Model selector works", "Select 'Groq Fast' → generate complex prompt → only Groq used (check logs)"],
    ],
    col_widths_mm=[8, 52, 110]
))
story.append(sp(8))

story += sub("Nice-to-Have (post-launch)")
story.append(tbl(
    ["Item", "Pass Condition"],
    [
        ["Lighthouse Performance", "> 85 on Vercel production URL"],
        ["Framer Motion animations", "All card, pipeline, and output animations run at 60 FPS"],
        ["Dark mode", "Toggle works, preference saves to account and persists on login"],
        ["Usage counter", "Account page shows correct monthly_usage / 50"],
        ["Concurrent streams", "10 users generating simultaneously → all complete, no 503 errors"],
    ],
    col_widths_mm=[55, 115]
))
story.append(sp(6))
story.append(callout(
    "Definition of DONE: All 15 Must-Pass tests pass on the production Vercel URL, "
    "using a real Clerk account, with real LLM API keys, on both desktop Chrome and mobile Safari. "
    "If any test fails, the feature is not done — fix it before moving on."
))

# ── Build ────────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
print(f"TRD PDF saved to: {OUTPUT_PATH}")
