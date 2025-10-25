"""Minimal asynchronous helpers for fetching cryptocurrency prices."""
from __future__ import annotations

from typing import Dict, Iterable

import httpx

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
SUPPORTED_COINS = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
    "MATIC": "matic-network",
    "ADA": "cardano",
    "DOT": "polkadot",
    "LINK": "chainlink",
    "AVAX": "avalanche-2",
    "UNI": "uniswap",
    "USDC": "usd-coin",
    "USDT": "tether",
}


async def get_coin_price(coin_symbol: str, vs_currency: str = "usd") -> float:
    """Return the latest price for a single coin."""
    coin_id = SUPPORTED_COINS.get(coin_symbol.upper())
    if not coin_id:
        raise ValueError(f"Unsupported coin symbol: {coin_symbol}")

    async with httpx.AsyncClient(base_url=COINGECKO_BASE_URL, timeout=10) as client:
        response = await client.get(
            "/simple/price",
            params={"ids": coin_id, "vs_currencies": vs_currency},
        )
        response.raise_for_status()
        data = response.json()

    price = data.get(coin_id, {}).get(vs_currency)
    if price is None:
        raise RuntimeError(f"Price for {coin_symbol} not available from CoinGecko")

    return float(price)


async def get_multiple_coin_prices(
    coin_symbols: Iterable[str],
    vs_currency: str = "usd",
) -> Dict[str, float]:
    """Return a mapping of coin symbols to their latest prices."""
    normalized = []
    ids = []
    for symbol in coin_symbols:
        symbol_upper = symbol.upper()
        coin_id = SUPPORTED_COINS.get(symbol_upper)
        if coin_id:
            normalized.append(symbol_upper)
            ids.append(coin_id)

    if not ids:
        raise ValueError("No supported coin symbols were provided")

    async with httpx.AsyncClient(base_url=COINGECKO_BASE_URL, timeout=10) as client:
        response = await client.get(
            "/simple/price",
            params={"ids": ",".join(ids), "vs_currencies": vs_currency},
        )
        response.raise_for_status()
        data = response.json()

    prices: Dict[str, float] = {}
    for symbol, coin_id in zip(normalized, ids):
        price = data.get(coin_id, {}).get(vs_currency)
        if price is not None:
            prices[symbol] = float(price)

    if not prices:
        raise RuntimeError("CoinGecko did not return prices for the requested symbols")

    return prices


def list_supported_coins() -> Dict[str, str]:
    """Return the supported symbol-to-id mapping."""
    return dict(SUPPORTED_COINS)
