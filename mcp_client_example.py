#!/usr/bin/env python3
"""
Minimal MCP Streamable HTTP client example for TwiAPI.

Examples:

  # Initialize only
  venv/bin/python examples/mcp_client_example.py \
    --url http://127.0.0.1:9833/mcp \
    initialize

  # List all tools
  venv/bin/python examples/mcp_client_example.py \
    --url http://127.0.0.1:9833/mcp \
    --api-key YOUR_API_KEY \
    list-tools

  # Call a tool
  venv/bin/python examples/mcp_client_example.py \
    --url http://127.0.0.1:9833/mcp \
    --api-key YOUR_API_KEY \
    call \
    --tool user_info \
    --arguments '{"username":"openai"}'
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import sys
from typing import Any

import httpx


class McpHttpClient:
    def __init__(
        self,
        url: str,
        api_key: str | None = None,
        protocol_version: str = "2025-11-25",
        timeout: float = 30.0,
    ) -> None:
        self.url = url
        self.api_key = api_key
        self.protocol_version = protocol_version
        self._id_counter = itertools.count(1)
        self._client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def initialize(self, client_name: str, client_version: str) -> dict[str, Any]:
        payload = {
            "jsonrpc": "2.0",
            "id": next(self._id_counter),
            "method": "initialize",
            "params": {
                "protocolVersion": self.protocol_version,
                "capabilities": {},
                "clientInfo": {
                    "name": client_name,
                    "version": client_version,
                },
            },
        }
        return self._request(payload, include_auth=False)

    def initialized(self) -> None:
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        }
        self._request(payload, include_auth=False)

    def initialize_session(self, client_name: str, client_version: str) -> dict[str, Any]:
        result = self.initialize(client_name=client_name, client_version=client_version)
        self.initialized()
        return result

    def list_tools(self) -> list[dict[str, Any]]:
        self._require_api_key()
        tools: list[dict[str, Any]] = []
        cursor: str | None = None

        while True:
            payload = {
                "jsonrpc": "2.0",
                "id": next(self._id_counter),
                "method": "tools/list",
                "params": {} if cursor is None else {"cursor": cursor},
            }
            result = self._request(payload, include_auth=True)
            tools.extend(result.get("tools", []))
            cursor = result.get("nextCursor")
            if not cursor:
                break

        return tools

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self._require_api_key()
        payload = {
            "jsonrpc": "2.0",
            "id": next(self._id_counter),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments,
            },
        }
        return self._request(payload, include_auth=True)

    def _request(self, payload: dict[str, Any], include_auth: bool) -> dict[str, Any] | None:
        response = self._client.post(
            self.url,
            headers=self._build_headers(include_auth=include_auth),
            json=payload,
        )
        response.raise_for_status()

        if response.status_code == 202 or not response.content:
            return None

        message = response.json()
        if "error" in message:
            error = message["error"]
            raise RuntimeError(
                f"MCP error {error.get('code')}: {error.get('message')}"
            )
        return message.get("result", {})

    def _build_headers(self, include_auth: bool) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "MCP-Protocol-Version": self.protocol_version,
        }
        if include_auth:
            self._require_api_key()
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _require_api_key(self) -> None:
        if not self.api_key:
            raise ValueError(
                "This command requires an API key. Pass --api-key or set TWIAPI_MCP_KEY."
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simple MCP Streamable HTTP client example for TwiAPI.",
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:9833/mcp",
        help="MCP server URL. Default: http://127.0.0.1:9833/mcp",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("TWIAPI_MCP_KEY"),
        help="API key used as Authorization: Bearer <api_key>. Defaults to env TWIAPI_MCP_KEY.",
    )
    parser.add_argument(
        "--protocol-version",
        default="2025-11-25",
        help="Requested MCP protocol version. Default: 2025-11-25",
    )
    parser.add_argument(
        "--client-name",
        default="twiapi-sample-client",
        help="Client name used during initialize.",
    )
    parser.add_argument(
        "--client-version",
        default="1.0.0",
        help="Client version used during initialize.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("initialize", help="Run initialize + initialized only.")
    subparsers.add_parser("list-tools", help="Run initialize and list all tools.")

    call_parser = subparsers.add_parser("call", help="Run initialize and call one tool.")
    call_parser.add_argument("--tool", required=True, help="Tool name to call.")
    call_parser.add_argument(
        "--arguments",
        default="{}",
        help='Tool arguments as JSON string, e.g. \'{"username":"openai"}\'.',
    )
    return parser.parse_args()


def pretty_print(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main() -> int:
    args = parse_args()
    client = McpHttpClient(
        url=args.url,
        api_key=args.api_key,
        protocol_version=args.protocol_version,
    )

    try:
        init_result = client.initialize_session(
            client_name=args.client_name,
            client_version=args.client_version,
        )

        if args.command == "initialize":
            pretty_print(init_result)
            return 0

        if args.command == "list-tools":
            tools = client.list_tools()
            print(f"Found {len(tools)} tools from {args.url}")
            for tool in tools:
                print(f"- {tool['name']}: {tool.get('description', '')}")
            return 0

        if args.command == "call":
            try:
                arguments = json.loads(args.arguments)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid --arguments JSON: {exc.msg}") from exc
            if not isinstance(arguments, dict):
                raise ValueError("--arguments must decode to a JSON object")
            result = client.call_tool(args.tool, arguments)
            pretty_print(result)
            return 0

        raise ValueError(f"Unknown command: {args.command}")
    except (httpx.HTTPError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())
