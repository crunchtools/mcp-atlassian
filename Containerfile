# MCP Atlassian Container (sooperset/mcp-atlassian fork)
# Multi-stage: builder for pip install, distroless runtime
#
# Build:
#   podman build -f Containerfile -t quay.io/crunchtools/mcp-atlassian .
#
# Run:
#   podman run --env-file ~/.config/mcp-env/mcp-atlassian.env \
#     -p 127.0.0.1:8015:8000 quay.io/crunchtools/mcp-atlassian

FROM quay.io/hummingbird/python:3.14-builder AS lock
USER 0
RUN pip install --no-cache-dir uv==0.13.7
WORKDIR /lock
COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-emit-project \
      --format requirements-txt -o /requirements.txt

FROM quay.io/hummingbird/python:3.14-builder AS builder

WORKDIR /app

RUN python3 -m venv /app/venv

COPY --from=lock /requirements.txt /tmp/requirements.txt
RUN /app/venv/bin/pip install --no-cache-dir --no-deps -r /tmp/requirements.txt

COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN /app/venv/bin/pip install --no-cache-dir --no-deps .

FROM quay.io/hummingbird/python:3.14

LABEL name="mcp-atlassian" \
      summary="MCP server for Atlassian Jira and Confluence" \
      description="Containerized sooperset/mcp-atlassian for streamable-http transport" \
      maintainer="crunchtools.com" \
      url="https://github.com/crunchtools/mcp-atlassian" \
      org.opencontainers.image.source="https://github.com/crunchtools/mcp-atlassian" \
      org.opencontainers.image.description="MCP server for Atlassian tools (Confluence, Jira)" \
      org.opencontainers.image.licenses="MIT"

COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:${PATH}"

EXPOSE 8000
ENTRYPOINT ["mcp-atlassian"]
CMD ["--transport", "streamable-http", "--host", "0.0.0.0"]
