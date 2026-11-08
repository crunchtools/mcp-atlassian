import json
import os
import subprocess


def _probe_message(message_id: int | None, method: str, params: dict) -> str:
    message: dict = {"jsonrpc": "2.0", "method": method, "params": params}
    if message_id is not None:
        message["id"] = message_id
    return json.dumps(message) + "\n"


def _read_response(proc: subprocess.Popen[str], message_id: int) -> str:
    assert proc.stdout is not None
    for line in proc.stdout:
        if line.startswith('{"jsonrpc"') and f'"id":{message_id}' in line:
            return line
    raise AssertionError(f"stdout closed before response {message_id}")


def test_stdio_homebrew_probe_exits_after_stdin_close() -> None:
    """A probe gets its tools/list answer, and closing stdin then ends the
    process promptly (#939). The probe waits for the answer before closing
    stdin: the MCP SDK cancels in-flight requests when the transport closes."""
    env = os.environ.copy()
    env.update(
        {
            "JIRA_URL": "https://example.atlassian.net",
            "JIRA_USERNAME": "user@example.com",
            "JIRA_API_TOKEN": "x",
        }
    )

    proc = subprocess.Popen(
        ["uv", "run", "mcp-atlassian"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    try:
        assert proc.stdin is not None
        proc.stdin.write(
            _probe_message(
                1,
                "initialize",
                {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "homebrew-probe", "version": "1.0"},
                },
            )
        )
        proc.stdin.flush()
        _read_response(proc, 1)

        proc.stdin.write(_probe_message(None, "notifications/initialized", {}))
        proc.stdin.write(_probe_message(2, "tools/list", {}))
        proc.stdin.flush()
        assert '"tools"' in _read_response(proc, 2)

        proc.stdin.close()
        assert proc.wait(timeout=15) == 0
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
