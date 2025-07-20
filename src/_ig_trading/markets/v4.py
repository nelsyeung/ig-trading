from __future__ import annotations

import pydantic

from _ig_trading.markets.v1 import (
    Currency,
    DealingRule,
    InstrumentType,
    MarketStatus,
    SizeOfTradeUnit,
    TrailingStopsPreference,
)
from _ig_trading.model import Model


class DealingRules(Model):
    """Dealing rules."""

    #: Dealing rule for controlled risk spacing.
    controlled_risk_spacing: DealingRule
    #: Dealing rule for the maximum stop or limit distance.
    max_stop_or_limit_distance: DealingRule
    #: Dealing rule for the minimum controlled risk stop distance.
    min_controlled_risk_stop_distance: DealingRule
    #: Dealing rule for the minimum deal size.
    min_deal_size: DealingRule
    #: Dealing rule for the minimum normal stop or limit distance.
    min_normal_stop_or_limit_distance: DealingRule
    #: Dealing rule for the minimum step distance.
    min_step_distance: DealingRule
    #: Trailing stops trading preference for the specified market.
    trailing_stops_preference: TrailingStopsPreference


class Instrument(Model):
    """Instrument details."""

    #: Chart code.
    chart_code: str
    #: Contract size.
    contract_size: str
    #: Country.
    country: str | None
    #: Currencies accepted for dealing.
    currencies: tuple[Currency, ...]
    #: Instrument identifier.
    epic: str
    #: Instrument expiry period.
    expiry: str
    #: The limited risk premium.
    limited_risk_premium: DealingRule | None = None
    #: Lot size.
    lot_size: float
    #: Market identifier.
    market_id: str
    #: Instrument name.
    name: str
    #: Reuters news code.
    news_code: str
    #: ``True`` if streaming prices are available, i.e. the market is open
    #: and the client has appropriate permissions.
    streaming_prices_available: bool
    #: ``True`` if limit orders are allowed.
    limit_allowed: bool
    #: ``True`` if stops are allowed.
    stop_allowed: bool
    #: Instrument type.
    type: InstrumentType
    #: Unit used to qualify the size of a trade.
    unit: SizeOfTradeUnit
    #: Value of one pip.
    value_of_one_pip: float


class CurrencyLadder(Model):
    """Currency ladder."""

    #: List of ask price orders.
    ask_sizes: list[int]
    #: List of bid price orders.
    bid_sizes: list[int]
    #: Currency.
    currency: str


class PriceLadder(Model):
    """Price ladder rung."""

    #: Ask price.
    ask: str
    #: Bid price.
    bid: str


class Snapshot(Model):
    """Market snapshot."""

    #: Price ladder, by currency.
    currency_ladders: tuple[CurrencyLadder, ...] | None
    #: Number of decimal positions for market levels.
    decimal_places_factor: float
    #: Price delay time in minutes.
    delay_time: float
    #: Highest price of the day.
    high: float | None
    #: Lowest price of the day.
    low: float | None
    #: Describes the current status of a given market.
    market_status: MarketStatus
    #: Net price change on the day.
    net_change: float | None
    #: Percentage price change on the day.
    percentage_change: float | None
    #: Price ladder.
    price_ladder: tuple[PriceLadder, ...]
    #: Multiplying factor to determine actual pip value for the levels used by
    #: the instrument.
    scaling_factor: float
    #: Time (in seconds since 1970) of last price update, in UTC.
    update_timestamp_utc: int | None = pydantic.Field(
        alias="updateTimestampUTC"
    )


class Market(Model):
    """Market details."""

    #: Dealing rules for this market.
    dealing_rules: DealingRules
    #: Instrument details.
    instrument: Instrument
    #: Market snapshot data.
    snapshot: Snapshot
