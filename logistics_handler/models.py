"""
Pydantic v2 schemas and models matching the ADK UltraFast Specification.
"""

from typing import Literal, Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict

class MultimodalSummary(BaseModel):
    bill_id: str = Field(default="BILL-UNKNOWN", description="Waybill or BOL tracking identifier")
    damage_detected: bool = Field(default=False, description="Whether package or seal damage is detected")
    hazmat_classification: str = Field(default="NONE", description="Hazmat class, e.g. CLASS-3-FLAMMABLE, CLASS-8-CORROSIVE, or NONE")

class McpYardContext(BaseModel):
    assigned_dock: str = Field(default="DOCK-DEFAULT", description="Assigned bay or dock terminal")
    dock_restrictions: str = Field(default="STANDARD_CLEARANCE", description="Yard and dock restrictions or requirements")

class RoutingDecision(BaseModel):
    corridor: str = Field(default="STANDARD-CORRIDOR", description="Optimal route corridor code")
    eta_hours: float = Field(default=0.0, description="Estimated time of arrival in hours")
    toll_cost: float = Field(default=0.0, description="Estimated highway toll cost in USD")

class FeedbackAudit(BaseModel):
    self_healed: bool = Field(default=False, description="Whether auto-heal interceptor was activated")
    retry_count: int = Field(default=0, description="Number of retry attempts executed")
    error_log: str = Field(default="", description="Diagnostic error log if self-healed or flagged")

class LogisticsDispatchOutput(BaseModel):
    status: Literal["SUCCESS", "AUTO_HEALED", "FLAGGED"] = Field(
        default="SUCCESS",
        description="Dispatch execution status"
    )
    multimodal_summary: MultimodalSummary = Field(
        default_factory=MultimodalSummary,
        description="Multimodal parsing result"
    )
    mcp_yard_context: McpYardContext = Field(
        default_factory=McpYardContext,
        description="Dock and yard constraints resolved via MCP"
    )
    routing_decision: RoutingDecision = Field(
        default_factory=RoutingDecision,
        description="Shortest corridor and ETA calculation"
    )
    feedback_audit: FeedbackAudit = Field(
        default_factory=FeedbackAudit,
        description="Self-healing telemetry and audit trail"
    )
    execution_time_ms: float = Field(
        default=0.0,
        description="Turn-around latency in milliseconds"
    )

    model_config = ConfigDict(extra="allow")

# Tool input schemas
class RouteCalculationInput(BaseModel):
    origin: str = Field(..., description="Shipment origin city or facility code")
    destination: str = Field(..., description="Shipment destination city or facility code")
    cargo_tons: float = Field(..., description="Total cargo weight in metric tons")

class ErpStockInput(BaseModel):
    sku: str = Field(..., description="Stock Keeping Unit identifier")

class McpYardInput(BaseModel):
    dock_type: str = Field(..., description="Type of dock needed (e.g. STANDARD, HAZMAT, COLD_CHAIN, HEAVY_LIFT)")

# Request payload for dispatch API
class DispatchRequest(BaseModel):
    bill_id: Optional[str] = None
    sku: Optional[str] = "SKU-AUTO-1001"
    origin: Optional[str] = "Chicago, IL"
    destination: Optional[str] = "Dallas, TX"
    cargo_tons: Optional[float] = 12.5
    dock_type: Optional[str] = "STANDARD"
    image_base64: Optional[str] = None
    image_mime_type: Optional[str] = None
    simulate_429: Optional[bool] = False
    simulate_latency_spike: Optional[bool] = False
    simulate_schema_corruption: Optional[bool] = False
