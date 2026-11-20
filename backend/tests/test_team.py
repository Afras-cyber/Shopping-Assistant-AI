import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.agents.team import graph

result = graph.invoke({
    "topic": "I need a laptop for coding, budget 150000 LKR",
    "attempts": 0, "feedback": "", "approved": False, "budget": 0,
    "plan": "", "research": "", "recommendation": ""
})
print("\n===== FINAL RECOMMENDATION =====")
print(result['recommendation'])
print(f"\nBudget: {result['budget']}, Attempts: {result['attempts']}")