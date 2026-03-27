// ── Routing map — keywords → doc type ─────────────────────
export const ROUTING_MAP = [
  {
    keywords: ['business plan','start a','launch a business','startup idea','new company','found a'],
    type: 'business_plan', label: 'Business Plan',
    audience: 'Founders & Entrepreneurs',
    agents: ['Research Agent','Fact Checker','Strategist','Financial Analyst','Writer'],
    color: '#60A5FA',
  },
  {
    keywords: ['pitch deck','investor pitch','raise funding','seed round','vc ','fundraise','pitch to'],
    type: 'pitch_deck', label: 'Pitch Deck',
    audience: 'Startup Founders',
    agents: ['Research Agent','Strategist','Writer'],
    color: '#F472B6',
  },
  {
    keywords: ['market research','analyze the market','industry analysis','market size','market report'],
    type: 'deep_market_research', label: 'Market Research',
    audience: 'Product Managers',
    agents: ['Research Agent','Fact Checker','Writer'],
    color: '#34D399',
  },
  {
    keywords: ['competitor','competitive','rivals','compare products','competitive analysis','who are my compet'],
    type: 'competitor_analysis', label: 'Competitor Analysis',
    audience: 'Business Analysts',
    agents: ['Research Agent','Fact Checker','Writer'],
    color: '#A78BFA',
  },
  {
    keywords: ['product launch','launch plan','go to market','gtm ','launch strategy','launch my product'],
    type: 'product_launch_plan', label: 'Product Launch Plan',
    audience: 'Marketing Teams',
    agents: ['Research Agent','Strategist','Writer'],
    color: '#FB923C',
  },
  {
    keywords: ['financial','projections','p&l','unit economics','revenue model','cash flow','profit'],
    type: 'financial_projections', label: 'Financial Projections',
    audience: 'Founders & Finance',
    agents: ['Research Agent','Financial Analyst','Writer'],
    color: '#4ADE80',
  },
  {
    keywords: ['youtube','video strategy','channel','video content','vlog','youtuber'],
    type: 'youtube_strategy', label: 'YouTube Strategy',
    audience: 'YouTubers',
    agents: ['Research Agent','Creative Strategist','Writer'],
    color: '#F87171',
  },
  {
    keywords: ['blog','newsletter','editorial','content calendar','article','substack'],
    type: 'blog_newsletter', label: 'Blog & Newsletter Plan',
    audience: 'Writers',
    agents: ['Research Agent','Creative Strategist','Writer'],
    color: '#FBBF24',
  },
  {
    keywords: ['social media','instagram','linkedin','twitter','posting','content for','tiktok'],
    type: 'social_media_calendar', label: 'Social Media Calendar',
    audience: 'Content Creators',
    agents: ['Research Agent','Creative Strategist','Writer'],
    color: '#38BDF8',
  },
  {
    keywords: ['study','exam prep','study plan','revision','syllabus','upsc','gate','ielts','gre','learn','course'],
    type: 'study_plan', label: 'Study Plan',
    audience: 'Students',
    agents: ['Research Agent','Personal Coach','Writer'],
    color: '#818CF8',
  },
  {
    keywords: ['career','job search','career plan','transition','skill gap','resume','interview prep'],
    type: 'career_planning', label: 'Career Plan',
    audience: 'Graduates',
    agents: ['Research Agent','Personal Coach','Writer'],
    color: '#2DD4BF',
  },
  {
    keywords: ['research paper','academic','thesis','literature review','methodology','phd','dissertation'],
    type: 'research_paper', label: 'Research Paper Outline',
    audience: 'Researchers',
    agents: ['Research Agent','Fact Checker','Writer'],
    color: '#C084FC',
  },
  {
    keywords: ['campaign','ad campaign','marketing campaign','full funnel','paid ads'],
    type: 'campaign_strategy', label: 'Campaign Strategy',
    audience: 'Marketing Agencies',
    agents: ['Research Agent','Strategist','Writer'],
    color: '#F472B6',
  },
  {
    keywords: ['proposal','scope of work','client proposal','pricing','freelance quote','deliverable'],
    type: 'proposal_pricing', label: 'Proposal & Pricing',
    audience: 'Freelancers',
    agents: ['Research Agent','Writer'],
    color: '#FB923C',
  },
  {
    keywords: ['goals','daily routine','habit','life plan','personal goals','life organization','productivity'],
    type: 'life_goals', label: 'Life Goals Plan',
    audience: 'Individuals',
    agents: ['Personal Coach','Writer'],
    color: '#F87171',
  },
  {
    keywords: ['trip','travel','itinerary','vacation','visit','tourism','packing','holiday'],
    type: 'travel_planning', label: 'Travel Itinerary',
    audience: 'Travelers',
    agents: ['Research Agent','Writer'],
    color: '#34D399',
  },
  {
    keywords: ['meal plan','recipe','weekly meals','grocery','diet','cooking','food plan'],
    type: 'cooking_meal_plan', label: 'Meal Plan',
    audience: 'Home Cooks',
    agents: ['Personal Coach','Writer'],
    color: '#FBBF24',
  },
  {
    keywords: ['client deliverable','client template','client report','agency template','standardized sop','sop document'],
    type: 'client_deliverable', label: 'Client Deliverable Template',
    audience: 'Agency Owners',
    agents: ['Research Agent','Strategist','Writer'],
    color: '#34D399',
  },
  {
    keywords: ['brainstorm','ideas','validate','ideate','think through','possibilities','generate ideas'],
    type: 'brainstorm', label: 'Brainstorm Report',
    audience: 'Everyone',
    agents: ['Research Agent','Strategist','Writer'],
    color: '#60A5FA',
  },
]

