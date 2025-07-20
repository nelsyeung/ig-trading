from __future__ import annotations

import typing as t

from _ig_trading.model import Model

ActionStatus = t.Literal["ACCEPT", "MANUAL", "NOT_SET", "REJECT"]
TransactionType = t.Literal["ALL", "ALL_DEAL", "DEPOSIT", "WITHDRAWAL"]


class Activity(Model):
    """Account activity item."""

    #: The action status of the activity item.
    action_status: ActionStatus
    #: The high-level activity description, e.g. ``"Order"``.
    activity: str
    #: Activity history identifier.
    activity_history_id: str
    #: The channel the activity occurred on, e.g. ``"WEB"`` or ``"Mobile"``.
    channel: str
    #: The currency, e.g. a pound symbol.
    currency: str
    #: The date of the activity item, in ``DD/MM/YY`` format.
    date: str
    #: Deal identifier.
    deal_id: str
    #: Instrument epic identifier.
    epic: str
    #: The market level that the activity item occurred at.
    level: str
    #: The limit level of the activity item, if any.
    limit: str
    #: The market name of the activity item.
    market_name: str
    #: The period of the activity item.
    period: str
    #: The description of the result of the activity.
    result: str
    #: The size of the activity item.
    size: str
    #: The stop level of the activity item, if any.
    stop: str
    #: The type of stop, if applicable: ``"G"`` for guaranteed, ``"N"`` for
    #: non-guaranteed, or ``"T(<size>)"`` for a trailing stop.
    stop_type: str
    #: The time the activity item occurred, in ``hh:mm`` format.
    time: str


class Activities(Model):
    """Account activities."""

    #: Account activities.
    activities: tuple[Activity, ...]


class Transaction(Model):
    """Transaction."""

    #: ``True`` if this was a cash transaction.
    cash_transaction: bool
    #: Level at which the order was closed.
    close_level: str
    #: Order currency.
    currency: str
    #: Transaction date, in ``dd-MMM-yyyy`` format.
    date: str
    #: Instrument name.
    instrument_name: str
    #: Level at which the order was opened.
    open_level: str
    #: Period, in milliseconds.
    period: str
    #: Profit and loss.
    profit_and_loss: str
    #: Reference.
    reference: str
    #: Formatted order size, including the direction (``+`` for buy, ``-``
    #: for sell).
    size: str
    #: Transaction type.
    transaction_type: str


class Transactions(Model):
    """Transactions."""

    #: Transactions.
    transactions: tuple[Transaction, ...]
