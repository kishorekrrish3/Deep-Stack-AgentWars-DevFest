"""
Tool 3: mcp_yard_controller
Fetches local yard constraints, dock availability, and Hazmat bay maps via Model Context Protocol.
"""

from typing import Dict, Any
from logistics_handler.mcp_server import mcp_yard_server

def mcp_yard_controller(dock_type: str) -> Dict[str, Any]:
    """Fetches local yard constraints, dock availability, and Hazmat bay maps via Model Context Protocol.

    Args:
        dock_type: Dock class requested (STANDARD, HAZMAT, COLD_CHAIN, HEAVY_LIFT)

    Returns:
        Dict with assigned_dock and dock_restrictions.
    """
    return mcp_yard_server.resolve_dock(dock_type)

async def async_mcp_yard_controller(dock_type: str) -> Dict[str, Any]:
    """Async wrapper for non-blocking parallel execution."""
    return mcp_yard_controller(dock_type)
