# Security policy

DispatchGraph is an educational prototype and is not currently hardened for production or sensitive operational data.

## Supported reporting

Please do not publish credentials, exploitable vulnerabilities, or sensitive operational data in a public issue. Use GitHub's private vulnerability reporting for this repository if it is enabled. Otherwise, contact the repository owner privately through their GitHub profile.

Include the affected component, impact, reproduction steps, and a suggested mitigation where possible. Do not include live API keys or real personal/shipment data.

## Important deployment limitations

The current service does not implement production authentication, authorization, tenant isolation, or durable session storage. Its API configuration includes permissive CORS. Route, inventory, and yard values are demonstration data, and the local fallback is heuristic.

Before using the project in a real logistics environment, conduct a security and privacy review and add, at minimum:

- Authentication and role-based authorization.
- Strict CORS rules, request-size limits, validation, and rate limiting.
- Secret management and credential rotation.
- PII-aware logging and retention controls.
- Tests for prompt injection, unsafe input, cross-tenant access, and provider failure.
- Human review and validation against authoritative transport and HAZMAT regulations.

## Secrets

- Keep API keys in local environment variables or a secret manager.
- Never commit `.env`, access tokens, or real shipment/customer data.
- If a credential is accidentally committed, revoke/rotate it immediately; deleting the visible line does not make the credential safe again.

## Scope

This document is not a compliance certification or guarantee that every security property is implemented. Reported security controls must be verified against the current source code and tests.
