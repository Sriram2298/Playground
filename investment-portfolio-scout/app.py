import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = AsyncAnthropic()
templates = Jinja2Templates(directory="templates")


SYSTEM_PROMPT = """You are a portfolio strategist assistant. Your job is to take a user's investment intent and produce a clear, structured portfolio suggestion.

You are informational and educational — not a financial advisor. Always remind users of this.

Use your knowledge of equities, ETFs, and funds to suggest a well-reasoned portfolio. Draw on your understanding of:
- Current market conditions and sector dynamics
- Historical performance characteristics of major indices, ETFs, and stocks
- Risk/return profiles appropriate to the stated strategy

Rules:
- No cryptocurrency. Equities, ETFs, and funds only.
- If user input is vague, infer sensible defaults and state them clearly.
- Be calm and credible — not hypey or trader-bro.
- Allocations should sum to 100%.

You MUST respond with a valid JSON object matching this exact structure:
{
  "strategy_summary": {
    "time_horizon": "string",
    "risk_appetite": "string",
    "key_assumptions": ["string", ...]
  },
  "portfolio": [
    {
      "name": "string",
      "ticker": "string",
      "category": "stock | ETF | fund",
      "industry_theme": "string",
      "why_it_fits": "string",
      "allocation_pct": number
    }
  ],
  "industry_view": [
    {
      "industry": "string",
      "weight_pct": number,
      "rationale": "string"
    }
  ],
  "risk_notes": {
    "concentration_risks": ["string", ...],
    "time_horizon_risks": ["string", ...],
    "volatility_notes": ["string", ...]
  },
  "rebalancing_notes": {
    "frequency": "string",
    "what_to_watch": ["string", ...]
  },
  "disclaimer": "string"
}

Respond with JSON only. No markdown fences, no extra text."""


def build_user_prompt(user_input: str) -> str:
    return f"""User's investment intent:
\"\"\"{user_input}\"\"\"

Produce a portfolio suggestion following the required JSON structure.
Choose 8–14 items. Make allocations practical and sum to exactly 100.
Be specific and grounded — reference real tickers and explain concisely why each fits the strategy."""


class UserInput(BaseModel):
    input: str


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/suggest")
async def suggest(body: UserInput):
    user_input = body.input.strip()
    if not user_input:
        return JSONResponse({"error": "Please describe what you're looking for."}, status_code=400)
    if len(user_input) > 2000:
        return JSONResponse({"error": "Input too long. Please keep it under 2000 characters."}, status_code=400)

    try:
        message = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_user_prompt(user_input)}],
        )
        raw = message.content[0].text.strip()
        result = json.loads(raw)
        return JSONResponse({"success": True, "data": result})
    except json.JSONDecodeError:
        return JSONResponse({"error": "Model returned malformed output. Please try again."}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
