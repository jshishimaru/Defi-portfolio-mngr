"""Entry point for the basic crypto uAgent."""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from uagents import Agent
from uagents_adapter.mcp.adapter import MCPServerAdapter

if __package__ in {None, ""}:
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    __package__ = "basic_agent"

from .mcp_server import mcp

load_dotenv()

ASI_ONE_API_KEY = os.getenv("ASI_ONE_API_KEY")
if not ASI_ONE_API_KEY:
    raise ValueError("ASI_ONE_API_KEY environment variable is required")

mcp_adapter = MCPServerAdapter(
    mcp_server=mcp,
    asi1_api_key=ASI_ONE_API_KEY,
    model="asi1-mini",
)

agent = Agent(
    name="basic-crypto-agent",
    port=8000,
    seed="BASIC-CRYPTO",
    mailbox=True,
)

print(f"Agent address: {agent.address}")

for protocol in mcp_adapter.protocols:
    agent.include(protocol, publish_manifest=True)


if __name__ == "__main__":
    mcp_adapter.run(agent)
