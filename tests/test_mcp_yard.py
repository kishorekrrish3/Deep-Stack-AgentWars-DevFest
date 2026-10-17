"""
Test Suite: Model Context Protocol (MCP) Yard Controller.
Verifies Rule 5: MCP dock assignment, hazmat safety perimeter, and dock restrictions.
"""

import pytest
from logistics_handler.mcp_server import mcp_yard_server
from logistics_handler.tools.yard import mcp_yard_controller

def test_mcp_standard_dock_resolution():
    res = mcp_yard_controller("STANDARD")
    assert res["assigned_dock"] == "Dock-04-NorthTerminal"
    assert "Standard Bay" in res["dock_restrictions"]

def test_mcp_hazmat_dock_resolution():
    res = mcp_yard_controller("HAZMAT")
    assert res["assigned_dock"] == "Dock-14-Hazmat-Bay-7"
    assert "HAZMAT Isolation" in res["dock_restrictions"]

def test_mcp_cold_chain_dock_resolution():
    res = mcp_yard_controller("COLD_CHAIN")
    assert res["assigned_dock"] == "Dock-02-ColdStorage-SubZero"
    assert "Refrigerated" in res["dock_restrictions"]

def test_mcp_heavy_lift_dock_resolution():
    res = mcp_yard_controller("HEAVY_LIFT")
    assert res["assigned_dock"] == "Dock-19-HeavyCrane-South"
    assert "Heavy Machinery" in res["dock_restrictions"]

def test_mcp_json_rpc_tool_call():
    call_res = mcp_yard_server.call_tool("mcp_yard_controller", {"dock_type": "HAZMAT"})
    assert call_res["isError"] is False
    assert len(call_res["content"]) > 0
    assert "Dock-14-Hazmat-Bay-7" in call_res["content"][0]["text"]
