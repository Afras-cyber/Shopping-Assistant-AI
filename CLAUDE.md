# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A monorepo for a multi-agent shopping assistant. A Vite + React frontend calls a FastAPI backend. The backend runs a LangGraph pipeline (Planner → Researcher → Writer → Critic) on a local Ollama LLM, and the Researcher pulls product data from a Pinecone vector index. Prices are in LKR, and an 18% VAT is added.

## Commands

Backend (run from `backend/`; imports use the `app.` package, so the working directory must be `backend/`):

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/ingest_pinecone.py          # one-time: embed + upsert sample products into Pinecone
uvicorn app.main:app --reload --port 8002   # Swagger at http://127.0.0.1:8002/docs
python -m app.mcp_server.server             # run the MCP tool server standalone (stdio)
```

Frontend (run from `frontend/`):

```bash
npm ci
npm run dev      # http://localhost:5173
npm run build
npm run lint     # ESLint (flat config in eslint.config.js)
```

The repo has no test suite.

Runtime prerequisites:
- Ollama must be running with `llama3.2:3b` and `nomic-embed-text` pulled.
- `backend/.env` must set `PINECONE_API_KEY`, and can also set `PINECONE_INDEX_NAME` and `OLLAMA_MODEL`.

## Architecture

Request flow: `frontend/src/api/shop.js` → `POST /shop` (`backend/app/api/shop.py`) → `graph.invoke(...)` (`backend/app/agents/team.py`) → a JSON `ShopResponse {recommendation, budget, attempts}` (`app/models/schemas.py`).

- **Agent graph (`app/agents/team.py`)**: a LangGraph `StateGraph` over the `Notebook` TypedDict.
  - `planner` asks the LLM for a one-line plan. The budget does not come from the LLM: the code takes the last digit-only word in the topic above 1000 as the budget, and defaults to 150000.
  - `researcher` calls the Pinecone search.
  - `writer` prompts the LLM with the research and a VAT example.
  - `critic` is rule-based, not an LLM. It approves when the text contains "LKR" and has at most 8 sentences. Otherwise it routes back to `writer` with feedback. The retry loop has no cap of its own, so only LangGraph's recursion limit stops it.
- **MCP tools (`app/mcp_server/server.py`)**: the plain functions `_search_product_logic` and `_calculate_total_logic` are wrapped with `FastMCP.tool()`. The agent graph imports and calls the plain `_..._logic` functions directly; it does not call them over MCP. Keep the logic in the undecorated functions.
- **Vector memory (`app/tools/pinecone_memory.py`)**: creates the Pinecone index if it is missing (768-dim, cosine, AWS us-east-1) **at import time**, and embeds with Ollama `nomic-embed-text`. As a result, importing `team.py`, `server.py` or `app.main` needs network access to Pinecone and a running Ollama. The embedding dimension must stay 768 to match the index. Search results come from `metadata["text"]`, so upserts must include a `text` field.
- **Config (`app/core/config.py`)**: the only module meant to read `.env`. Note that `team.py` currently hardcodes `ChatOllama(model="llama3.2:3b")` and ignores `settings.OLLAMA_MODEL`.
- **Frontend**: a single page in `src/App.jsx` styled with Tailwind v4 through `@tailwindcss/vite`. The agent progress indicator is purely cosmetic: it is driven by a timer and does not stream from the backend. The backend URL `http://127.0.0.1:8002` is hardcoded in `src/api/shop.js`.

## Conventions and gotchas

- Only `frontend/src/api/shop.js` may call the backend. The frontend never talks to Pinecone. The backend returns structured JSON, not raw LLM output.
- Pin `mcp<2`: the code uses `mcp.server.fastmcp.FastMCP`, which MCP 2.x renamed.
- `team.py`, `server.py` and `scripts/ingest_pinecone.py` add `backend/` to `sys.path` themselves, so they can be run as standalone scripts.
- `requirements.txt` does not list `langgraph`, which `team.py` imports. Install it separately if it is missing.
- `planner` uses nested double quotes inside an f-string (`f"...{state["topic"]}..."`), which requires Python 3.12+.
- The state key is inconsistent: `api/shop.py` seeds `"approved"`, but the graph reads and writes `"approval"`.
- The 3B model tends to recommend products that are not in Pinecone (see README). When editing the Writer prompt, keep it grounded in the `research` text, and consider making it stricter.
- README.md's folder tree is out of date: config is in `app/core/`, the ingest script is in `scripts/`, and `components/AnswerCard.jsx` does not exist.
