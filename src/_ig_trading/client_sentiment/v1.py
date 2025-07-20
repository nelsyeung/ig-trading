from __future__ import annotations

from _ig_trading.model import Model


class Sentiment(Model):
    """Client sentiment for a market."""

    #: Percentage long positions.
    long_position_percentage: float
    #: Market identifier.
    market_id: str
    #: Percentage short positions.
    short_position_percentage: float
