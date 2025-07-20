from __future__ import annotations

import typing as t

import pydantic

from _ig_trading.markets.v1 import InstrumentType, MarketStatus
from _ig_trading.model import Model
from _ig_trading.positions.v1 import DealDirection

WorkingOrderRequestType = t.Literal["LIMIT_ORDER", "STOP_ORDER"]


class Market(Model):
    """Market details."""

    #: Bid price.
    bid: float
    #: Instrument price delay, in minutes.
    delay_time: float
    #: Instrument epic identifier.
    epic: str
    #: Exchange identifier for this instrument.
    exchange_id: str
    #: Instrument expiry period.
    expiry: str
    #: High price.
    high: float
    #: Instrument name.
    instrument_name: str
    #: Instrument type.
    instrument_type: InstrumentType
    #: Instrument lot size.
    lot_size: float
    #: Low price.
    low: float
    #: Describes the current status of a given market.
    market_status: MarketStatus
    #: Price net change.
    net_change: float
    #: Offer price.
    offer: float
    #: Price percentage change.
    percentage_change: float
    #: Multiplying factor to determine actual pip value for the levels used by
    #: the instrument.
    scaling_factor: float
    #: ``True`` if streaming prices are available.
    streaming_prices_available: bool
    #: Local time of last instrument price update.
    update_time: str
    #: Time of last instrument price update, in UTC. Not always present.
    update_time_utc: str | None = pydantic.Field(
        None, alias="updateTimeUTC"
    )


class WorkingOrderData(Model):
    """Working order details."""

    #: Limit level.
    contingent_limit: float | None
    #: Stop level.
    contingent_stop: float | None
    #: ``True`` if controlled risk.
    controlled_risk: bool
    #: Local date and time when the order was created. Format is
    #: ``yyyy/MM/dd kk:mm:ss:SSS``.
    created_date: str
    #: Currency ISO code.
    currency_code: str
    #: Deal identifier.
    deal_id: str
    #: Deal direction.
    direction: DealDirection
    #: ``True`` if this is a DMA working order.
    dma: bool
    #: Instrument epic identifier.
    epic: str
    #: Working order expiry date and time, if set. Format is
    #: ``dd/MM/yy HH:mm``.
    good_till: str | None
    #: Limited risk premium.
    limited_risk_premium: float | None
    #: Price at which to execute the trade.
    level: float
    #: Working order request type.
    request_type: WorkingOrderRequestType
    #: Order size.
    size: float
    #: Trailing stop distance.
    trailing_stop_distance: float | None
    #: Trailing stop increment.
    trailing_stop_increment: float | None
    #: Trailing trigger distance.
    trailing_trigger_distance: float | None
    #: Trailing trigger increment.
    trailing_trigger_increment: float | None


class WorkingOrder(Model):
    """Working order."""

    #: Market details.
    market_data: Market
    #: Working order details.
    working_order_data: WorkingOrderData


class WorkingOrders(Model):
    """Working orders."""

    #: Working orders.
    working_orders: tuple[WorkingOrder, ...]
