# Changelog

All notable changes to the Crunchtools fork of mcp-atlassian are documented in
this file. Upstream changes are tracked in
[sooperset/mcp-atlassian releases](https://github.com/sooperset/mcp-atlassian/releases).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Gatehouse triage passes `review_result: ${{ needs.review.result }}`, so a PR
  whose review job died before posting is held instead of passing (constitution
  v1.52.0 XII Triage, gatehouse#161).

### Changed
- CI is the fleet's one `ci.yml` (sdlc 0.15), configured in `[tool.sdlc]`.
  It replaces the Gatehouse, constitution, security, Ashigaru and container
  workflows: the image is built, booted over MCP stdio, scanned, signed and
  promoted by its `image` and `promote` jobs from `[tool.sdlc.image]`, and the
  `stacks` key puts the Containerfile under the gates. The signing and
  `container-release.yml` entries below describe the workflows this replaces.
- Promote signs the image with the fleet cosign key (`sign: true`), because
  bootc hosts are moving to trust only signed `quay.io/crunchtools` images
  (crunchtools/rhel10-bootc-server#47). Needs the repo's `cosign-signing`
  environment to hold `COSIGN_PRIVATE_KEY` and `COSIGN_PASSWORD`.
- The container release runs constitution v1.51.0's `container-release.yml`
  (was v1.46.0) and grants it `issues: write`, so a failed scheduled rebuild
  opens an issue instead of only warning. A `v*` promote now also refuses an
  image whose `version` label names a different release of this repo; this
  image sets none, and the one it inherits from Hummingbird is not compared.

### Removed
- The upstream `@claude` workflow (`claude.yml`). Nothing replaces it: the
  fleet's `ai` job triages issues and reviews PRs but does not answer
  `@claude` mentions.
- The upstream stale-issue bot (`stale.yml`), and Dependabot with its
  auto-merge; Renovate's org config covers updates.

## [0.22.4] - 2026-11-14

### Fixed
- Jira tools' default `fields` value is now a sorted string. It was joined
  from a set, so its order changed with every process; each restart published
  a new tool schema, and gateways that pin tool definitions held the Jira
  tools again until an operator re-approved them.

## [0.22.3] - 2026-11-11

### Fixed

- The container installed dependencies with `pip install .`, which reads only
  `pyproject.toml`'s floor-pins and resolves a fresh set at build time instead
  of the committed, Dependabot-maintained `uv.lock`. CI tests the locked
  versions; the shipped image could silently drift to different ones. The
  builder now exports `uv.lock` to a requirements file in a dedicated stage
  and installs both it and the project with `--no-deps`, so the image ships
  exactly what CI tested (RT #1564).

### Removed

- Upstream's PyPI publish workflow. It ran on every fork release and would
  publish to upstream's `mcp-atlassian` package name; the fork ships only the
  Quay.io image.

## [0.22.2] - 2026-11-08

First Crunchtools fork release, on upstream v0.22.1.

### Security

- Upgraded locked dependencies within their declared ranges to clear the
  advisories the fleet dependency audit found (26 of 28 flagged packages).
- Ported to fastmcp 3.4 (PYSEC-2026-2475, PYSEC-2026-2476, GHSA-7xgj-8392-5q4r).
  This also drops diskcache (PYSEC-2026-2447), which only fastmcp 2.x pulled
  in (#24).
- Tool enablement (read-only mode, `ENABLED_TOOLS`, toolsets) is now enforced
  by fastmcp middleware on every tools/list and tools/call path. A call with no
  lifespan context is refused, not allowed through.

### Added

- Gourmand CI workflow and pre-commit hook, scoped to the Crunchtools delta;
  upstream paths are excluded (RT #1511).
- Gatehouse review, triage, and pre-commit gates (constitution XII).
- Forked MCP Server profile in the per-repo constitution.
- Multi-stage Containerfile on distroless Hummingbird Python, built and pushed
  to Quay.io by `container.yml`.

### Changed

- Tool input schemas now declare `additionalProperties: false`. The server
  already rejected unknown arguments; fastmcp 3 now says so in the schema.
  Tool names, parameters and tags are unchanged. Tags moved from
  `meta._fastmcp` to `meta.fastmcp`.
- Container base images pinned to `quay.io/hummingbird/python:3.14*` instead of
  `latest`, which moved to Python 3.15.0 on 2026-10-20 (crunchtools/constitution#66).
- Per-repo constitution is now a v1.18.0 manifest: only fork-specific facts
  (upstream, deployment, patches); fleet and profile rules apply by reference.
- Constitution validation pinned to v1.18.0 via `constitution.yml`.
- Dependabot auto-merges GitHub Actions minor and patch updates.
- Synced with upstream v0.22.1.

[Unreleased]: https://github.com/crunchtools/mcp-atlassian/compare/v0.22.3...HEAD
[0.22.3]: https://github.com/crunchtools/mcp-atlassian/releases/tag/v0.22.3
[0.22.2]: https://github.com/crunchtools/mcp-atlassian/releases/tag/v0.22.2
