"""
PM Copilot — structured product analysis
- Example chips: pre-baked, no API key needed
- Textarea submit: powered by Claude
"""
import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="PM Copilot")
claude = Anthropic()


SYSTEM_PROMPT = """You are an experienced Product Manager and startup advisor. Analyze the product idea and return a structured PM analysis.

Return ONLY a valid JSON object — no markdown fences, no extra text:
{
  "scores": [
    {"label": "Clarity of Problem", "score": <1-10>, "rationale": "one sentence"},
    {"label": "Differentiation",    "score": <1-10>, "rationale": "one sentence"},
    {"label": "Feasibility",        "score": <1-10>, "rationale": "one sentence"}
  ],
  "verdict": "2-3 sentence direct assessment. Be honest and specific — not generic.",
  "sections": [
    {"title": "1. Problem Statement",    "body": "..."},
    {"title": "2. Target Users",         "body": "..."},
    {"title": "3. Core Use Cases",       "body": "..."},
    {"title": "4. Solution Approach",    "body": "..."},
    {"title": "5. Risks & Failure Modes","body": "..."},
    {"title": "6. Assumptions",          "body": "..."},
    {"title": "7. Success Metrics",      "body": "..."},
    {"title": "8. Edge Cases",           "body": "..."},
    {"title": "9. MVP Scope",            "body": "..."},
    {"title": "10. Suggested Next Steps","body": "..."}
  ]
}

For section bodies use plain text with:
- **double asterisks** for bold
- Lines starting with "- " for bullet lists
- Lines starting with "1. " etc for numbered lists
Be specific to the idea described. Avoid generic advice."""


class Idea(BaseModel):
    idea: str


