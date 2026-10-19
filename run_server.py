"""
Entry point to launch the DispatchGraph API server.
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
    print(f"  DispatchGraph Server v2.0.0")
    print(f"  Framework: google-adk (Agent Development Kit)")
    print(f"  Benchmark target: < 350ms | latency and cost vary by runtime path")
    print(f"  Dashboard: http://127.0.0.1:{API_PORT}")
    print(f"  API Docs:  http://127.0.0.1:{API_PORT}/docs")
    print(f"=======================================================\n")
    uvicorn.run("logistics_handler.api:app", host="0.0.0.0", port=API_PORT, reload=False)

if __name__ == "__main__":
    main()
