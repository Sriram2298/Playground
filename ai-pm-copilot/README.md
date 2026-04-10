# PM Copilot

An AI-powered product analysis tool for product managers and founders. Describe a product idea in plain language and get back a structured, opinionated PM analysis — the kind a senior PM would produce after a day of thinking, returned in seconds.

---

## What it does

PM Copilot takes a rough product idea as input and returns a full 10-section analysis covering the product from every angle a PM would care about before committing resources to it.

The output is designed to be critical and specific — not generic encouragement, but the questions and risks that actually determine whether a product idea is worth building.

---

## Output structure

**Quick Evaluation**
Three scores (1–10) across the dimensions that matter most at the idea stage:
- Clarity of Problem — is the pain real, specific, and measurable?
- Differentiation — is there a credible reason someone would switch to this?
- Feasibility — is the hard part a technical problem or a distribution problem?

Each score includes a one-line rationale and a plain-language verdict.

**10-section analysis**
1. Problem Statement — the specific workflow gap and who it costs
2. Target Users — primary and secondary users with key characteristics
3. Core Use Cases — the actions the product must support end-to-end
4. Solution Approach — the core mechanic and the key product decisions
5. Risks & Failure Modes — where this type of product typically fails
6. Assumptions — what has to be true for this to work
7. Success Metrics — leading indicators that the product is working
8. Edge Cases — the scenarios that break naive implementations
9. MVP Scope — what's in, what's explicitly out for v1
10. Suggested Next Steps — the first three things to do before writing a line of code

---

## How it works

The tool accepts any product description — a one-liner, a paragraph, or a rough brief. It interprets the input, infers the product category, and generates a structured analysis grounded in PM practice.

Three built-in examples demonstrate the output for common product types (a freelancer tool, a two-sided marketplace, and an AI workflow tool) and work immediately without any configuration.

For live analysis of a custom idea, the tool calls Claude via the Anthropic API and generates a fresh analysis specific to what was described.

---

## Tech

Single-page web app. Python backend (FastAPI) with an embedded frontend — no separate build step, no frontend framework. The full product ships as two files: `app.py` and `requirements.txt`.
