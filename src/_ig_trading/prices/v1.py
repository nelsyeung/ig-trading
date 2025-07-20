from __future__ import annotations

import typing_extensions as t

from _ig_trading.markets.v1 import InstrumentType
from _ig_trading.model import DateTime, Model

PriceResolution = t.Literal[
    "HOUR",  #: 1 hour.
    "HOUR_2",  #: 2 hours.
    "HOUR_3",  #: 3 hours.
    "HOUR_4",  #: 4 hours.
    "MINUTE",  #: 1 minute.
    "MINUTE_10",  #: 10 minutes.
    "MINUTE_15",  #: 15 minutes.
    "MINUTE_2",  #: 2 minutes.
    "MINUTE_3",  #: 3 minutes.
    "MINUTE_30",  #: 30 minutes.
    "MINUTE_5",  #: 5 minutes.
    "MONTH",  #: 1 month.
    "SECOND",  #: 1 second.
    "WEEK",  #: 1 week.
]


class Allowance(Model):
    """Allowance."""

    #: The number of seconds till the current allowance period will end and
    #: the remaining allowance field is reset.
    allowance_expiry: int
    #: The number of data points still available to fetch within the current
    #: allowance period.
    remaining_allowance: int
    #: The number of data points the API key and account combination is
    #: allowed to fetch in any given allowance period.
    total_allowance: int


class PriceData(Model):
    """Price data."""

    #: Ask price.
    ask: float | None
    #: Bid price.
    bid: float | None
    #: Last traded price. This will generally be ``None`` for non
    #: exchange-traded instruments.
    last_traded: float | None


class Price(Model):
    """Price."""

    #: Closing price.
    close_price: PriceData
    #: Highest price.
    high_price: PriceData
    #: Last traded volume. This will generally be ``None`` for non
    #: exchange-traded instruments.
    last_traded_volume: int
    #: Lowest price.
    low_price: PriceData
    #: Opening price.
    open_price: PriceData
    #: Snapshot local time.
    snapshot_time: DateTime


class Prices(Model):
    """Prices."""

    #: Allowance details.
    allowance: Allowance
    #: Instrument type.
    instrument_type: InstrumentType
    #: Price points.
    prices: tuple[Price, ...]
