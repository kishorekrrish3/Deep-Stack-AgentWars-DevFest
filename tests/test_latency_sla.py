"""
Test Suite: Latency SLA Verification.
Verifies the Primary Metric: Execution Time Target < 350ms total turn-around latency.
"""

import pytest
import time
from logistics_handler.models import DispatchRequest
from logistics_handler.orchestrator import orchestrator

@pytest.mark.asyncio
async def test_sub_350ms_latency_sla():
    """Executes a batch of 10 dispatch requests and asserts latency < 350ms."""
    latencies = []

    for i in range(10):
        req = DispatchRequest(
            bill_id=f"WB-SLA-TEST-{i+1:02d}",
            sku="SKU-AUTO-1001",
            origin="Chicago, IL",
            destination="Dallas, TX",
            cargo_tons=10.0 + i,
            dock_type="STANDARD"
        )
        output = await orchestrator.dispatch(req)
        latencies.append(output.execution_time_ms)
        assert output.execution_time_ms < 350.0, f"Request {i+1} breached 350ms SLA: {output.execution_time_ms}ms"

    avg_ms = sum(latencies) / len(latencies)
    assert avg_ms < 350.0, f"Average latency breached 350ms SLA: {avg_ms}ms"
