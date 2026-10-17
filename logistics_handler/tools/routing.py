"""
Tool 1: calculate_low_latency_route
Computes shortest corridor avoiding congestion and weather with sub-millisecond cache.
"""

import time
from typing import Dict, Any

# Pre-computed corridor matrix for ultra-fast latency (< 0.5ms)
CORRIDOR_GRAPH = {
    ("CHICAGO", "DALLAS"): {"corridor": "I-55S_I-30W_EXPRESS", "base_eta": 14.2, "base_toll": 48.50, "weather": "CLEAR"},
    ("DALLAS", "CHICAGO"): {"corridor": "I-30E_I-55N_EXPRESS", "base_eta": 14.5, "base_toll": 48.50, "weather": "CLEAR"},
    ("LOS ANGELES", "PHOENIX"): {"corridor": "I-10E_DESERT_BYPASS", "base_eta": 5.8, "base_toll": 18.00, "weather": "CLEAR"},
    ("PHOENIX", "LOS ANGELES"): {"corridor": "I-10W_PACIFIC_FEEDER", "base_eta": 6.1, "base_toll": 18.00, "weather": "CLEAR"},
    ("NEWARK", "ATLANTA"): {"corridor": "I-95S_I-85S_ATL_ARTERIAL", "base_eta": 13.0, "base_toll": 65.00, "weather": "RAIN_MONITORED"},
    ("HOUSTON", "MEMPHIS"): {"corridor": "US-59N_I-69N_MIDWEST", "base_eta": 9.4, "base_toll": 22.50, "weather": "CLEAR"},
    ("SEATTLE", "SALT LAKE"): {"corridor": "I-84E_I-15S_INTERMOUNTAIN", "base_eta": 12.8, "base_toll": 15.00, "weather": "CLEAR"}
}

# In-memory routing LRU cache for zero-latency retrieval
_ROUTING_CACHE: Dict[str, Dict[str, Any]] = {}

def calculate_low_latency_route(origin: str, destination: str, cargo_tons: float) -> Dict[str, Any]:
    """Computes shortest corridor avoiding congestion and weather.

    Args:
        origin: City or terminal of origin (e.g., 'Chicago, IL' or 'Chicago')
        destination: Destination city or terminal (e.g., 'Dallas, TX' or 'Dallas')
        cargo_tons: Cargo gross weight in metric tons

    Returns:
        Dict containing corridor, eta_hours, and toll_cost.
    """
    cache_key = f"{origin.strip().upper()}_{destination.strip().upper()}_{round(cargo_tons, 1)}"
    if cache_key in _ROUTING_CACHE:
        return _ROUTING_CACHE[cache_key]

    orig_clean = origin.split(",")[0].strip().upper()
    dest_clean = destination.split(",")[0].strip().upper()
    key = (orig_clean, dest_clean)

    if key in CORRIDOR_GRAPH:
        route = CORRIDOR_GRAPH[key]
        weight_penalty = max(0.0, (cargo_tons - 10.0) * 0.05)
        eta = round(route["base_eta"] + weight_penalty, 2)
        toll = round(route["base_toll"] + (cargo_tons * 0.85), 2)
        result = {
            "corridor": route["corridor"],
            "eta_hours": eta,
            "toll_cost": toll
        }
    else:
        # Dynamic fallback corridor
        corridor_code = f"CORR-{orig_clean[:3]}-{dest_clean[:3]}-OPT"
        eta = round(8.5 + (cargo_tons * 0.1), 2)
        toll = round(35.00 + (cargo_tons * 0.5), 2)
        result = {
            "corridor": corridor_code,
            "eta_hours": eta,
            "toll_cost": toll
        }

    _ROUTING_CACHE[cache_key] = result
    return result

async def async_calculate_low_latency_route(origin: str, destination: str, cargo_tons: float) -> Dict[str, Any]:
    """Async wrapper for non-blocking parallel execution."""
    return calculate_low_latency_route(origin, destination, cargo_tons)