export const CAPABILITY_GRID = [
  {
    iconName: 'Rocket',    iconBg: 'rgba(96,165,250,0.12)',   iconColor: '#60A5FA',
    title: 'Build a Business Plan',        audience: 'Founders & Entrepreneurs',
    description: 'Create a comprehensive business plan with market analysis, financial projections, and go-to-market strategy.',
    outcome: 'Complete business plan document',  category: 'business',
    prompt: 'Build a business plan for a cloud kitchen startup in Tier-2 Indian cities',
  },
  {
    iconName: 'Monitor',   iconBg: 'rgba(244,114,182,0.12)',  iconColor: '#F472B6',
    title: 'Create Investor Pitch Deck',   audience: 'Startup Founders',
    description: 'Structure a compelling pitch deck with problem, solution, market size, traction, and ask slides.',
    outcome: 'Pitch deck outline & content',     category: 'business',
    prompt: 'Create an investor pitch deck for an ed-tech startup raising $500K seed',
  },
  {
    iconName: 'Search',    iconBg: 'rgba(52,211,153,0.12)',   iconColor: '#34D399',
    title: 'Deep Market Research',         audience: 'Product Managers',
    description: 'Conduct thorough market research with competitive analysis, trends, and opportunity mapping.',
    outcome: 'Research report with insights',    category: 'business',
    prompt: 'Deep market research on the electric vehicle market in India',
  },
  {
    iconName: 'Target',    iconBg: 'rgba(167,139,250,0.12)',  iconColor: '#A78BFA',
    title: 'Competitor Analysis',          audience: 'Business Analysts',
    description: 'Analyze competitors across features, pricing, positioning, and market share.',
    outcome: 'Competitive intelligence report',  category: 'business',
    prompt: 'Analyze competitors in the project management software space',
  },
  {
    iconName: 'TrendingUp', iconBg: 'rgba(251,146,60,0.12)',  iconColor: '#FB923C',
    title: 'Product Launch Plan',          audience: 'Marketing Teams',
    description: 'Create a comprehensive launch plan with timeline, channels, messaging, and success metrics.',
    outcome: 'Launch playbook & checklist',      category: 'business',
    prompt: 'Create a product launch plan for a new project management SaaS tool',
  },
  {
    iconName: 'BarChart2', iconBg: 'rgba(74,222,128,0.12)',   iconColor: '#4ADE80',
    title: 'Financial Projections',        audience: 'Founders & Finance',
    description: 'Structure revenue models, cost assumptions, and cash flow projections for your business.',
    outcome: 'Financial model structure',        category: 'business',
    prompt: 'Financial projections for a subscription SaaS product at ₹999/month',
  },
  {
    iconName: 'Video',     iconBg: 'rgba(248,113,113,0.12)',  iconColor: '#F87171',
    title: 'YouTube Content Strategy',     audience: 'YouTubers',
    description: 'Plan video concepts, script outlines, titles, and thumbnail ideas for your channel.',
    outcome: 'Video production pipeline',        category: 'creators',
    prompt: 'Create a YouTube content strategy for a personal finance channel',
  },
  {
    iconName: 'BookOpen',  iconBg: 'rgba(251,191,36,0.12)',   iconColor: '#FBBF24',
    title: 'Blog & Newsletter Planning',   audience: 'Writers',
    description: 'Develop an editorial calendar with content pillars, article outlines, and distribution strategies.',
    outcome: 'Editorial calendar',               category: 'creators',
    prompt: 'Blog and newsletter plan for a tech founder sharing startup lessons',
  },
  {
    iconName: 'Calendar',  iconBg: 'rgba(56,189,248,0.12)',   iconColor: '#38BDF8',
    title: 'Social Media Calendar',        audience: 'Content Creators',
    description: 'Generate a month of social media posts tailored to your brand voice and platform algorithms.',
    outcome: 'Social media schedule',            category: 'creators',
    prompt: '30-day social media calendar for a D2C skincare brand',
  },
  {
    iconName: 'GraduationCap', iconBg: 'rgba(129,140,248,0.12)', iconColor: '#818CF8',
    title: 'Study Plan & Exam Prep',       audience: 'Students',
    description: 'Break down syllabuses into manageable daily study schedules with revision techniques.',
    outcome: 'Structured study schedule',        category: 'students',
    prompt: 'Study plan to crack GATE exam in 4 months while working full-time',
  },
  {
    iconName: 'Briefcase', iconBg: 'rgba(45,212,191,0.12)',   iconColor: '#2DD4BF',
    title: 'Career Planning',              audience: 'Graduates',
    description: 'Map out career paths, identify skill gaps, and structure your resume and interview preparation.',
    outcome: 'Career action plan',               category: 'students',
    prompt: 'Career plan to transition from software developer to product manager',
  },
  {
    iconName: 'FileText',  iconBg: 'rgba(192,132,252,0.12)',  iconColor: '#C084FC',
    title: 'Research Paper Outline',       audience: 'Researchers',
    description: 'Structure academic papers with thesis statements, literature reviews, and methodology sections.',
    outcome: 'Academic paper framework',         category: 'students',
    prompt: 'Research paper outline on the impact of AI on healthcare diagnostics',
  },
  {
    iconName: 'ClipboardList', iconBg: 'rgba(52,211,153,0.12)', iconColor: '#34D399',
    title: 'Client Deliverable Templates', audience: 'Agency Owners',
    description: 'Structure standardized client reports, audits, and strategy documents to scale your services.',
    outcome: 'Standardized SOPs',                category: 'agencies',
    prompt: 'Create standardized client deliverable templates for a digital marketing agency',
  },
  {
    iconName: 'Users',     iconBg: 'rgba(244,114,182,0.12)',  iconColor: '#F472B6',
    title: 'Campaign Strategy',            audience: 'Marketing Agencies',
    description: 'Develop full-funnel marketing campaigns for clients across multiple channels.',
    outcome: 'Campaign strategy doc',            category: 'agencies',
    prompt: 'Develop a full-funnel marketing campaign strategy for a new fashion e-commerce brand',
  },
  {
    iconName: 'FileCheck', iconBg: 'rgba(251,146,60,0.12)',   iconColor: '#FB923C',
    title: 'Proposal & Pricing',           audience: 'Freelancers',
    description: 'Draft compelling client proposals with clear scopes of work, timelines, and tiered pricing.',
    outcome: 'Client proposal document',         category: 'freelancers',
    prompt: 'Draft a proposal and pricing for a digital marketing agency client',
  },
  {
    iconName: 'Heart',     iconBg: 'rgba(248,113,113,0.12)',  iconColor: '#F87171',
    title: 'Life Organization & Goals',    audience: 'Individuals',
    description: 'Create structured personal goals, daily routines, and habit tracking systems.',
    outcome: 'Personal planning system',         category: 'personal',
    prompt: 'Help me create a life organization plan with daily routines and personal goals',
  },
  {
    iconName: 'Plane',     iconBg: 'rgba(52,211,153,0.12)',   iconColor: '#34D399',
    title: 'Travel Planning',              audience: 'Travelers',
    description: 'Build detailed day-by-day itineraries, packing lists, and budget estimations for your trips.',
    outcome: 'Complete travel itinerary',        category: 'personal',
    prompt: 'Plan a 10-day trip to Europe for 2 people with €3000 budget',
  },
  {
    iconName: 'ChefHat',   iconBg: 'rgba(251,191,36,0.12)',   iconColor: '#FBBF24',
    title: 'Cooking & Recipe Planning',    audience: 'Home Cooks',
    description: 'Plan weekly meals based on dietary preferences, generate grocery lists, and organize recipes.',
    outcome: 'Meal plan & grocery list',         category: 'personal',
    prompt: 'Plan weekly meals for a vegetarian family of 4, including grocery list',
  },
  {
    iconName: 'Lightbulb', iconBg: 'rgba(96,165,250,0.12)',   iconColor: '#60A5FA',
    title: 'Brainstorm Ideas',             audience: 'Everyone',
    description: 'Generate and validate ideas with structured frameworks and feasibility assessments.',
    outcome: 'Validated idea framework',         category: 'general',
    prompt: 'Help me brainstorm and validate ideas for a new mobile app startup',
  },
  {
    iconName: 'MessageCircle', iconBg: 'rgba(56,189,248,0.12)', iconColor: '#38BDF8',
    title: 'Casual Conversations',         audience: 'Everyone',
    description: 'Have thoughtful conversations, get quick answers, and think through everyday decisions.',
    outcome: 'Clear, concise answers',           category: 'general',
    prompt: 'I have a question I need help thinking through',
  },
]

