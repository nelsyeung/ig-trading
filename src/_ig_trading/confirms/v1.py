from __future__ import annotations

import typing_extensions as t

from _ig_trading.model import DateTime, Model
from _ig_trading.positions.v1 import DealDirection

AffectedDealStatus = t.Literal[
    "AMENDED",
    "DELETED",
    "FULLY_CLOSED",
    "OPENED",
    "PARTIALLY_CLOSED",
]
DealConfirmationReason = t.Literal[
    "ACCOUNT_NOT_ENABLED_TO_TRADING",
    "ATTACHED_ORDER_LEVEL_ERROR",
    "ATTACHED_ORDER_TRAILING_STOP_ERROR",
    "CANNOT_CHANGE_STOP_TYPE",
    "CANNOT_REMOVE_STOP",
    "CLOSINGS_ONLY_ACCOUNT",
    "CLOSING_ONLY_TRADES_ACCEPTED_ON_THIS_MARKET",
    "CONFLICTING_ORDER",
    "CONTACT_SUPPORT_INSTRUMENT_ERROR",
    "CR_SPACING",
    "DUPLICATE_ORDER_ERROR",
    "EXCHANGE_MANUAL_OVERRIDE",
    "EXPIRY_LESS_THAN_SPRINT_MARKET_MIN_EXPIRY",
    "FINANCE_REPEAT_DEALING",
    "FORCE_OPEN_ON_SAME_MARKET_DIFFERENT_CURRENCY",
    "GENERAL_ERROR",
    "GOOD_TILL_DATE_IN_THE_PAST",
    "INSTRUMENT_NOT_FOUND",
    "INSTRUMENT_NOT_TRADEABLE_IN_THIS_CURRENCY",
    "INSUFFICIENT_FUNDS",
    "LEVEL_TOLERANCE_ERROR",
    "LIMIT_ORDER_WRONG_SIDE_OF_MARKET",
    "MANUAL_ORDER_TIMEOUT",
    "MARGIN_ERROR",
    "MARKET_CLOSED",
    "MARKET_CLOSED_WITH_EDITS",
    "MARKET_CLOSING",
    "MARKET_NOT_BORROWABLE",
    "MARKET_OFFLINE",
    "MARKET_ORDERS_NOT_ALLOWED_ON_INSTRUMENT",
    "MARKET_PHONE_ONLY",
    "MARKET_ROLLED",
    "MARKET_UNAVAILABLE_TO_CLIENT",
    "MAX_AUTO_SIZE_EXCEEDED",
    "MINIMUM_ORDER_SIZE_ERROR",
    "MOVE_AWAY_ONLY_LIMIT",
    "MOVE_AWAY_ONLY_STOP",
    "MOVE_AWAY_ONLY_TRIGGER_LEVEL",
    "NCR_POSITIONS_ON_CR_ACCOUNT",
    "OPPOSING_DIRECTION_ORDERS_NOT_ALLOWED",
    "OPPOSING_POSITIONS_NOT_ALLOWED",
    "ORDER_DECLINED",
    "ORDER_LOCKED",
    "ORDER_NOT_FOUND",
    "ORDER_SIZE_CANNOT_BE_FILLED",
    "OVER_NORMAL_MARKET_SIZE",
    "PARTIALY_CLOSED_POSITION_NOT_DELETED",
    "POSITION_ALREADY_EXISTS_IN_OPPOSITE_DIRECTION",
    "POSITION_NOT_AVAILABLE_TO_CANCEL",
    "POSITION_NOT_AVAILABLE_TO_CLOSE",
    "POSITION_NOT_FOUND",
    "REJECT_CFD_ORDER_ON_SPREADBET_ACCOUNT",
    "REJECT_SPREADBET_ORDER_ON_CFD_ACCOUNT",
    "SIZE_INCREMENT",
    "SPRINT_MARKET_EXPIRY_AFTER_MARKET_CLOSE",
    "STOP_OR_LIMIT_NOT_ALLOWED",
    "STOP_REQUIRED_ERROR",
    "STRIKE_LEVEL_TOLERANCE",
    "SUCCESS",
    "TRAILING_STOP_NOT_ALLOWED",
    "UNKNOWN",
    "WRONG_SIDE_OF_MARKET",
]
DealStatus = t.Literal["ACCEPTED", "REJECTED"]
PositionStatus = t.Literal[
    "AMENDED",
    "CLOSED",
    "DELETED",
    "OPEN",
    "PARTIALLY_CLOSED",
]


class DealConfirmation(Model):
    """Deal confirmation."""

    #: Affected deal.
    affected_deals: tuple[AffectedDeal, ...]
    #: Transaction date.
    date: DateTime
    #: Deal identifier.
    deal_id: str
    #: Deal reference.
    deal_reference: str
    #: Deal status.
    deal_status: DealStatus
    #: Deal direction.
    direction: DealDirection
    #: Instrument epic identifier.
    epic: str
    #: Instrument expiry.
    expiry: str | None
    #: Whether guaranteed stop.
    guaranteed_stop: bool
    #: Level.
    level: float | None
    #: Limit distance.
    limit_distance: float | None
    #: Limit level.
    limit_level: float | None
    #: Profit.
    profit: float | None
    #: Profit currency.
    profit_currency: str | None
    #: Describes the error (or success) condition for the specified trading
    #: operation.
    reason: DealConfirmationReason
    #: Size.
    size: float | None
    #: Position status.
    status: PositionStatus | None
    #: Stop distance.
    stop_distance: float | None
    #: Stop level.
    stop_level: float | None
    #: Whether trailing stop is enabled.
    trailing_stop: bool


class AffectedDeal(Model):
    """Affected deal."""

    #: Deal identifier.
    deal_id: str
    #: Status of the affected deal.
    status: AffectedDealStatus
