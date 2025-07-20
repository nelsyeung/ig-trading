from __future__ import annotations

import typing as t

import pydantic

from _ig_trading.model import Model
from _ig_trading.positions.v1 import DealDirection
from _ig_trading.working_orders.v1 import Market

WorkingOrderType = t.Literal["LIMIT", "STOP"]
TimeInForce = t.Literal["GOOD_TILL_CANCELLED", "GOOD_TILL_DATE"]


class WorkingOrderData(Model):
    """Working order details."""

    #: Local date and time when the order was created. Format is
    #: ``yyyy/MM/dd kk:mm:ss:SSS``.
    created_date: str
    #: Date and time when the order was created, in UTC.
    created_date_utc: str = pydantic.Field(alias="createdDateUTC")
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
    #: The date and time the working order will be deleted if not triggered
    #: till then. Format is ``yyyy/MM/dd hh:mm``.
    good_till_date: str | None
    #: The date and time the working order will be deleted if not triggered
    #: till then.
    good_till_date_iso: str | None = pydantic.Field(alias="goodTillDateISO")
    #: ``True`` if controlled risk.
    guaranteed_stop: bool
    #: Limit distance.
    limit_distance: float | None
    #: Limited risk premium.
    limited_risk_premium: float | None
    #: Price at which to execute the trade.
    order_level: float
    #: Order size.
    order_size: float
    #: Working order type.
    order_type: WorkingOrderType
    #: Stop distance.
    stop_distance: float | None
    #: Describes the type of time in force for a given order.
    time_in_force: TimeInForce


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
