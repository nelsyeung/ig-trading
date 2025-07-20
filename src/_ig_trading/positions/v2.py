from __future__ import annotations

import datetime as dt

import pydantic
import typing_extensions as t

from _ig_trading.model import DateTime, Model
from _ig_trading.positions import v1


class Market(v1.Market):
    """Market details."""

    #: Time of last price update.
    update_time_utc: t.Annotated[
        dt.time,
        pydantic.BeforeValidator(
            lambda v: dt.datetime.strptime(v, "%H:%M:%S")
            .replace(tzinfo=dt.timezone.utc)
            .time()
        ),
    ] = pydantic.Field(alias="updateTimeUTC")


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
    #: Date the position was opened.
    created_date_utc: DateTime = pydantic.Field(alias="createdDateUTC")
    #: Position currency ISO code.
    currency: str
    #: Deal identifier.
    deal_id: str
    #: Deal reference.
    deal_reference: str
    #: Deal direction.
    direction: v1.DealDirection
    #: Level at which the position was opened.
    level: float
    #: Limit level.
    limit_level: float | None
    #: Limited risk premium.
    limited_risk_premium: float | None
    #: Deal size.
    size: float
    #: Stop level.
    stop_level: float | None
    #: Trailing step size.
    trailing_step: float | None
    #: Trailing stop distance.
    trailing_stop_distance: float | None
