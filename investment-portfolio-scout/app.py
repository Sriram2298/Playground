import os
import json
import asyncio
import yfinance as yf
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

# Universe of securities to sample from
UNIVERSE = {
    "stocks": {
        "Technology": ["AAPL", "MSFT", "NVDA", "GOOGL", "META", "AMZN", "AVGO", "ORCL", "AMD", "ADBE"],
        "Healthcare": ["LLY", "UNH", "JNJ", "ABBV", "MRK", "PFE", "TMO", "ABT", "ISRG", "AMGN"],
        "Financials": ["BRK-B", "JPM", "V", "MA", "GS", "MS", "BAC", "AXP", "BLK", "SPGI"],
        "Consumer": ["COST", "HD", "MCD", "NKE", "SBUX", "TGT", "LOW", "TJX", "AMZN", "PG"],
        "Energy": ["XOM", "CVX", "COP", "EOG", "SLB", "PSX", "MPC", "VLO"],
        "Industrials": ["CAT", "HON", "UPS", "RTX", "GE", "DE", "LMT", "BA", "ETN"],
        "Real Estate": ["PLD", "AMT", "EQIX", "SPG", "O", "WELL"],
        "Communication": ["GOOGL", "META", "NFLX", "DIS", "CMCSA", "T"],
    },
    "etfs": {
        "Broad Market": ["SPY", "VTI", "IVV", "QQQ", "IWM", "VUG", "VTV"],
        "International": ["VXUS", "EFA", "VWO", "EEM", "VEA"],
        "Sector": ["XLK", "XLV", "XLF", "XLE", "XLI", "XLY", "XLP", "XLRE"],
        "Income / Dividend": ["SCHD", "VYM", "VIG", "JEPI", "HDV", "DVY"],
        "Thematic": ["CIBR", "ROBO", "WCLD", "HERO", "BOTZ", "ARKK", "ARKG"],
        "Bond / Fixed Income": ["BND", "AGG", "TLT", "IEF", "LQD", "HYG", "VCIT"],
        "Balanced": ["AOA", "AOM", "AOR", "AOK"],
    },
}


def get_market_snapshot() -> dict:
    all_tickers: dict[str, dict] = {}
    for category, sectors in UNIVERSE.items():
        for sector, tickers in sectors.items():
            for t in tickers:
                if t not in all_tickers:
                    all_tickers[t] = {"category": category, "sector": sector}

    ticker_list = list(all_tickers.keys())

    raw = yf.download(
        tickers=ticker_list,
        period="3mo",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        progress=False,
        threads=True,
    )

    results: dict[str, dict] = {}
    for ticker in ticker_list:
        try:
            hist = raw["Close"][ticker].dropna() if len(ticker_list) > 1 else raw["Close"]
            if hist.empty or len(hist) < 5:
                continue
            price_now = float(hist.iloc[-1])
            price_1m_ago = float(hist.iloc[-22]) if len(hist) >= 22 else float(hist.iloc[0])
            price_3m_ago = float(hist.iloc[0])
            results[ticker] = {
                "price": round(price_now, 2),
                "return_1m": round(((price_now - price_1m_ago) / price_1m_ago) * 100, 2),
                "return_3m": round(((price_now - price_3m_ago) / price_3m_ago) * 100, 2),
                "category": all_tickers[ticker]["category"],
                "sector": all_tickers[ticker]["sector"],
            }
        except Exception:
            continue

    snapshot: dict[str, list] = {"stocks": [], "etfs": []}
    seen: set[str] = set()
    for ticker, d in sorted(results.items(), key=lambda x: x[1].get("return_1m", -999), reverse=True):
        if ticker in seen:
            continue
        seen.add(ticker)
        entry = {
            "ticker": ticker,
            "price": d["price"],
            "return_1m_pct": d["return_1m"],
            "return_3m_pct": d["return_3m"],
            "sector": d["sector"],
        }
        if d["category"] == "stocks":
            snapshot["stocks"].append(entry)
        else:
            snapshot["etfs"].append(entry)

    snapshot["stocks"] = snapshot["stocks"][:40]
    return snapshot


SYSTEM_PROMPT = """You are a portfolio strategist assistant. Your job is to take a user's investment intent,
combined with recent real market performance data, and produce a clear, structured portfolio suggestion.

You are informational and educational — not a financial advisor. Always remind users of this.

Rules:
- No cryptocurrency. Equities, ETFs, and funds only.
- Keep it practical and grounded in the market data provided.
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


def build_user_prompt(user_input: str, snapshot: dict) -> str:
    market_context = json.dumps(snapshot, indent=2)
    return f"""User's investment intent:
\"\"\"{user_input}\"\"\"

Recent market performance data (last 1 month and 3 months returns):
{market_context}

Based on the user's intent and this real market data, produce a portfolio suggestion following the required JSON structure.
Choose 8–14 items for the portfolio. Make allocations practical and sum to exactly 100.
Prioritize securities that have performed well recently AND fit the stated strategy — do not just chase momentum blindly."""


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
        # Run yfinance (blocking) in a thread so it doesn't block the event loop
        snapshot = await asyncio.get_event_loop().run_in_executor(None, get_market_snapshot)
    except Exception as e:
        return JSONResponse({"error": f"Failed to fetch market data: {str(e)}"}, status_code=500)

    try:
        message = await client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_user_prompt(user_input, snapshot)}],
        )
        raw = message.content[0].text.strip()
        result = json.loads(raw)
        return JSONResponse({"success": True, "data": result})
    except json.JSONDecodeError:
        return JSONResponse({"error": "Model returned malformed output. Please try again."}, status_code=500)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
