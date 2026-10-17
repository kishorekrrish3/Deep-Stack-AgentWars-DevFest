"""
Test Suite: Self-Healing Feedback Loop.
Verifies Rule 4 and the 3 auto-healing strategies:
1. SCHEMA_MISMATCH
2. RATE_LIMIT_429
3. API_TIMEOUT
"""

import pytest
from logistics_handler.models import DispatchRequest
from logistics_handler.orchestrator import orchestrator
from logistics_handler.self_healing import self_healing_interceptor

@pytest.mark.asyncio
async def test_schema_mismatch_auto_heal():
    """Verifies extraneous keys and markdown are stripped, returning clean strict JSON."""
    raw_bad_json = """
    ```json
    {
      "status": "SUCCESS",
      "conversational_padding": "Here is your dispatch result!",
      "multimodal_summary": {
        "bill_id": "WB-CORRUPT-001",
        "damage_detected": false,
        "hazmat_classification": "NONE",
        "unwanted_metadata": 9999
      },
      "mcp_yard_context": {
        "assigned_dock": "Dock-04-NorthTerminal",
        "dock_restrictions": "Standard",
        "dock_color": "Blue"
      },
      "routing_decision": {
        "corridor": "I-55S_I-30W_EXPRESS",
        "eta_hours": 14.2,
        "toll_cost": 48.50,
        "extra_costs": []
      }
    }
    ```
    """
    healed = self_healing_interceptor.heal_schema_mismatch(
        raw_content=raw_bad_json,
        error_msg="Testing schema mismatch",
        execution_time_ms=12.4
    )
    assert healed.status == "AUTO_HEALED"
    assert healed.feedback_audit.self_healed is True
    assert "SCHEMA_MISMATCH" in healed.feedback_audit.error_log
    assert healed.multimodal_summary.bill_id == "WB-CORRUPT-001"

    # Ensure no extra attributes in sanitized output
    data = healed.model_dump()
    assert "conversational_padding" not in data
    assert "unwanted_metadata" not in data["multimodal_summary"]

@pytest.mark.asyncio
async def test_simulated_429_reroute_to_fallback():
    """Verifies that HTTP 429 triggers the secondary vision engine."""
    req = DispatchRequest(simulate_429=True)
    res = await orchestrator.dispatch(req)

    assert res.status == "AUTO_HEALED"
    assert res.feedback_audit.self_healed is True
    assert "RATE_LIMIT_429" in res.feedback_audit.error_log

@pytest.mark.asyncio
async def test_simulated_latency_spike_timeout_heal():
    """Verifies that latency > 1200ms triggers local cache injection."""
    req = DispatchRequest(simulate_latency_spike=True)
    res = await orchestrator.dispatch(req)

    assert res.status == "AUTO_HEALED"
    assert res.feedback_audit.self_healed is True
    assert "AUTO_HEALED" in res.feedback_audit.error_log or "API_TIMEOUT" in res.feedback_audit.error_log
