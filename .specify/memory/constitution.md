# mcp-atlassian Constitution

> **Version:** 1.1.0
> **Ratified:** 2026-09-20
> **Status:** Active
> **Inherits:** [crunchtools/constitution](https://github.com/crunchtools/constitution) v1.17.0
> **Profile:** Forked MCP Server

## Upstream

- **Source:** https://github.com/sooperset/mcp-atlassian
- **License:** MIT
- **Forked at:** v0.22.1 (last sync 2026-07-12)

## Deployment

- **Port:** 8021
- **Env file:** /srv/mcp-jira.crunchtools.com/config/mcp-jira.env
- **Credentials:** JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN, ALLOW_GLOBAL_CRED_FALLBACK, TOOLSETS

## Patches

- Multi-stage Containerfile on distroless Hummingbird Python (upstream ships a single-stage python:slim build)
- Security hardening across the attachment, transport, SSRF, authorization, filter and OAuth layers
- Proxy routing preserved for trusted transports
- Rate-limit tests made deterministic against a shared bucket

## Registry

Quay.io only — `quay.io/crunchtools/mcp-atlassian`. Per constitution Section III,
forked projects do not dual-push to GHCR; the GHCR mirror exists for images we
author. This repo was flagged as a Section III gap during the RT #1480 fleet
sweep purely because it had no profile declared, so it fell through to the
default container-image expectations. It was exempt the whole time.

## Quality Gates

Gourmand gates only the Crunchtools delta (Containerfile, our workflows,
`.specify/`, our config); upstream paths are excluded in
`.gourmand-exceptions.d/globals.toml` and revisited on each upstream sync.
