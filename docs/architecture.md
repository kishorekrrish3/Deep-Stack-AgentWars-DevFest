# Architecture notes

DispatchGraph is a logistics dispatch prototype built around a FastAPI service, a dispatch orchestrator, deterministic demonstration tools, and a Google ADK conversational copilot.

## Request paths

### Dispatch API

1. A client submits structured shipment metadata to `POST /dispatch`, or a document/image to `POST /dispatch/multimodal`.
2. The orchestrator fans out route calculation, inventory lookup, and yard selection with asynchronous concurrency.
3. If an image is supplied and a Google API key is configured, the system attempts model-backed document/image understanding.
4. If the model-backed parsing path fails or times out, the fallback engine returns a heuristic result and the response records recovery status.
5. The response is assembled from typed Pydantic models, including dispatch status, routing/yard context, recovery audit, and elapsed time.

The non-image text fast path uses local heuristics. It should not be described as computer vision.

### Conversational copilot

The Google ADK copilot accepts natural-language requests and has access to route, inventory, yard, and dispatch tools. Session history is kept in process memory; it is not durable storage and is lost when the server process restarts.

## Main modules

| Module | Responsibility |
| --- | --- |
| `logistics_handler/api.py` | FastAPI app, endpoint definitions, dashboard route, and in-memory metrics |
| `logistics_handler/orchestrator.py` | Dispatch workflow, asynchronous tool fan-out, multimodal parsing, and response assembly |
| `logistics_handler/copilot_agent.py` | Google ADK conversational agent and session manager |
| `logistics_handler/models.py` | Pydantic request and response schemas |
| `logistics_handler/tools/routing.py` | Route calculation demonstration tool |
| `logistics_handler/tools/inventory.py` | SKU and staging demonstration tool |
| `logistics_handler/tools/yard.py` | Yard controller adapter |
| `logistics_handler/mcp_server.py` | Local yard registry, tool definition, and JSON-RPC-style dispatch |
| `logistics_handler/self_healing.py` | Response normalization and failure-recovery helpers |
| `logistics_handler/fallback_engine.py` | Local rule-based fallback for parsing metadata |
| `benchmark.py` | End-to-end benchmark and simulated recovery exercises |

## Trust boundaries and current limitations

The project is a prototype. A few distinctions are important:

- Route and inventory results are local demonstration logic; they are not live traffic, carrier, or ERP data.
- Yard assignments are resolved against a local registry. This is not an integration with a physical yard-management system.
- The yard interface exposes MCP-shaped tool metadata and a JSON-RPC-style HTTP endpoint. The current implementation is not a separately deployed MCP service connected to external operations.
- Model-backed vision depends on the Google API and the configured model ID. The local fallback uses heuristics and request text/metadata; it is not a replacement for image understanding.
- The default implementation uses Gemini plus local fallback. End-to-end Groq/OpenRouter multi-provider failover is not currently wired as an active integration.
- The API has no authentication and configures permissive CORS. Do not expose it to untrusted users or send sensitive shipment data to a public instance.
- A response marked successful is not a guarantee of route feasibility, inventory availability, or hazardous-material compliance.

## Extending the system

When adding a real provider integration, keep the deterministic interface stable and add contract tests for normal responses, timeouts, rate limits, malformed payloads, and unavailability. Store provider credentials in environment variables or a secret manager, never source code. Keep benchmark reports explicit about which work is local, cached, or model-backed.