@app.post("/analyze-live")
async def analyze_live(body: Idea):
    idea = body.idea.strip()
    if not idea:
        return JSONResponse({"error": "Please describe your product idea."}, status_code=400)
    if len(idea) > 3000:
        return JSONResponse({"error": "Input too long. Keep it under 3000 characters."}, status_code=400)
    try:
        message = claude.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Product idea:\n{idea}"}],
        )
        raw = message.content[0].text.strip()
        result = json.loads(raw)
        result["_live"] = True
        return JSONResponse(result)
    except json.JSONDecodeError:
        return JSONResponse({"error": "Model returned malformed output. Please try again."}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PM Copilot</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #0f1117; color: #e2e8f0;
  min-height: 100vh; padding: 40px 16px 64px;
}
.header { text-align: center; margin-bottom: 32px; }
h1 { font-size: 1.45rem; font-weight: 700; color: #a78bfa; letter-spacing: -0.3px; margin-bottom: 4px; }
.subtitle { font-size: 0.83rem; color: #64748b; }
.container { max-width: 760px; margin: 0 auto; }

/* Examples strip */
.examples-label {
  font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.08em; color: #4b5563; margin-bottom: 8px;
}
.example-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px; }
.chip {
  background: #1a1d2e; border: 1.5px solid #2d3148;
  color: #94a3b8; padding: 7px 14px; border-radius: 20px;
  font-size: 0.8rem; cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
}
.chip:hover { border-color: #7c3aed; color: #c4b5fd; }
.chip.active { border-color: #7c3aed; color: #c4b5fd; background: #1e1a3a; }

/* Divider */
.divider {
  display: flex; align-items: center; gap: 10px;
  font-size: 0.72rem; color: #374151; margin-bottom: 20px;
}
.divider::before, .divider::after { content:''; flex:1; height:1px; background:#1e2130; }

/* Input card */
.input-card {
  background: #1e2130; border: 1px solid #2d3148;
  border-radius: 10px; padding: 20px; margin-bottom: 16px;
}
.input-label {
  display: block; font-size: 0.75rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.06em;
  color: #64748b; margin-bottom: 10px;
}
textarea {
  width: 100%; min-height: 120px; background: #161926;
  border: 1px solid #2d3148; color: #e2e8f0;
  padding: 12px 14px; border-radius: 8px;
  font-size: 0.9rem; font-family: inherit;
  resize: vertical; line-height: 1.6; outline: none;
  transition: border-color 0.15s;
}
textarea:focus { border-color: #7c3aed; }
textarea::placeholder { color: #4b5563; }
.input-footer {
  display: flex; justify-content: space-between;
  align-items: center; margin-top: 10px; gap: 10px;
}
.input-hint { font-size: 0.72rem; color: #374151; }
button.submit-btn {
  background: #7c3aed; color: #fff; border: none;
  padding: 9px 22px; border-radius: 8px;
  font-size: 0.88rem; font-weight: 600;
  cursor: pointer; transition: background 0.15s;
  display: flex; align-items: center; gap: 7px; white-space: nowrap;
}
button.submit-btn:hover:not(:disabled) { background: #6d28d9; }
button.submit-btn:disabled { background: #374151; cursor: default; }
.btn-spinner {
  width: 14px; height: 14px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff; border-radius: 50%;
  animation: spin 0.7s linear infinite; display: none;
}
@keyframes spin { to { transform: rotate(360deg); } }
button.submit-btn.loading .btn-spinner { display: block; }
button.submit-btn.loading .btn-label { display: none; }

/* Result banner */
.result-banner {
  display: none;
  background: #1a1d2e; border: 1px solid #2d3148;
  border-left: 3px solid #7c3aed;
  border-radius: 0 8px 8px 0;
  padding: 8px 14px; font-size: 0.75rem; color: #6b6f9e;
  align-items: center; gap: 8px; margin-bottom: 16px;
}
.result-banner.visible { display: flex; }
.banner-dot { width: 6px; height: 6px; background: #7c3aed; border-radius: 50%; flex-shrink: 0; }

/* Error */
.error-box {
  background: #1f1212; border: 1px solid #4c1d1d;
  border-radius: 8px; padding: 12px 16px;
  color: #f87171; font-size: 0.85rem;
  margin-bottom: 16px; display: none;
}
.error-box.visible { display: block; }

/* Output */
#output { display: none; animation: fadeIn 0.25s ease; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

.eval-card {
  background: #1e2130; border: 1px solid #2d3148;
  border-radius: 10px; padding: 20px 24px; margin-bottom: 12px;
}
.eval-title { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 14px; }
.scores { display: flex; flex-direction: column; gap: 10px; margin-bottom: 16px; }
.score-row { display: flex; align-items: baseline; gap: 12px; }
.score-lbl { font-size: 0.82rem; color: #94a3b8; min-width: 165px; }
.score-num { font-size: 0.9rem; font-weight: 700; min-width: 36px; text-align: right; }
.score-rat { font-size: 0.78rem; color: #64748b; flex: 1; line-height: 1.5; }
.green { color: #4ade80; } .amber { color: #fbbf24; } .red { color: #f87171; }
.verdict { border-top: 1px solid #2d3148; padding-top: 14px; }
.verdict-lbl { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #7c3aed; margin-bottom: 6px; }
.verdict p { font-size: 0.85rem; color: #cbd5e1; line-height: 1.7; }

.sections { display: flex; flex-direction: column; gap: 10px; }
.sec {
  background: #1e2130; border: 1px solid #2d3148;
  border-left: 3px solid #7c3aed;
  border-radius: 0 10px 10px 0; padding: 16px 20px;
}
.sec-title { font-size: 0.85rem; font-weight: 700; color: #e2e8f0; margin-bottom: 10px; }
.sec-body { font-size: 0.82rem; color: #94a3b8; line-height: 1.7; }
.sec-body p  { margin: 5px 0; }
.sec-body ul, .sec-body ol { padding-left: 18px; margin: 6px 0; }
.sec-body li { margin: 4px 0; }
.sec-body strong { color: #e2e8f0; font-weight: 600; }
</style>
</head>
<body>

<div class="header">
  <h1>PM Copilot</h1>
  <p class="subtitle">Paste a product idea. Get a structured PM analysis.</p>
</div>

<div class="container">

  <!-- Examples -->
  <div class="examples-label">Example outputs — click to preview</div>
  <div class="example-chips">
    <span class="chip" id="chip-freelancer"  onclick="showExample('freelancer')">🧾 Freelancer invoicing tool</span>
    <span class="chip" id="chip-marketplace" onclick="showExample('marketplace')">🏠 Contractor marketplace</span>
    <span class="chip" id="chip-ai_tool"     onclick="showExample('ai_tool')">🤖 AI spec generator</span>
  </div>

  <div class="divider">or describe your own idea below</div>

  <!-- Input -->
  <div class="input-card">
    <label class="input-label" for="idea">Your product idea</label>
    <textarea id="idea" placeholder="What does it do, who is it for, and what problem does it solve?"></textarea>
    <div class="input-footer">
      <span class="input-hint">Cmd+Enter to submit · Requires API key for live analysis</span>
      <button class="submit-btn" id="submit-btn" onclick="submitLive()">
        <div class="btn-spinner"></div>
        <span class="btn-label">Analyze</span>
      </button>
    </div>
  </div>

  <!-- Result banner -->
  <div class="result-banner" id="result-banner">
    <div class="banner-dot"></div>
    <span id="banner-text">Example output — pre-generated to illustrate the product. Live analysis is generated by Claude based on your specific idea.</span>
  </div>

  <!-- Error -->
  <div class="error-box" id="error-box"></div>

  <!-- Output -->
  <div id="output">
    <div id="inner"></div>
  </div>

</div>

<script>
// ── Pre-baked example analyses ─────────────────────────────────────────────
const ANALYSES = {
  freelancer: {
    scores: [
      {label:"Clarity of Problem", score:7, rationale:"Pain is real and measurable, but stated at category level — 'admin overhead' needs sharper specificity"},
      {label:"Differentiation",    score:4, rationale:"Harvest, Toggl, FreshBooks, Bonsai all own this space — no wedge identified"},
      {label:"Feasibility",        score:8, rationale:"CRUD + PDF generation is technically straightforward; the hard problem is distribution"}
    ],
    verdict: "The problem is genuinely painful — freelancers do lose hours to admin. But this is one of the most saturated SMB SaaS categories. Without a clear answer to why someone switches from what they already use, you're building into a headwind. Viable only with a specific niche angle.",
    sections: [
      {title:"1. Problem Statement",    body:"Freelancers doing project-based work lose 2–4 hours/week to admin: logging hours, calculating totals, formatting invoices, chasing payment. Many under-bill or delay invoicing — directly cutting income they've already earned."},
      {title:"2. Target Users",         body:"<strong>Primary:</strong> Independent designers and developers earning $60–150k/yr with 3–8 concurrent clients.<br><strong>Secondary:</strong> Small creative agencies (2–5 people) where the owner is also the primary biller.<br><br><strong>Key characteristics:</strong><ul><li>Work across multiple clients with different rates and budget caps</li><li>Currently on spreadsheets or a free tool tier they've outgrown</li><li>Delay invoicing because the process feels tedious</li></ul>"},
      {title:"3. Core Use Cases",       body:"<ul><li><strong>Timer capture:</strong> Start/stop a running timer against a project in the moment</li><li><strong>Invoice generation:</strong> One click to produce a PDF invoice from all logged hours in a period</li><li><strong>AR tracking:</strong> See outstanding invoices by client — sent, overdue, paid</li><li><strong>Budget alerts:</strong> Surface when a fixed-price project is burning toward the cap</li></ul>"},
      {title:"4. Solution Approach",    body:"A tight loop — timer → logged hours → invoice — with zero manual re-entry. Every minute logged is already tagged to a client and rate, so invoice generation is a button press, not a rebuild.<br><br><strong>Key decisions:</strong><ul><li>Mobile timer is non-negotiable — time gets logged in the moment, not at a desktop later</li><li>White-label invoices matter to users who want to look professional</li></ul>"},
      {title:"5. Risks & Failure Modes",body:"<ul><li><strong>Incumbent stickiness:</strong> Freelancers in Harvest or Toggl have years of history. Switching rarely happens from slightly better UX alone.</li><li><strong>Feature parity trap:</strong> Pressure to add expense tracking, retainer billing before the core loop is proven</li><li><strong>Low engagement between projects:</strong> No active project = no reason to open the app</li><li><strong>Price sensitivity:</strong> Freelancers spending &lt;$20/mo on tools are a hard sell</li></ul>"},
      {title:"6. Assumptions",          body:"<ul><li>Users want one tool for time tracking AND invoicing — if wrong, you compete on two fronts</li><li>Users will actively log time rather than reconstruct it — if wrong, invoice accuracy suffers</li><li>PDF is the right output — if clients want QuickBooks sync, you need integrations on day one</li></ul>"},
      {title:"7. Success Metrics",      body:"<ul><li><strong>Invoice sent within 48h of period end:</strong> &gt;70%</li><li><strong>Week-4 retention:</strong> &gt;50%</li><li><strong>Hours logged per active user per week:</strong> &gt;4h</li><li><strong>Free-to-paid conversion in 30 days:</strong> &gt;8%</li></ul>"},
      {title:"8. Edge Cases",           body:"<ul><li><strong>Mixed billing models:</strong> Hourly and fixed-price projects simultaneously — data model must handle both</li><li><strong>Disputed hours:</strong> Client disputes 3 hours — need a per-entry audit trail, not just a total</li><li><strong>Project overruns:</strong> Must surface proactively, not after the invoice is sent</li></ul>"},
      {title:"9. MVP Scope",            body:"<strong>Must have:</strong><ul><li>Project creation with client name, hourly rate, optional budget cap</li><li>Running timer + manual time entry per project</li><li>One-click PDF invoice from logged hours in a date range</li><li>Invoice status: draft / sent / paid</li></ul><strong>Out of scope for v1:</strong><ul><li>Expense tracking</li><li>In-app payment collection</li><li>Multi-seat features</li></ul>"},
      {title:"10. Suggested Next Steps",body:"<ol><li><strong>Interview 8–10 freelancers on spreadsheets</strong> — find the exact moment invoicing feels most painful</li><li><strong>Map what triggers people to leave Harvest/Toggl</strong> — switching only happens when something breaks</li><li><strong>Ship the timer → invoice loop in 2 weeks</strong></li><li><strong>Price test at $9/mo vs $15/mo</strong> — validate willingness to pay before investing in growth</li></ol>"}
    ]
  },
  marketplace: {
    scores: [
      {label:"Clarity of Problem", score:6, rationale:"Friction on both sides is identifiable, but which side has the more acute pain is unclear"},
      {label:"Differentiation",    score:5, rationale:"Most marketplace niches have an incumbent — better UX is not a differentiation strategy"},
      {label:"Feasibility",        score:4, rationale:"Platform is buildable; cold-starting two-sided demand is the hard problem, not the engineering"}
    ],
    verdict: "Two-sided marketplaces are among the hardest products to cold-start. This needs a concrete answer to the chicken-and-egg problem before anything else: what brings the first 50 suppliers, and what guarantees enough demand to keep them? Without that, this is a planning exercise, not a product.",
    sections: [
      {title:"1. Problem Statement",    body:"There is friction on both sides: homeowners can't easily find vetted contractors, and contractors spend time on unpredictable lead generation. The market is fragmented — transactions happen through referrals — making quality and pricing opaque."},
      {title:"2. Target Users",         body:"<strong>Primary (demand):</strong> Homeowners planning renovations who prioritise trust over price.<br><strong>Primary (supply):</strong> Contractors with excess capacity who rely on word-of-mouth and want a consistent lead source.<br><br><strong>Key characteristics:</strong><ul><li>Trust is the core product — one bad supplier experience kills NPS early</li><li>Contractors must see ROI within 30 days or they stop responding to leads</li></ul>"},
      {title:"3. Core Use Cases",       body:"<ul><li><strong>Search and match:</strong> Homeowner describes a job; platform surfaces contractors with reviews</li><li><strong>Quote request:</strong> Homeowner sends job details; contractor responds on-platform</li><li><strong>Job tracking:</strong> Both parties track milestones in one place</li><li><strong>Review:</strong> Post-job review closes the trust loop for future buyers</li></ul>"},
      {title:"4. Solution Approach",    body:"Curated supply side (invite-only initially) combined with low-friction demand. Do not launch an open marketplace — curation is how you guarantee quality and win the first reviews.<br><br><strong>Key decisions:</strong><ul><li>Managed supply vs. open listing — managed is slower but produces better early reviews</li><li>Take rate vs. subscription — take rate aligns incentives but requires high GMV</li></ul>"},
      {title:"5. Risks & Failure Modes",body:"<ul><li><strong>Chicken-and-egg:</strong> No buyers without supply; no supply without buyers</li><li><strong>Disintermediation:</strong> Buyer and contractor connect once, then transact off-platform</li><li><strong>Low transaction frequency:</strong> Renovations happen once every few years — retention is structurally low</li><li><strong>Supply concentration:</strong> If 3 contractors drive 80% of jobs, losing one is a crisis</li></ul>"},
      {title:"6. Assumptions",          body:"<ul><li>Homeowners will pay a premium for trust/vetting — if wrong, they just Google and call directly</li><li>You can recruit supply before demand exists — key sequencing assumption</li><li>The job value is high enough to support a take rate</li></ul>"},
      {title:"7. Success Metrics",      body:"<ul><li><strong>Supplier first transaction within 14 days of joining</strong></li><li><strong>Repeat buyer rate within 18 months:</strong> &gt;25%</li><li><strong>Disintermediation rate:</strong> &lt;15% of matches</li><li><strong>GMV per active supplier per month</strong></li></ul>"},
      {title:"8. Edge Cases",           body:"<ul><li><strong>No-shows:</strong> Contractor accepts a job and doesn't show — need a policy before the first transaction</li><li><strong>Dispute resolution:</strong> Homeowner says work wasn't finished; contractor says it was — you're the adjudicator</li><li><strong>Off-platform contact:</strong> Need design to disincentivise this from message #1</li></ul>"},
      {title:"9. MVP Scope",            body:"<strong>Must have:</strong><ul><li>Contractor profile with photos, reviews, trade type</li><li>Homeowner job posting with location, scope, budget range</li><li>On-platform messaging and quote flow</li><li>Post-job review on both sides</li></ul><strong>Out of scope for v1:</strong><ul><li>In-app payments</li><li>Automated matching algorithm</li><li>Mobile app</li></ul>"},
      {title:"10. Suggested Next Steps",body:"<ol><li><strong>Recruit 20 contractors in one city manually</strong> — before building anything</li><li><strong>Run 10 jobs as a concierge MVP</strong> — match via email first; find the friction before encoding it</li><li><strong>Define unit economics first</strong> — what take rate covers CAC?</li><li><strong>Pick one trade type and one city</strong> — broad launch with thin supply fails</li></ol>"}
    ]
  },
  ai_tool: {
    scores: [
      {label:"Clarity of Problem", score:6, rationale:"Workflow problem is real, but 'AI for X' describes a mechanism — the specific pain needs sharper articulation"},
      {label:"Differentiation",    score:5, rationale:"Every PM tool now has an AI spec feature — 'why not ChatGPT' is the unanswered question"},
      {label:"Feasibility",        score:7, rationale:"LLM integration is fast; the hard parts are output quality, prompt reliability, and D7 retention"}
    ],
    verdict: "AI as a feature is table stakes in 2025. The question is whether the workflow is 10x better than pasting the same brief into ChatGPT. If the honest answer is 'not much, but more convenient,' that's a thin moat. The product needs workflow lock-in, not just an AI wrapper.",
    sections: [
      {title:"1. Problem Statement",    body:"PMs writing product specs spend 2–3 hours on a document that mostly follows the same structure every time. The first draft is the hardest part. An AI that generates a structured spec from a one-line brief could compress that to minutes — but only if output quality is high enough to be used, not just admired."},
      {title:"2. Target Users",         body:"<strong>Primary:</strong> PMs at startups who write 2–5 specs per month and are comfortable editing AI output.<br><strong>Secondary:</strong> Engineering leads who need spec-like documents but don't have a dedicated PM.<br><br><strong>Key characteristics:</strong><ul><li>Write specs frequently enough that the time saving compounds</li><li>Know what a good spec looks like — they'll edit, not just accept output</li><li>Currently using Notion with a blank page and a template</li></ul>"},
      {title:"3. Core Use Cases",       body:"<ul><li><strong>Spec from brief:</strong> PM types one paragraph; AI generates a full structured spec</li><li><strong>Section regeneration:</strong> PM keeps 80% and regenerates a weak section without redoing the whole doc</li><li><strong>Export:</strong> Output lands in Notion, Linear, or Confluence — not just a text box</li></ul>"},
      {title:"4. Solution Approach",    body:"Structured input form (not freeform chat) feeds a domain-tuned prompt that produces consistent output. The product's edge is the structure it imposes on both input and output.<br><br><strong>Key decisions:</strong><ul><li>Form-based input vs. chat — forms produce consistent output; chat is flexible but lower quality</li><li>Integration as core feature — if output is just text, there's no reason not to use ChatGPT</li></ul>"},
      {title:"5. Risks & Failure Modes",body:"<ul><li><strong>ChatGPT is good enough:</strong> If users get 80% of the value from a ChatGPT prompt, the switching cost isn't worth it</li><li><strong>One-and-done usage:</strong> Users try it once, find it impressive, never return</li><li><strong>Prompt commoditisation:</strong> Prompts are not a moat — workflow and integrations are</li><li><strong>Model updates break output:</strong> LLM providers change models silently; output format changes without warning</li></ul>"},
      {title:"6. Assumptions",          body:"<ul><li>PMs will trust AI output enough to use it with light editing — if heavy rewriting is always required, time savings disappear</li><li>The structured input form is better than free prompting — test against ChatGPT directly</li><li>Spec writing is frequent enough to justify a dedicated tool</li></ul>"},
      {title:"7. Success Metrics",      body:"<ul><li><strong>D7 retention:</strong> &gt;30% — AI tools have great D1, terrible D7; this is the critical benchmark</li><li><strong>Output acceptance rate:</strong> &gt;60% of specs used with &lt;20% editing</li><li><strong>Time-to-spec:</strong> &lt;5 minutes from brief to usable draft</li><li><strong>Week-4 WAU / total signups:</strong> &gt;25%</li></ul>"},
      {title:"8. Edge Cases",           body:"<ul><li><strong>Vague input:</strong> 'Improve the dashboard' — AI generates generic output; need input quality guardrails</li><li><strong>Sensitive product details:</strong> Users paste unreleased roadmap items — data handling must be explicit</li><li><strong>Team disagreement:</strong> PM uses AI spec; engineering team rejects it as too vague</li></ul>"},
      {title:"9. MVP Scope",            body:"<strong>Must have:</strong><ul><li>Structured input: product name, one-line brief, target user, key problem</li><li>AI-generated spec with fixed sections</li><li>Regenerate individual sections</li><li>Copy full spec to clipboard</li></ul><strong>Out of scope for v1:</strong><ul><li>Notion/Confluence integration</li><li>Team collaboration</li><li>Custom templates</li></ul>"},
      {title:"10. Suggested Next Steps",body:"<ol><li><strong>Run the ChatGPT comparison test with 10 PMs</strong> — same brief in both; measure quality difference</li><li><strong>Find one PM who writes specs weekly</strong> — build for them specifically first</li><li><strong>Ship the single input → spec flow in 1 week</strong></li><li><strong>Measure D1/D7 retention from week one</strong></li></ol>"}
    ]
  }
};

// ── Markdown → HTML converter (for live Claude output) ─────────────────────
function mdToHtml(text) {
  if (!text) return '';
  let html = text.replace(/[*][*](.*?)[*][*]/g, '<strong>$1</strong>');
  const lines = html.split('\\n');
  let result = '', inUl = false, inOl = false;
  for (const line of lines) {
    const t = line.trim();
    if (!t) {
      if (inUl) { result += '</ul>'; inUl = false; }
      if (inOl) { result += '</ol>'; inOl = false; }
      continue;
    }
    const olM = t.match(/^(\\d+)\\.\\s+(.+)/);
    if (t.startsWith('- ') || t.startsWith('• ')) {
      if (inOl) { result += '</ol>'; inOl = false; }
      if (!inUl) { result += '<ul>'; inUl = true; }
      result += `<li>${t.replace(/^[-•]\\s+/, '')}</li>`;
    } else if (olM) {
      if (inUl) { result += '</ul>'; inUl = false; }
      if (!inOl) { result += '<ol>'; inOl = true; }
      result += `<li>${olM[2]}</li>`;
    } else {
      if (inUl) { result += '</ul>'; inUl = false; }
      if (inOl) { result += '</ol>'; inOl = false; }
      result += `<p>${t}</p>`;
    }
  }
  if (inUl) result += '</ul>';
  if (inOl) result += '</ol>';
  return result;
}

// ── Render ──────────────────────────────────────────────────────────────────
function renderAnalysis(data, isLive) {
  const sc = n => n >= 7 ? 'green' : n >= 5 ? 'amber' : 'red';
  let html = '<div class="eval-card"><div class="eval-title">Quick Evaluation</div><div class="scores">';
  for (const s of data.scores) {
    html += `<div class="score-row">
      <span class="score-lbl">${esc(s.label)}</span>
      <span class="score-num ${sc(s.score)}">${s.score}/10</span>
      <span class="score-rat">${esc(s.rationale)}</span>
    </div>`;
  }
  html += `</div><div class="verdict"><div class="verdict-lbl">Verdict</div><p>${esc(data.verdict)}</p></div></div>`;
  html += '<div class="sections">';
  for (const sec of data.sections) {
    const body = isLive ? mdToHtml(sec.body) : sec.body;
    html += `<div class="sec"><div class="sec-title">${esc(sec.title)}</div><div class="sec-body">${body}</div></div>`;
  }
  html += '</div>';
  document.getElementById('inner').innerHTML = html;
  document.getElementById('output').style.display = 'block';
}

// ── Example loader ──────────────────────────────────────────────────────────
function showExample(key) {
  ['freelancer','marketplace','ai_tool'].forEach(k => {
    document.getElementById('chip-' + k).classList.toggle('active', k === key);
  });
  hideError();
  setBanner("Example output — pre-generated to illustrate the product. Live analysis is generated by Claude based on your specific idea.");
  renderAnalysis(ANALYSES[key], false);
}

// ── Live submit ─────────────────────────────────────────────────────────────
async function submitLive() {
  const idea = document.getElementById('idea').value.trim();
  if (!idea) { showError('Please describe your product idea before submitting.'); return; }

  ['freelancer','marketplace','ai_tool'].forEach(k => {
    document.getElementById('chip-' + k).classList.remove('active');
  });
  hideBanner();
  hideError();
  setLoading(true);
  document.getElementById('output').style.display = 'none';

  try {
    const res  = await fetch('/analyze-live', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({idea}),
    });
    const data = await res.json();
    if (data.error) {
      showError(data.error);
    } else {
      renderAnalysis(data, true);
    }
  } catch(e) {
    showError('Network error. Is the server running?');
  } finally {
    setLoading(false);
  }
}

function setLoading(on) {
  const btn = document.getElementById('submit-btn');
  btn.disabled = on;
  btn.classList.toggle('loading', on);
}
function setBanner(msg) {
  document.getElementById('banner-text').textContent = msg;
  document.getElementById('result-banner').classList.add('visible');
}
function hideBanner() { document.getElementById('result-banner').classList.remove('visible'); }
function showError(msg) {
  const el = document.getElementById('error-box');
  el.textContent = msg; el.classList.add('visible');
}
function hideError() { document.getElementById('error-box').classList.remove('visible'); }
function esc(s) {
  return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// Cmd/Ctrl+Enter to submit
document.getElementById('idea').addEventListener('keydown', e => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') submitLive();
});
</script>
</body>
</html>"""
