# 🛒 Shopping Assistant Pro

A full-stack Agentic AI shopping assistant.

Type what you want to buy and your budget. A team of 4 AI agents works together to research products and give you a final recommendation with price + VAT + budget check.

Built with Vite + React + FastAPI + LangGraph + Pinecone + MCP.

![Stack](https://img.shields.io/badge/Frontend-Vite%20%2B%20React-blue)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![Agents](https://img.shields.io/badge/Agents-LangGraph-orange)
![Memory](https://img.shields.io/badge/Memory-Pinecone-0EA5E9)
![Tools](https://img.shields.io/badge/Tools-MCP-purple)

---

## ✨ What It Does

**Example:**

> "I need a laptop for coding, budget 150000 LKR"

**Result:**

1. **Planner** understands your need and budget
2. **Researcher** searches products in Pinecone via MCP
3. **Writer** drafts a recommendation
4. **Critic** checks it and sends it back if it is wrong
5. The final recommendation shows in the website, not in the terminal

---

## 🧠 How The AI Team Works

```text
User (Vite Frontend)
  |
  v
FastAPI - POST /shop
  |
  v
LangGraph Team
  Planner -> Researcher -> Writer -> Critic
    |           |            |         |
    |           |            |         +--> If NEEDS FIX, go back to Writer
    |           |            |         +--> If APPROVED, stop
    |           |
    |           +--> MCP Tools: search_product, calculate_total
    |
    +--> Pinecone Vector Memory (nomic-embed-text, 768 dim)
```

**Why multi-agent and not 1 prompt?**
One prompt can hallucinate. A team can check itself. The Critic is the teacher.

---

## 🛠 Tech Stack

| Part | Tech |
| --- | --- |
| Frontend | Vite + React (JavaScript) |
| Backend | FastAPI (Python) |
| Agents | LangChain + LangGraph |
| LLM | Ollama - `llama3.2:3b` (local, free) |
| Embeddings | Ollama - `nomic-embed-text` (768 dim) |
| Vector DB | Pinecone |
| Tools | MCP Server (Model Context Protocol) |
| Language | Python 3.10+, Node.js 18+ |

---

## 📁 Folder Structure - Professional Monorepo

```text
shopping-assistant-pro/
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py                # FastAPI app, CORS, routes
│   │   ├── config.py              # Env, Pinecone, Ollama config
│   │   ├── api/
│   │   │   └── shop.py            # POST /shop - Cashier
│   │   ├── agents/
│   │   │   └── team.py            # Planner, Researcher, Writer, Critic
│   │   ├── tools/
│   │   │   └── pinecone_memory.py # Pinecone search + ingest
│   │   └── mcp_server/
│   │       └── server.py          # MCP tools: search_product, calculate_total
│   └── ingest_pinecone.py         # Load products into Pinecone
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx                # Main page
        ├── api/
        │   └── shop.js            # Only file that calls backend
        └── components/
            └── AnswerCard.jsx
```

**Rules I follow:**

- Frontend never talks to Pinecone directly. Only `src/api/shop.js` calls the backend.
- Backend never returns raw LLM text. It returns clean JSON.

---

## 🚀 How To Run - Step By Step

### 1. Prerequisites

- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) installed
- Pinecone API Key (free tier)

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

### 2. Clone

```bash
git clone https://github.com/Afras-cyber/shopping-assistant-pro.git
cd shopping-assistant-pro
```

### 3. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
PINECONE_API_KEY=your_key_here
PINECONE_INDEX_NAME=shopping-assistant
OLLAMA_MODEL=llama3.2:3b
EMBED_MODEL=nomic-embed-text
```

Load products into Pinecone (only once):

```bash
python scripts/ingest_pinecone.py
```

You should see: `Ingest success`

### 4. Run Backend

```bash
uvicorn app.main:app --reload --port 8002
```

Open: <http://127.0.0.1:8002/docs>

Test `POST /shop` with:

```json
{"topic": "I need a laptop for coding, budget 150000 LKR"}
```

### 5. Run Frontend

Open a new terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open: <http://localhost:5173>

Type a question and click **Get Recommendation**.

---

## 🔌 API

### `POST /shop`

**Request:**

```json
{
  "topic": "I need a laptop for coding, budget 150000 LKR"
}
```

**Response:**

```json
{
  "recommendation": "Based on your requirements, I recommend...",
  "budget": 150000,
  "attempts": 1
}
```

### MCP Tools

| Tool | What it does |
| --- | --- |
| `search_product` | Searches Pinecone for products by meaning, not keyword |
| `calculate_total` | Calculates Subtotal + 18% VAT + Total |

---

## 🧪 Try These

- "I need a laptop for coding, budget 150000 LKR"
- "I need headphones, budget 15000 LKR"
- "I need a mouse, budget 5000 LKR"

---

## 📸 Demo

Add your screenshots here:

1. Frontend home page - `localhost:5173`
2. Team working - Planner, Researcher, Writer, Critic
3. Final recommendation with Budget LKR 150,000

---

## 💡 What I Learned Building This

- **Pinecone dimension must match.** `nomic-embed-text` = 768, `llama-text-embed-v2` = 1024. If they don't match, you get a 400 error. Don't mix Way A (own vectors) and Way B (Pinecone hosted).
- **Pin your versions.** MCP 1.x uses `FastMCP`, MCP 2.x uses `MCPServer`. Use `mcp<2` in `requirements.txt`.
- **LLMs hallucinate.** My Writer once recommended Acer Aspire 5 with GTX 1050, which was not in my Pinecone memory. Fix: make the prompt strict - "Only recommend from MCP memory."
- **CORS matters.** Vite on 5173 cannot talk to FastAPI on 8002 without CORS.

---

## 🔜 Next Improvements

- [ ] Fix Writer hallucination with stricter Critic check
- [ ] Add tests for team
- [ ] Add Docker for backend + frontend
- [ ] Move frontend to Next.js for SEO
- [ ] Mobile app with Expo, same FastAPI backend

---

## 👤 Author

**Afraz Ahd**
Learning in public: AI Engineering + Full-Stack

- GitHub: <https://github.com/Afras-cyber>
- LinkedIn: <https://linkedin.com/in/ahamed-afras-6849aa190>

*Built brick by brick. Still learning. Still building.*
