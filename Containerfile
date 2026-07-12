# MCP Atlassian Container (sooperset/mcp-atlassian fork)
# Containerized following crunchtools constitution for streamable-http deployment
#
# Build:
#   podman build -f Containerfile -t quay.io/crunchtools/mcp-atlassian .
#
# Run:
#   podman run --env-file ~/.config/mcp-env/mcp-atlassian.env \
#     -p 127.0.0.1:8015:8000 quay.io/crunchtools/mcp-atlassian

FROM quay.io/hummingbird/python:latest

LABEL name="mcp-atlassian" \
      summary="MCP server for Atlassian Jira and Confluence" \
      description="Containerized sooperset/mcp-atlassian for streamable-http transport" \
      maintainer="crunchtools.com" \
      url="https://github.com/crunchtools/mcp-atlassian" \
      org.opencontainers.image.source="https://github.com/crunchtools/mcp-atlassian" \
      org.opencontainers.image.description="MCP server for Atlassian Jira and Confluence" \
      org.opencontainers.image.licenses="AGPL-3.0-or-later"

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir .
ENV PATH="/tmp/.local/bin:${PATH}"

RUN python -c "from mcp_atlassian import main; print('Installation verified')"

EXPOSE 8000
ENTRYPOINT ["mcp-atlassian"]
CMD ["--transport", "streamable-http", "--host", "0.0.0.0"]
