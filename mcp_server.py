"""Minimal FastMCP server exposing basic crypto price tools."""
from __future__ import annotations

from typing import Iterable

from mcp.server.fastmcp import FastMCP

from .market import get_coin_price, get_multiple_coin_prices, list_supported_coins

mcp = FastMCP("basic-crypto-agent")


@mcp.tool()
async def fetch_coin_price(coin_symbol: str) -> str:
    """Return the latest USD price for the requested coin symbol."""
    price = await get_coin_price(coin_symbol)
    return f"{coin_symbol.upper()} price: ${price:,.2f} USD"


@mcp.tool()
async def fetch_multiple_prices(coin_symbols: Iterable[str]) -> dict:
    """Return USD prices for multiple coin symbols."""
    prices = await get_multiple_coin_prices(list(coin_symbols))
    return {symbol: f"${value:,.2f}" for symbol, value in prices.items()}


@mcp.tool()
def supported_coins() -> dict:
    """List coin symbols recognised by the agent."""
    return list_supported_coins()
