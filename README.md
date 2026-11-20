shopping-assistant-pro/
├── README.md                  - What is this project, how to run, demo video link
├── .gitignore                 - Never push .env, __pycache__, node_modules
├── backend/
│   ├── requirements.txt       - Python packages
│   ├── .env.example           - Example keys, NO real keys inside
│   ├── .env                   - YOUR real keys, never pushed
│   ├── app/
│   │   ├── main.py            - FastAPI app, only starts server, no logic
│   │   ├── core/
│   │   │   └── config.py      - Loads API keys from .env, one place for all settings
│   │   ├── api/
│   │   │   └── shop.py        - API routes: POST /shop, GET /health
│   │   ├── agents/
│   │   │   └── team.py        - Your Planner, Researcher, Writer, Critic team
│   │   ├── tools/
│   │   │   └── pinecone_memory.py - Only Pinecone code, search + upload
│   │   ├── mcp_server/
│   │   │   └── server.py      - MCP server, will do in Brick 2
│   │   └── models/
│   │       └── schemas.py     - Pydantic models: ShopRequest, ShopResponse
│   ├── scripts/
│   │   └── ingest_pinecone.py - One-time script to put products into Pinecone
│   └── tests/
│       └── test_team.py       - 1 test: budget check
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx             - Main page
        ├── api/
        │   └── shop.js         - Only code that calls backend
        └── components/
            ├── ChatBox.jsx     - Input box
            └── AnswerCard.jsx  - Shows recommendation# Shopping-Assistant-AI
