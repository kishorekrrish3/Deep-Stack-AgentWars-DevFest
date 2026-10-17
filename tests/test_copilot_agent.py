"""
Test suite for the Conversational Logistics Copilot Agent and MCP endpoints.
Verifies Google ADK agent definition, conversational multi-turn sessions,
tool execution (routing, inventory, yard, dispatch), multimodal inspection,
and MCP JSON-RPC protocol compliance.
"""

import pytest
import base64
from fastapi.testclient import TestClient
from google.adk.agents.llm_agent import Agent

from logistics_handler.copilot_agent import (
    create_copilot_agent,
    copilot_root_agent,
    copilot_session_manager,
    trigger_autonomous_dispatch
)
from logistics_handler.api import app

client = TestClient(app)

def test_copilot_adk_agent_definition():
    """Verifies that the Copilot is properly defined using Google ADK."""
    agent = create_copilot_agent()
    assert isinstance(agent, Agent)
    assert agent.name == "LogisticsCopilotAgent"
    assert "LogisticsCopilot" in agent.instruction
    tool_names = [t.__name__ for t in agent.tools]
    assert "calculate_low_latency_route" in tool_names
    assert "check_erp_stock_live" in tool_names
    assert "mcp_yard_controller" in tool_names
    assert "trigger_autonomous_dispatch" in tool_names

@pytest.mark.asyncio
async def test_copilot_yard_dock_inquiry():
    """Verifies conversational resolution of MCP yard dock constraints."""
    session_id = "test-session-yard-1"
    response = await copilot_session_manager.chat(
        message="What dock is assigned for HAZMAT cargo and what are the safety rules?",
        session_id=session_id
    )
    assert "reply" in response
    assert "mcp_yard_controller" in response["tools_used"]
    assert "Dock-14-Hazmat" in response["reply"] or "HAZMAT" in response["reply"]
    assert response["execution_time_ms"] >= 0.0

@pytest.mark.asyncio
async def test_copilot_erp_inventory_inquiry():
    """Verifies conversational live ERP stock check."""
    session_id = "test-session-inv-1"
    response = await copilot_session_manager.chat(
        message="Can you check real-time warehouse stock for SKU-AUTO-1001?",
        session_id=session_id
    )
    assert "reply" in response
    assert "check_erp_stock_live" in response["tools_used"]
    assert "SKU-AUTO-1001" in response["reply"]
    assert "1420" in response["reply"] or "STAGED_READY" in response["reply"]

@pytest.mark.asyncio
async def test_copilot_corridor_routing_inquiry():
    """Verifies conversational low-latency routing calculation."""
    session_id = "test-session-route-1"
    response = await copilot_session_manager.chat(
        message="What is the lowest latency freight corridor from Chicago to Dallas for 12 tons?",
        session_id=session_id
    )
    assert "reply" in response
    assert "calculate_low_latency_route" in response["tools_used"]
    assert "I-55S_I-30W_EXPRESS" in response["reply"] or "Corridor" in response["reply"]

@pytest.mark.asyncio
async def test_copilot_autonomous_dispatch():
    """Verifies copilot can trigger autonomous dispatch pipeline."""
    session_id = "test-session-disp-1"
    response = await copilot_session_manager.chat(
        message="Please dispatch SKU-CHEM-9012 to Dallas immediately.",
        session_id=session_id
    )
    assert "reply" in response
    assert "trigger_autonomous_dispatch" in response["tools_used"]
    assert "Autonomous Dispatch Executed" in response["reply"] or "SUCCESS" in response["reply"]

@pytest.mark.asyncio
async def test_copilot_multimodal_inspection():
    """Verifies copilot processes attached image/document scans."""
    session_id = "test-session-multi-1"
    # 1x1 dummy PNG
    dummy_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    response = await copilot_session_manager.chat(
        message="Please inspect this waybill image and tell me if it's safe to load.",
        session_id=session_id,
        image_base64=dummy_b64,
        image_mime_type="image/png"
    )
    assert response["multimodal_processed"] is True
    assert "Multimodal Scan" in response["reply"] or "Waybill" in response["reply"]

@pytest.mark.asyncio
async def test_copilot_multi_turn_history():
    """Verifies that conversation history is preserved across turns."""
    session_id = "test-session-history-1"
    res1 = await copilot_session_manager.chat(message="Hello! What can you do?", session_id=session_id)
    assert "LogisticsCopilot" in res1["reply"]

    res2 = await copilot_session_manager.chat(message="Check Bay 7 status please", session_id=session_id)
    assert "Dock" in res2["reply"] or "Bay" in res2["reply"]

    history = copilot_session_manager.get_history(session_id)
    assert len(history) == 4  # 2 user messages + 2 assistant replies

def test_api_copilot_endpoints():
    """Tests the REST API /copilot/chat and /copilot/history endpoints."""
    res = client.post("/copilot/chat", json={
        "message": "Where should I dock a refrigerated cold chain truck?",
        "session_id": "api-copilot-test-1"
    })
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert "mcp_yard_controller" in data["tools_used"]
    assert "Dock-02-ColdStorage" in data["reply"] or "Refrigerated" in data["reply"]

    hist_res = client.get("/copilot/history?session_id=api-copilot-test-1")
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert len(hist_data["messages"]) >= 2

def test_mcp_json_rpc_endpoints():
    """Tests /mcp/tools and /mcp/call JSON-RPC 2.0 endpoints."""
    tools_res = client.get("/mcp/tools")
    assert tools_res.status_code == 200
    tools_data = tools_res.json()
    assert "tools" in tools_data
    assert tools_data["tools"][0]["name"] == "mcp_yard_controller"

    call_res = client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": "test-call-1",
        "method": "tools/call",
        "params": {
            "name": "mcp_yard_controller",
            "arguments": {"dock_type": "HEAVY_LIFT"}
        }
    })
    assert call_res.status_code == 200
    call_data = call_res.json()
    assert "content" in call_data
    assert "50-ton" in call_data["content"][0]["text"] or "Dock-19" in call_data["content"][0]["text"]
