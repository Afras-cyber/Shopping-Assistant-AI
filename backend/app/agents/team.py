import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent.parent))

from app.mcp_server.server import _search_product_logic, _calculate_total_logic

from langchain_ollama import ChatOllama
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

llm = ChatOllama(model="llama3.2:3b")

class Notebook(TypedDict):
    topic: str
    plan:str
    budget:int
    research:str
    attempts:int
    recommendation:str
    approval:bool
    feedback:str

def planner(state:Notebook):
    prompt = f"Extract Budget and Need from {state["topic"]}. Reply in 1 line"
    result = llm.invoke([{"role": "user", "content": prompt}])
    budget = 150000
    for word in state['topic'].replace(".","").split():
        if word.isdigit() and int(word) > 1000:
            budget = int(word)
    return {"plan":result.content, "budget":budget}

def researcher(state:Notebook):
    research = _search_product_logic(state['topic'])
    return {"research":research}


def writer(state:Notebook):
    attempts = state.get("attempts", 0) + 1
    feedback = state.get("feedback", "")
    prompt = f"""Recommend products for: {state['topic']}
Budget: {state['budget']} LKR
Plan: {state['plan']}
MCP Research (products from memory):
{state['research']}
MCP Calculator example for Dell:
{_calculate_total_logic(100000, 1)}  
Teacher feedback: {feedback}
RULE: Recommend only products UNDER budget. Must include price in LKR + total with VAT. Max 6 sentences."""
    result = llm.invoke(prompt)
    return {"recommendation": result.content, "attempts": attempts}

def critic(state: Notebook):
    text = state.get("recommendation",'')
    hasLKR = "LKR" in text
    sentence_count = text.count(".") + text.count("!") + text.count("?")
    if hasLKR and sentence_count <=8:
        return {"approval": True, "feedback" :""}
    else:
        return {"approval": False, "feedback": "Must include price in LKR with VAT and max 8 sentences. Only under budget."}

def route_after_critic(state: Notebook):
    if state['approval']:
        return "approval"
    else:
        return "needs_fix"

builder = StateGraph(Notebook)
builder.add_node("planner", planner)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("critic", critic)

builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "writer")
builder.add_edge("writer", "critic")
builder.add_conditional_edges("critic", route_after_critic, 
{
    "approval": END, 
"needs_fix": "writer"
})


graph = builder.compile()