# Contributing to DispatchGraph

Thanks for helping improve DispatchGraph. Small, focused contributions are easiest to review.

## Before opening an issue

- Search existing issues for duplicates.
- Include a minimal reproduction, expected behavior, actual behavior, and relevant logs with secrets removed.
- Use synthetic shipment data. Never attach real customer documents or private operational data.

## Development setup

Use Python 3.11 or newer from the repository root:

```bash
python -m venv .venv
```

Activate it, then install project dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For model-backed image/document tests, create a local `.env` from `.env.example` and add your own Google AI Studio API key. Do not commit `.env`.

## Verification

Run tests before submitting a change:

```bash
pytest tests -v
```

For changes to dispatch timing or recovery paths, also run:

```bash
python benchmark.py
```

Benchmarks can vary with API availability, model latency, host load, and cache/warm state. Include the command you ran and the observed results rather than copying a previous benchmark claim.

## Pull request checklist

- [ ] The change has a clear, focused purpose.
- [ ] Tests are added or updated where appropriate.
- [ ] Documentation reflects the actual implementation.
- [ ] No credentials, private shipment records, or customer documents are included.
- [ ] Failure cases are considered for provider/tool integrations.
- [ ] Latency claims identify the exact path measured and the environment.
- [ ] The full test output is summarized in the PR description.

## Design principles

1. Prefer deterministic business rules for hard constraints.
2. Keep model output separate from tool-derived values.
3. Make failure and fallback behavior observable.
4. Do not label demonstration data as live operational data.
5. Preserve compatibility or document breaking changes clearly.
