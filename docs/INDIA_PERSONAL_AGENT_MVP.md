# India-first Personal AI Agent — MVP plan

This project is an independent personal assistant inspired by the *category* of personal agents (planning and carrying out multi-step tasks), not a copy of Meta's source code, private APIs, visual identity, or restricted service.

## Important distinction: REA is a developer tool

[REA](https://github.com/morluto/rea) is a local reverse-engineering CLI/MCP server. It helps an authorized developer inspect an app or artifact and collect evidence about behavior. It is not Meta Muse's source code and is not a runtime dependency for the personal-agent product. Use it only on apps, accounts, and artifacts you own or are authorized to inspect. The public REA repository states that its authored code is MIT-licensed; third-party tools and bundled material retain their own terms.

## Product goal

Build an India-accessible, provider-agnostic personal agent that can:
- Turn a natural-language goal into a sequence of small, reviewable steps.
- Draft messages, itineraries, research summaries, checklists, and other useful artifacts.
- Keep a visible activity log and explain what it is about to do.
- Ask for explicit approval before sending messages, submitting forms, making purchases, deleting data, or taking other consequential actions.
- Let users connect only the services they choose and revoke access.
- Keep secrets server-side; never ask users to paste long-lived provider tokens into a public shared demo.

## MVP scope (first release)

1. **Chat + planner:** User enters a goal; the model proposes a structured plan.
2. **Approval gate:** The user approves, edits, or rejects the plan before any tool action.
3. **Safe local tools:** Generate a draft, create a checklist, calculate, and save user-requested notes.
4. **Run history:** Show each step, its status, and any outputs/errors.
5. **Provider configuration:** OpenAI-compatible API endpoint with local Ollama/LM Studio support and hosted providers configured by environment variables.
6. **India-ready deployment:** Responsive web UI, clear privacy/retention notice, and no region-locked Meta service dependency.

## Not in the first release

- No automatic access to WhatsApp, Instagram, Gmail, or other accounts without an official integration and user authorization.
- No pretending a browser action succeeded when it was not verified.
- No autonomous purchases, payments, message sending, or form submission without per-action approval.
- No scraping behind logins, bypassing region controls, or reverse-engineering protections.
- No promise of feature parity with Meta Muse; we will implement and test a narrower, reliable MVP first.

## Suggested architecture

- **UI:** Gradio prototype first; replace with a polished web/mobile UI after validating workflows.
- **Agent service:** Python orchestration, typed plan/action schemas, explicit tool allowlist, step-level timeouts and error handling.
- **Model layer:** Existing OpenAI-compatible provider abstraction in `llm_output_polisher/core.py`, extended carefully rather than coupling to one vendor.
- **Storage:** SQLite for local prototype; production database with per-user isolation, encryption for credentials, retention/deletion controls, and audit events.
- **Execution:** Each tool has a declared input schema, permissions, and a dry-run/approval step where appropriate.
- **Safety:** Treat webpages, files, and retrieved content as untrusted input; keep them separate from system instructions. Require confirmation for external side effects.

## How REA fits the workflow

If a legitimate, accessible Meta Muse web page or app artifact is available, REA can help a developer document observable behavior and evidence. The reconstruction should then be implemented independently using our own code and integrations. A public product description is enough to guide broad product goals; it is not evidence for undocumented internals.

## Release checklist

- [ ] Build a working planner and step log.
- [ ] Add approval-gated, allowlisted tools.
- [ ] Add unit tests for plan validation and permission checks.
- [ ] Add provider timeout/error handling and request limits.
- [ ] Add authentication before any multi-user/public deployment.
- [ ] Add privacy notice, deletion/export path, and incident contact.
- [ ] Verify dependencies, licenses, build, tests, and deployment before claiming release readiness.
