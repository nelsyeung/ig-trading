from __future__ import annotations

import typing as t

from _ig_trading.model import Model

Status = t.Literal["DISABLED", "ENABLED", "REVOKED"]


class Application(Model):
    """Client-owned application."""

    #: API key.
    api_key: str
    #: ``True`` if access to equity prices is permitted.
    allow_equities: bool
    #: ``True`` if quote orders are permitted.
    allow_quote_orders: bool
    #: Per account request per minute allowance.
    allowance_account_overall: float
    #: Per account trading request per minute allowance.
    allowance_account_trading: float
    #: Historical price data data points per minute allowance.
    allowance_account_historical_data: float
    #: Overall request per minute allowance.
    allowance_application_overall: float
    #: Concurrent subscription limit per Lightstreamer connection.
    concurrent_subscriptions_limit: float
    #: Application creation date.
    created_date: str
    #: Application name.
    name: str
    #: Application status.
    status: Status