export const QUICK_PROMPTS = [
  { icon: '🚀', label: 'Pitch deck',         prompt: 'Build a pitch deck for an AI tutoring app for K-12 students' },
  { icon: '📅', label: 'Social calendar',    prompt: 'I need a 30-day social media calendar for my bakery' },
  { icon: '✈️', label: 'Travel plan',        prompt: 'Plan a 7-day trip to Bali with a budget of $2000' },
  { icon: '🔍', label: 'Competitor analysis',prompt: 'Create a competitive analysis of the CRM software market' },
  { icon: '📚', label: 'Study plan',         prompt: 'Study plan for UPSC exam in 6 months starting from scratch' },
  { icon: '📊', label: 'Financials',         prompt: 'Financial projections for a SaaS product charging ₹999/month' },
]

export const CATEGORY_FILTERS = [
  { key: 'all',        label: 'All',         prompt: null },
  { key: 'business',   label: 'Business',    prompt: 'I want to create a business plan for a cloud kitchen startup' },
  { key: 'creators',   label: 'Creators',    prompt: 'Build a YouTube content strategy for a travel vlog channel' },
  { key: 'students',   label: 'Students',    prompt: 'Study plan for CA Final exam in 3 months' },
  { key: 'freelancers',label: 'Freelancers', prompt: 'Write a project proposal for a web development client' },
  { key: 'personal',   label: 'Personal',    prompt: 'Help me plan a 10-day trip to Japan' },
]

