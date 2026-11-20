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

Example:
> "I need a laptop for coding, budget 150000 LKR"

Result:
- Planner understands your need and budget
- Researcher searches products in Pinecone via MCP
- Writer drafts a recommendation
- Critic checks it and sends it back if it is wrong
- Final recommendation shows in the website, not in the terminal

## 🧠 How The AI Team Works
