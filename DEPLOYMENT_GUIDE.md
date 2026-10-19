# Local and hosted deployment notes

VECTRON is a prototype. These instructions explain how to run it for learning, local demos, and controlled evaluation. Do not deploy it as an operational logistics service without the security and integration work described in [SECURITY.md](SECURITY.md).

## Requirements

- Python 3.11 or newer
- Git
- A Google AI Studio API key for Gemini-backed image/document parsing

## Local setup

From the repository root:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a local environment file:

```powershell
# Windows PowerShell
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

Set `GOOGLE_API_KEY` in `.env`. Keep that file out of version control.

Start the API and dashboard:

```bash
python run_server.py
```

The default local dashboard is at `http://127.0.0.1:8000/`; interactive API docs are at `http://127.0.0.1:8000/docs`.

## Configuration

| Variable | Purpose |
| --- | --- |
| `GOOGLE_API_KEY` | Credentials for Gemini-backed image/document parsing |
| `PRIMARY_MODEL` | Primary Gemini model ID |
| `FALLBACK_PRIMARY_MODEL` | Alternate Gemini model ID used by the current model-selection logic |
| `TARGET_LATENCY_MS` | Benchmark target; not a service-level guarantee |
| `MAX_LATENCY_THRESHOLD_MS` | Timeout threshold for model-backed parsing |
| `MAX_RETRIES` | Retry budget used by recovery helpers |
| `BACKOFF_MS` | Base retry backoff in milliseconds |
| `API_PORT` | Local HTTP server port |

Use model IDs currently enabled for your account. Provider availability, quota, and latency can change independently of the application code.

## Hosted deployment

The API can be containerized or hosted on a Python web service, but the current code should be considered demo-only:

- It has no application authentication or role-based authorization.
- CORS is permissive and should be restricted before public deployment.
- Recent metrics and copilot history are process-local and non-durable.
- Route, inventory, and yard integrations use local demonstration data.
- Publicly accessible endpoints should receive synthetic data only.

If deploying to a platform that injects a `PORT` environment variable, verify that the service listens on the assigned port. The current application reads `API_PORT`; platform-specific port wiring may be required.

## Verification after startup

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/mcp/yard?dock_type=HAZMAT
pytest tests -v
python benchmark.py
```

Benchmark results depend on model calls, API availability, warm/cold state, and host load. Report results from the environment you ran rather than treating earlier results as universal.
