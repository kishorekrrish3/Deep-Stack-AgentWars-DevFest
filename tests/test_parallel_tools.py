"""
Test Suite: Parallel Dispatch Concurrency.
Verifies Rule 3: all tool calls are executed concurrently with sub-50ms latency.
"""

import pytest
import time
from logistics_handler.orchestrator import orchestrator
from logistics_handler.tools.routing import calculate_low_latency_route
from logistics_handler.tools.inventory import check_erp_stock_live
from logistics_handler.tools.yard import mcp_yard_controller

@pytest.mark.asyncio
async def test_parallel_tool_execution():
    t0 = time.perf_counter()
    route, stock, yard = await orchestrator.execute_parallel_tools(
        origin="Chicago, IL",
        destination="Dallas, TX",
        cargo_tons=12.5,
        sku="SKU-AUTO-1001",
        dock_type="STANDARD"
    )
    t1 = time.perf_counter()
    elapsed_ms = (t1 - t0) * 1000.0

    # Ensure concurrent execution is ultra fast (well under 50ms, usually < 2ms)
    assert elapsed_ms < 50.0, f"Parallel tool execution too slow: {elapsed_ms}ms"

    # Verify tool outputs
    assert "corridor" in route
    assert "eta_hours" in route
    assert "toll_cost" in route

    assert "sku" in stock
    assert stock["sku"] == "SKU-AUTO-1001"
    assert "units_available" in stock

    assert "assigned_dock" in yard
    assert "dock_restrictions" in yard
