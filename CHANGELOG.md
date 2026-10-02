# Changelog

All notable changes to the Crunchtools fork of mcp-atlassian are documented in
this file. Upstream changes are tracked in
[sooperset/mcp-atlassian releases](https://github.com/sooperset/mcp-atlassian/releases).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Gourmand CI workflow and pre-commit hook, scoped to the Crunchtools delta;
  upstream paths are excluded (RT #1511).
- Gatehouse review, triage, and pre-commit gates (constitution XII).
- Forked MCP Server profile in the per-repo constitution.
- Multi-stage Containerfile on distroless Hummingbird Python, built and pushed
  to Quay.io by `container.yml`.

### Changed

- Per-repo constitution is now a v1.18.0 manifest: only fork-specific facts
  (upstream, deployment, patches); fleet and profile rules apply by reference.
- Constitution validation pinned to v1.18.0 via `constitution.yml`.
- Dependabot auto-merges GitHub Actions minor and patch updates.
- Synced with upstream v0.22.1.
