# Crypto MCP Agent

An opinionated reference agent for DeFi/crypto portfolio tooling, built on top of the [uAgents](https://github.com/FetchAI/uAgents) framework and the [FastMCP](https://github.com/modelcontextprotocol/fastmcp) server runtime. It exposes curated MCP tools that deliver live market data from CoinGecko and can be embedded inside Model Context Protocol (MCP) clients such as AI copilots.

---

## ✨ Features

- **MCP-native tools** that fetch single or batched coin prices and list supported assets.
- **Live market data** using CoinGecko's `/simple/price` API with graceful error handling.
- **uAgents integration** that registers the FastMCP server and publishes tool manifests automatically.
- **Environment-driven configuration** so sensitive keys (e.g., `ASI_ONE_API_KEY`) stay outside source control.

---

## 🏗 Architecture at a Glance

| Module | Responsibility |
| ------ | -------------- |
| `basic_agent/agent.py` | Bootstraps the uAgent, loads environment variables, and wires the MCP adapter. |
| `basic_agent/mcp_server.py` | Defines MCP tools using `FastMCP` and exposes them to the agent. |
| `basic_agent/market.py` | Async helpers that talk to CoinGecko and normalize symbol-to-ID mapping. |

**Data Flow**
1. The agent process starts, loads `ASI_ONE_API_KEY`, and creates a `FastMCP` adapter.
2. The MCP adapter registers each tool defined in `mcp_server.py` with the uAgent runtime.
3. MCP clients invoke tools (e.g., `fetch_coin_price`), which in turn call into `market.py` helpers.
4. Market helpers query CoinGecko and return price data back through the MCP tool response.

---

## ✅ Prerequisites

- Python **3.12** (matching the bundled virtual environment)
- A valid `ASI_ONE_API_KEY` credential for the MCP adapter
- Internet access for CoinGecko API requests

---

## 🚀 Quickstart

```bash
# Clone the repository
git clone https://github.com/jshishimaru/Defi-portfolio-mngr
cd Defi-portfolio-mngr/basic_agent

# Create and activate the virtualenv (Linux/macOS)
python3 -m venv .venv
source .venv/bin/activate

# Install runtime dependencies
pip install -r requirements.txt

# Provide your API key
cp .env .env.backup 2>/dev/null || true
cat <<'EOF' > .env
ASI_ONE_API_KEY=replace-with-your-key
EOF

# Launch the agent (preferred entrypoint)
python -m basic_agent.agent
```











