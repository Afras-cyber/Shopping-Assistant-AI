# backend/app/mcp_server/server.py - Works on MCP 1.x and 2.x
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from app.tools.pinecone_memory import search_products

from mcp.server.fastmcp import FastMCP
mcp = FastMCP("shop-tools")

def _search_product_logic(query: str) -> str:
    """Real logic, no decorator, so we can test it easily"""
    results = search_products(query, top_k=3)
    if not results:
        return "No products found"
    return "\n".join(results)

def _calculate_total_logic(price: int, quantity: int = 1) -> str:
    subtotal = price * quantity
    tax = int(subtotal * 0.18)
    total = subtotal + tax
    return f"Subtotal: {subtotal} LKR, VAT 18%: {tax} LKR, Total: {total} LKR"

# Register tools with MCP, using the plain logic functions
search_product = mcp.tool()(_search_product_logic)
calculate_total = mcp.tool()(_calculate_total_logic)

if __name__ == "__main__":
    mcp.run()