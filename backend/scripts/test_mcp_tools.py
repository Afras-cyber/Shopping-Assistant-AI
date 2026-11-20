# backend/scripts/test_mcp_tools.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.mcp_server.server import _search_product_logic, _calculate_total_logic

print("Test 1 - Search:")
print(_search_product_logic("laptop for coding"))
print("\nTest 2 - Calculate:")
print(_calculate_total_logic(145000, 1))