// ── Sample outputs (shown in demo mode) ───────────────────
export const SAMPLE_OUTPUTS = {
  pitch_deck: `# Pitch Deck — AI Tutoring App for K-12 Students

## Slide 1 — Cover
**TutorAI** · *Personalized AI learning for every K-12 student*

---

## Slide 2 — The Problem
- 260M school children in India; only 12% have access to quality tutoring
- Average private tutor costs ₹800–2,000/hour — unaffordable for 80% of families
- Students fall behind silently; teachers have 40+ students per class
- COVID accelerated the gap — 50% of students lost foundational skills

**Speaker note:** Lead with emotion. Every parent wants their child to succeed.

---

## Slide 3 — The Solution
**TutorAI** adapts to each student's learning style and pace:
- 1-on-1 AI sessions available 24/7
- Automatically identifies gaps and fills them
- Gamified learning: 45+ min average session time
- Parent dashboard with weekly progress reports

---

## Slide 4 — Market Size
| Segment | Size |
|---------|------|
| TAM — India K-12 education | ₹4.8 lakh crore ($58B) |
| SAM — Private tutoring | ₹28,000 crore ($3.4B) |
| SOM — Year 3 target | ₹280 crore ($34M) |

---

## Slide 5 — Traction
- **12,000 beta students** across 8 cities in 90 days
- **71-minute** average daily session (3× industry average)
- **NPS: 78** from parents and students combined
- Waitlist of **45,000 students**

---

## Slide 6 — Business Model
| Plan | Price | Target |
|------|-------|--------|
| Basic | ₹299/month | Tier-2/3 cities |
| Pro | ₹599/month | Urban families |
| School | ₹49/student/month | B2B schools |

**Blended ARPU: ₹420/month · Gross margin: 78%**

---

## Slide 7 — The Ask
**Raising ₹4.2 crore ($500K) Seed**

- 45% — Engineering & AI model fine-tuning
- 30% — Growth & marketing (Tier-2 cities)
- 15% — Content & curriculum
- 10% — Operations

**Target: 50,000 paying students by Month 18 = ₹2.5Cr ARR**`,

  social_media_calendar: `# 30-Day Social Media Calendar — Bakery Brand

## Strategy
**Platforms:** Instagram (primary) · Facebook (secondary)
**Frequency:** 7×/week Instagram · 4×/week Facebook
**Content ratio:** 40% educational · 30% product · 20% BTS · 10% community

---

## Week 1 — Theme: "The Art of Baking"

**Day 1 (Mon) — Reel**
Caption: *"We wake up at 3am so your croissants are flaky by 7am ☀️ Behind the scenes of our morning."*
Visual: 30-sec time-lapse of croissant lamination
Hashtags: #bakery #freshbread #artisanbakery #croissant

**Day 2 (Tue) — Carousel**
Caption: *"5 signs your sourdough starter is ready 🍞 Save this!"*
Visual: 5-slide infographic, clean design · **Educational — builds saves**

**Day 3 (Wed) — Story Poll**
"Which new flavour for this weekend?"
🌹 Pistachio rose croissant **vs** 🥭 Mango cardamom danish

**Day 4 (Thu) — Product Showcase**
Caption: *"Our almond tart: 100% French almond flour, zero shortcuts. Pre-order: link in bio 🥐"*

**Day 5 (Fri) — Behind the Scenes**
Caption: *"Meet Priya, decorating cakes for 4 years. Every flower is hand-piped 🌸"*

**Day 6 (Sat) — Weekend Drop**
Caption: *"12 varieties, baked fresh this morning. Pickup from 8am 🧁"*

**Day 7 (Sun) — Community UGC**
Caption: *"Nothing better than seeing your baking attempts 💛 Tag us!"*

---

## Weeks 2–4
| Week | Theme | Focus |
|------|-------|-------|
| Week 2 | Ingredients Transparency | Where we source, what makes us different |
| Week 3 | Celebrating Occasions | Birthdays, weddings, corporate orders |
| Week 4 | Community & Favourites | Top posts, fan favourites, milestones |

---

## KPIs
- Reach per post: target 3× follower count
- Story views: target 40% of followers
- Link clicks (orders): target 2% of reach`,

  travel_planning: `# 7-Day Bali Travel Plan — Budget $2,000

## Overview
**Base:** Seminyak (Days 1–3) → Ubud (Days 4–5) → Uluwatu (Days 6–7)
**Best time to visit:** May–October (dry season)

## Budget Breakdown
| Category | Budget |
|----------|--------|
| Accommodation (7 nights) | $280 |
| Food & drink | $210 |
| Transport | $110 |
| Activities & entry fees | $150 |
| Shopping & misc | $80 |
| **Total (excl. flights)** | **$830** |
| Remaining for flights/buffer | $1,170 |

---

## Day-by-Day Itinerary

**Day 1 — Arrival & Seminyak**
- Land at Ngurah Rai → Grab taxi to Seminyak (~$8, 40 min)
- Get SIM card at airport: Telkomsel, $5 for 10GB
- Sunset walk at Seminyak Beach (free)
- Dinner at Mama San: budget $15–20pp

**Day 2 — Temples & Beach Clubs**
- Tanah Lot Temple at sunrise (fewer crowds, $3 entry)
- Potato Head Beach Club (free entry, pay for drinks)
- Sunset at La Plancha — colourful bean bag beach

**Day 3 — Canggu**
- Scooter rental $7/day → drive to Echo Beach
- Old Man's bar for sunset cocktails
- Explore Seminyak Square market

**Day 4 — Move to Ubud · Sacred Monkey Forest**
- Grab taxi Seminyak → Ubud ($15, 1.5 hours)
- Sacred Monkey Forest ($5) — arrive early
- Tegalalang Rice Terraces ($2 entry + $3 swing)
- Ubud night market dinner: $5–8/meal

**Day 5 — Waterfall & Cooking Class**
- Tegenungan Waterfall ($2 entry)
- Balinese cooking class: $25–35, includes market + 5-course meal
- Kecak Fire Dance at Uluwatu Temple ($12)

**Day 6 — Uluwatu Cliffs**
- Uluwatu cliff temple ($3 entry)
- Padang Padang Beach ($2 entry)
- Single Fin bar — legendary sunset spot

**Day 7 — Final Day**
- Sunrise at Bingin Beach
- Last shopping at local markets
- Airport transfer & fly home

---

## Packing List
✅ Lightweight clothes (28–32°C) · ✅ Sarong (buy locally, $3 — required for temples)
✅ Reef-safe sunscreen · ✅ Portable charger · ✅ Cash (Rupiah) + card`,

  default: null,
}

// ── Classify user input ────────────────────────────────────
export function classifyInput(input) {
  const lower = input.toLowerCase()
  for (const route of ROUTING_MAP) {
    if (route.keywords.some(kw => lower.includes(kw))) return route
  }
  return {
    type: 'casual_chat', label: 'Quick Answer',
    audience: 'Everyone',
    agents: ['Writer'],
    color: '#E8C547',
  }
}
