"""
Entry point to launch the LogisticsHandler-ADK-UltraFast Server.
Starts FastAPI + MCP Yard Controller + Dashboard on http://127.0.0.1:8000
"""

import sys
import uvicorn
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from logistics_handler.config import API_PORT

def main():
    print(f"\n=======================================================")
    print(f"  LogisticsHandler-ADK-UltraFast Server v2.0.0")
    print(f"  Framework: google-adk (Agent Development Kit)")
    print(f"  Target Latency SLA: < 350ms | Cost: $0.00")
    print(f"  Dashboard: http://127.0.0.1:{API_PORT}")
    print(f"  API Docs:  http://127.0.0.1:{API_PORT}/docs")
    print(f"=======================================================\n")
    uvicorn.run("logistics_handler.api:app", host="0.0.0.0", port=API_PORT, reload=False)

if __name__ == "__main__":
    main()
