"""
Local Model Context Protocol (MCP) Server for Autonomous Yard & Dock Control.
Exposes yard constraints, dock availability, and Hazmat safety perimeters.
Supports both ultra-fast in-process dispatch (< 0.5ms) and JSON-RPC 2.0 MCP Protocol.
"""

import json
from typing import Dict, Any, Optional

# Static Yard Architecture Map & Live Bay Registry
YARD_REGISTRY = {
    "STANDARD": {
        "assigned_dock": "Dock-04-NorthTerminal",
        "dock_restrictions": "Standard Bay: Max axle weight 35 tons; clearance height 14.5ft; hydraulic levelers active.",
        "bay_id": "BAY-N04",
        "crane_available": False,
        "hazmat_certified": False,
        "temperature_controlled": False
    },
    "HAZMAT": {
        "assigned_dock": "Dock-14-Hazmat-Bay-7",
        "dock_restrictions": "HAZMAT Isolation Zone: Spark-proof grounding mandatory; vapor suppression ready; 150m perimeter clear.",
        "bay_id": "BAY-HZ07",
        "crane_available": True,
        "hazmat_certified": True,
        "temperature_controlled": False
    },
    "COLD_CHAIN": {
        "assigned_dock": "Dock-02-ColdStorage-SubZero",
        "dock_restrictions": "Refrigerated Dock: -20C air curtain seal; dual 480V electric hookup; rapid unload within 20 mins.",
        "bay_id": "BAY-CS02",
        "crane_available": False,
        "hazmat_certified": False,
        "temperature_controlled": True
    },
    "HEAVY_LIFT": {
        "assigned_dock": "Dock-19-HeavyCrane-South",
        "dock_restrictions": "Heavy Machinery Bay: 50-ton gantry crane active; reinforced concrete pad; escort required.",
        "bay_id": "BAY-HL19",
        "crane_available": True,
        "hazmat_certified": False,
        "temperature_controlled": False
    }
}

class LocalMcpYardServer:
    """Model Context Protocol Yard Controller Server."""

    def __init__(self):
        self.server_name = "local-mcp-yard-controller"
        self.version = "2.0.0"

    def list_tools(self) -> Dict[str, Any]:
        """Returns MCP tool definitions."""
        return {
            "tools": [
                {
                    "name": "mcp_yard_controller",
                    "description": "Fetches local yard constraints, dock availability, and Hazmat bay maps via Model Context Protocol.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "dock_type": {
                                "type": "string",
                                "description": "Type of dock (STANDARD, HAZMAT, COLD_CHAIN, HEAVY_LIFT)"
                            }
                        },
                        "required": ["dock_type"]
                    }
                }
            ]
        }

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tool calls compliant with MCP JSON-RPC 2.0 specifications."""
        if name == "mcp_yard_controller":
            dock_type = arguments.get("dock_type", "STANDARD").upper()
            bay_info = YARD_REGISTRY.get(dock_type, YARD_REGISTRY["STANDARD"])
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({
                            "assigned_dock": bay_info["assigned_dock"],
                            "dock_restrictions": bay_info["dock_restrictions"],
                            "bay_id": bay_info["bay_id"],
                            "hazmat_certified": bay_info["hazmat_certified"]
                        })
                    }
                ],
                "isError": False
            }
        else:
            return {
                "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                "isError": True
            }

    def resolve_dock(self, dock_type: str) -> Dict[str, str]:
        """High-speed synchronous in-memory resolution for sub-millisecond execution."""
        d_type = (dock_type or "STANDARD").upper()
        if "HAZ" in d_type:
            d_type = "HAZMAT"
        elif "COLD" in d_type or "REEF" in d_type:
            d_type = "COLD_CHAIN"
        elif "HEAVY" in d_type or "CRANE" in d_type:
            d_type = "HEAVY_LIFT"
        elif d_type not in YARD_REGISTRY:
            d_type = "STANDARD"

        info = YARD_REGISTRY[d_type]
        return {
            "assigned_dock": info["assigned_dock"],
            "dock_restrictions": info["dock_restrictions"]
        }

# Global singleton instance for sub-millisecond in-process MCP queries
mcp_yard_server = LocalMcpYardServer()
