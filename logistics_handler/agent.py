"""
LogisticsHandlerAgent Definition using google-adk.
Configures system instructions, operational rules, tool registrations, and lifecycle callbacks.
"""

from typing import List, Callable
from google.adk.agents.llm_agent import Agent

from logistics_handler.config import PRIMARY_MODEL, FALLBACK_PRIMARY_MODEL
from logistics_handler.tools.routing import calculate_low_latency_route
from logistics_handler.tools.inventory import check_erp_stock_live
from logistics_handler.tools.yard import mcp_yard_controller

SYSTEM_INSTRUCTION = """
You are LogisticsHandlerAgent, an Autonomous Yard, Fleet, and Cargo Dispatch Controller.
OPERATIONAL RULES:
RULE 1 (SPEED FIRST): Do not generate conversational padding, preamble, or apologies. Return pure JSON actions directly.
RULE 2 (MULTIMODAL PARSING): When an image/waybill is ingested, extract SKU, Destination, Consignee, Hazmat status, and Package Damage in a single visual pass.
RULE 3 (PARALLEL DISPATCH): When routing or inventory checks are needed, trigger all tool calls concurrently, never sequentially.
RULE 4 (MANDATORY FEEDBACK LOOP): Pass every tool response through the Self-Healing Interceptor. If an endpoint errors, auto-fallback to safe default parameters without failing the user pipeline.
RULE 5 (MCP RESOLUTION): Query the local Model Context Protocol server for dock/yard constraints prior to dispatch assignment.

OUTPUT FORMAT:
Return strictly a single JSON object matching:
{
  "status": "SUCCESS" | "AUTO_HEALED" | "FLAGGED",
  "multimodal_summary": {
    "bill_id": string,
    "damage_detected": boolean,
    "hazmat_classification": string
  },
  "mcp_yard_context": {
    "assigned_dock": string,
    "dock_restrictions": string
  },
  "routing_decision": {
    "corridor": string,
    "eta_hours": number,
    "toll_cost": number
  },
  "feedback_audit": {
    "self_healed": boolean,
    "retry_count": integer,
    "error_log": string
  },
  "execution_time_ms": number
}
"""

def create_adk_agent(model_name: str = PRIMARY_MODEL) -> Agent:
    """Factory function to build the Google ADK Agent."""
    return Agent(
        name="LogisticsHandlerAgent",
        description="Autonomous Yard, Fleet, and Cargo Dispatch Controller built with google-adk.",
        instruction=SYSTEM_INSTRUCTION.strip(),
        model=model_name,
        tools=[
            calculate_low_latency_route,
            check_erp_stock_live,
            mcp_yard_controller
        ]
    )

# Root agent export for standard ADK discovery (Autonomous UltraFast Dispatcher)
root_agent = create_adk_agent()

# Export Conversational Agent for ADK discovery
from logistics_handler.copilot_agent import create_copilot_agent, copilot_root_agent
