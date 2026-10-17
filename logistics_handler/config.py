"""
Configuration parameters for LogisticsHandler-ADK-UltraFast
Strict adherence to Zero-Cost ($0.00) and Sub-350ms Latency Target
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root or parent directory
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    load_dotenv()

# Gemini / Google GenAI Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_GENAI_USE_ENTERPRISE = os.getenv("GOOGLE_GENAI_USE_ENTERPRISE", "0")

# Primary Engine
# Defaults to gemini-2.0-flash per spec, with dynamic fallback to gemini-3.8-flash if 2.0 is retired
PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "gemini-2.0-flash")
FALLBACK_PRIMARY_MODEL = os.getenv("FALLBACK_PRIMARY_MODEL", "gemini-3.8-flash")
GENERATION_TEMPERATURE = 0.0
MAX_OUTPUT_TOKENS = 512
RESPONSE_MIME_TYPE = "application/json"

# Groq Cloud Free Tier Fallback Engine
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.2-11b-vision-preview")

# Latency & SLA Parameters
TARGET_LATENCY_MS = float(os.getenv("TARGET_LATENCY_MS", 350.0))
MAX_LATENCY_THRESHOLD_MS = float(os.getenv("MAX_LATENCY_THRESHOLD_MS", 1200.0))
FAST_CACHE_ENABLED = os.getenv("FAST_CACHE_ENABLED", "true").lower() in ("true", "1", "yes")

# Self-Healing Retry Configuration
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
BACKOFF_MS = int(os.getenv("BACKOFF_MS", 25))

# Server Ports
API_PORT = int(os.getenv("API_PORT", 8000))
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 8001))
