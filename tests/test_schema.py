"""
Test Suite: Strict JSON Schema Adherence.
Verifies Rule 1 and output_schema compliance according to ADK UltraFast specification.
"""

import pytest
import json
from logistics_handler.models import LogisticsDispatchOutput, DispatchRequest
from logistics_handler.orchestrator import orchestrator

@pytest.mark.asyncio
async def test_strict_output_schema_adherence():
    req = DispatchRequest(
        bill_id="WB-99482-TX",
        sku="SKU-AUTO-1001",
        origin="Chicago, IL",
        destination="Dallas, TX",
        cargo_tons=12.5,
        dock_type="STANDARD"
    )

    output = await orchestrator.dispatch(req)
    assert isinstance(output, LogisticsDispatchOutput)

    # Convert to JSON dictionary
    data = json.loads(output.model_dump_json())

    # Verify all required top-level keys
    required_keys = {
        "status",
        "multimodal_summary",
        "mcp_yard_context",
        "routing_decision",
        "feedback_audit",
        "execution_time_ms"
    }
    assert required_keys.issubset(data.keys())

    # Verify status enum
    assert data["status"] in ["SUCCESS", "AUTO_HEALED", "FLAGGED"]

    # Verify multimodal_summary structure
    assert "bill_id" in data["multimodal_summary"]
    assert isinstance(data["multimodal_summary"]["damage_detected"], bool)
    assert isinstance(data["multimodal_summary"]["hazmat_classification"], str)

    # Verify mcp_yard_context structure
    assert "assigned_dock" in data["mcp_yard_context"]
    assert "dock_restrictions" in data["mcp_yard_context"]

    # Verify routing_decision structure
    assert "corridor" in data["routing_decision"]
    assert isinstance(data["routing_decision"]["eta_hours"], (int, float))
    assert isinstance(data["routing_decision"]["toll_cost"], (int, float))

    # Verify feedback_audit structure
    assert isinstance(data["feedback_audit"]["self_healed"], bool)
    assert isinstance(data["feedback_audit"]["retry_count"], int)
    assert isinstance(data["feedback_audit"]["error_log"], str)

    # Verify execution_time_ms
    assert isinstance(data["execution_time_ms"], (int, float))
    assert data["execution_time_ms"] > 0
