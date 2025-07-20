from __future__ import annotations

import datetime as dt

import pydantic
import typing_extensions as t

from _ig_trading.markets.v1 import InstrumentType, MarketStatus
from _ig_trading.model import DateTime, Model

DealDirection = t.Literal["BUY", "SELL"]


class Market(Model):
    """Market details."""

    #: Bid price.
    bid: float | None
    #: Price delay time in minutes.
    delay_time: float
    #: Instrument epic identifier.
    epic: str
    #: Instrument expiry period.
    expiry: str
    #: Highest price of the day.
    high: float | None
    #: Instrument name.
    instrument_name: str
    #: Instrument type.
    instrument_type: InstrumentType
    #: Instrument lot size.
    lot_size: float
    #: Lowest price of the day.
    low: float | None
    #: Describes the current status of a given market.
    market_status: MarketStatus
    #: Price net change.
    net_change: float | None
    #: Offer price.
    offer: float | None
    #: Percentage price change on the day.
    percentage_change: float | None
    #: Multiplying factor to determine actual pip value for the levels used by
    #: the instrument.
    scaling_factor: float
    #: ``True`` if streaming prices are available, i.e. the market is tradeable
    #: and the client holds the necessary access permissions.
    streaming_prices_available: bool
    #: Local time of last price update.
    update_time: t.Annotated[
        dt.time,
        pydantic.BeforeValidator(
            lambda v: dt.datetime.strptime(v, "%H:%M:%S")
            .astimezone(dt.datetime.now().astimezone().tzinfo)
            .time()
        ),
    ]


class Position(Model):
    """Position."""

    #: Market details.
    market: Market
    #: Position details.
    position: PositionData


class PositionData(Model):
    """Position details."""

    #: Size of the contract.
    contract_size: float
    #: Whether position is risk controlled.
    controlled_risk: bool
    #: Date the position was opened.
    created_date: DateTime
    #: Position currency ISO code.
    currency: str
    #: Deal identifier.
    deal_id: str
    #: Deal size.
    deal_size: float
    #: Deal direction.
    direction: DealDirection
    #: Limit level.
    limit_level: float | None
    #: Limited risk premium.
    limited_risk_premium: float | None
    #: Level at which the position was opened.
    open_level: float
    #: Stop level.
    stop_level: float | None
    #: Trailing step size.
    trailing_step: float | None
    #: Trailing stop distance.
    trailing_stop_distance: float | None
