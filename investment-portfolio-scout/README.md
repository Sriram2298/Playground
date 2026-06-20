# Portfolio Scout

An AI-powered stock and ETF discovery tool. Describe your investment goals in plain language — risk tolerance, time horizon, sector preferences, or just a general intent — and get back a structured portfolio suggestion grounded in recent market performance.

The output is designed to feel like a considered recommendation from a calm, credible analyst, not a trading platform.

---

## What it does

Portfolio Scout takes a natural language description of what a user is looking for and returns a complete portfolio proposal across six sections.

It pulls recent price data for a curated universe of equities and ETFs, ranks recent performance, and passes both the market context and the user's intent to Claude. The result is a portfolio that reflects both current market conditions and the stated strategy — not a static template.

Equities, ETFs, and funds only. No cryptocurrency.

---

## Output structure

**Strategy Summary**
The inferred time horizon, risk appetite, and key assumptions the tool made when interpreting the request. If the input was vague, sensible defaults are applied and stated explicitly.

**Suggested Portfolio**
8–14 recommended securities, each with:
- Name and ticker
- Category (stock / ETF / fund)
- Industry or theme
- Why it fits the stated strategy

**Allocation**
Suggested percentage split across the selected holdings, displayed as a visual bar chart sorted by weight.

**Industry View**
Which sectors are represented, how much weight they carry, and why those sectors fit the strategy.

**Risk Notes**
Concentration risks, time-horizon mismatches, and volatility considerations specific to the proposed portfolio.

**Rebalancing & Monitoring**
How often to revisit the portfolio and what signals to watch for.

---

## How it works

The tool fetches 3-month price history for ~80 tracked securities (large-cap stocks, sector ETFs, thematic ETFs, bond funds, dividend ETFs) using Yahoo Finance. It ranks recent 1-month and 3-month performance, then passes the snapshot alongside the user's input to Claude, which interprets the strategy and selects the appropriate holdings.

Three built-in examples cover common investment intents (aggressive growth, balanced long-term, income-focused) and work immediately without any configuration.

For live analysis, the tool calls Claude via the Anthropic API. Market data is fetched fresh on each request.

---

## Positioning

Portfolio Scout is a decision-support tool, not a financial advisor. The output is clearly positioned as informational — a structured starting point for thinking about allocation, not a guaranteed recommendation. The disclaimer is included in every response.

---

## Tech

Python backend (Flask + gunicorn) with a single-page HTML frontend — no JavaScript framework, no build step. Market data via `yfinance`. AI via the Anthropic API (`claude-sonnet-4-6`).
