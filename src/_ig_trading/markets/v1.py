from __future__ import annotations

import typing as t

import pydantic

from _ig_trading.model import Model

InstrumentType = t.Literal[
    "BINARY",
    "BUNGEE_CAPPED",
    "BUNGEE_COMMODITIES",
    "BUNGEE_CURRENCIES",
    "BUNGEE_INDICES",
    "COMMODITIES",
    "CURRENCIES",
    "INDICES",
    "KNOCKOUTS_COMMODITIES",
    "KNOCKOUTS_CURRENCIES",
    "KNOCKOUTS_INDICES",
    "KNOCKOUTS_SHARES",
    "OPT_COMMODITIES",
    "OPT_CURRENCIES",
    "OPT_INDICES",
    "OPT_RATES",
    "OPT_SHARES",
    "RATES",
    "SECTORS",
    "SHARES",
    "SPRINT_MARKET",
    "TEST_MARKET",
    "UNKNOWN",
]
MarketOrderPreference = t.Literal[
    "AVAILABLE_DEFAULT_OFF", "AVAILABLE_DEFAULT_ON", "NOT_AVAILABLE"
]
MarketStatus = t.Literal[
    "CLOSED",  #: Closed.
    "EDITS_ONLY",  #: Open for edits.
    "OFFLINE",  #: Offline.
    "ON_AUCTION",  #: In auction mode.
    "ON_AUCTION_NO_EDITS",  #: In no-edits mode.
    "SUSPENDED",  #: Suspended.
    "TRADEABLE",  #: Open for trades.
]
TrailingStopsPreference = t.Literal["AVAILABLE", "NOT_AVAILABLE"]
Unit = t.Literal["PERCENTAGE", "POINTS"]
SizeOfTradeUnit = t.Literal["AMOUNT", "CONTRACTS", "SHARES"]


class Currency(Model):
    """Currency."""

    #: Base exchange rate.
    base_exchange_rate: float
    #: Code, to be used when placing orders.
    code: str
    #: Exchange rate.
    exchange_rate: float
    #: ``True`` if this is the default currency.
    is_default: bool
    #: Name.
    name: str | None = None
    #: Symbol, for display purposes.
    symbol: str


class DealingRule(Model):
    """Dealing rule."""

    #: Describes the dimension for a dealing rule value.
    unit: Unit
    #: Value.
    value: float


class DealingRules(Model):
    """Dealing rules."""

    #: Dealing rule for controlled risk spacing.
    controlled_risk_spacing: DealingRule
    #: Client's market order trading preference.
    market_order_preference: MarketOrderPreference
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
    trailing_stops_preference: TrailingStopsPreference | None = None


class ExpiryDetails(Model):
    """Market expiry details."""

    #: Last dealing date.
    last_dealing_date: str
    #: Settlement information.
    settlement_info: str


class MarginDepositBands(Model):
    """Margin deposit band."""

    #: The currency for this currency band factor calculation.
    currency: str | None = None
    #: Margin percentage.
    margin: float
    #: Band maximum.
    max: float | None
    #: Band minimum.
    min: float


class MarketTime(Model):
    """Market open/close time range."""

    #: Close time.
    close_time: str
    #: Open time.
    open_time: str


class OpeningHours(Model):
    """Market opening hours."""

    #: Time ranges the market is open.
    market_times: tuple[MarketTime, ...]


class RolloverDetails(Model):
    """Market rollover details."""

    #: Last rollover date.
    last_rollover_time: str
    #: Rollover info.
    rollover_info: str


class SlippageFactor(Model):
    """Slippage factor."""

    #: Unit.
    unit: str
    #: Value.
    value: float


class Instrument(Model):
    """Instrument details."""

    #: Chart code.
    chart_code: str
    #: Contract size.
    contract_size: str
    #: ``True`` if controlled risk trades are allowed.
    controlled_risk_allowed: bool
    #: Country.
    country: str | None
    #: Currencies accepted for dealing.
    currencies: tuple[Currency, ...]
    #: Instrument identifier.
    epic: str
    #: Instrument expiry period.
    expiry: str
    #: Market expiry details.
    expiry_details: ExpiryDetails | None
    #: ``True`` if force open is allowed.
    force_open_allowed: bool
    #: The limited risk premium.
    limited_risk_premium: DealingRule | None = None
    #: Lot size.
    lot_size: float
    #: Default margin requirement.
    margin: float | None = None
    #: Deposit bands.
    margin_deposit_bands: tuple[MarginDepositBands, ...]
    #: Margin requirement factor.
    margin_factor: float | None = None
    #: Describes the dimension for the margin factor.
    margin_factor_unit: Unit | None = None
    #: Market identifier.
    market_id: str
    #: Instrument name.
    name: str
    #: Reuters news code.
    news_code: str
    #: Meaning of one pip.
    one_pip_means: str
    #: Market open and close times.
    opening_hours: OpeningHours | None
    #: Market rollover details.
    rollover_details: RolloverDetails | None
    #: Slippage factor details for this market.
    slippage_factor: SlippageFactor
    #: List of special information notices.
    special_info: tuple[str, ...]
    #: For sprint markets only, the maximum value to be specified as the
    #: expiry of a sprint markets trade.
    sprint_markets_maximum_expiry_time: float | None = None
    #: For sprint markets only, the minimum value to be specified as the
    #: expiry of a sprint markets trade.
    sprint_markets_minimum_expiry_time: float | None = None
    #: ``True`` if stops and limits are allowed.
    stops_limits_allowed: bool
    #: ``True`` if streaming prices are available, i.e. the market is open
    #: and the client has appropriate permissions.
    streaming_prices_available: bool
    #: Instrument type.
    type: InstrumentType | None
    #: Unit used to qualify the size of a trade.
    unit: SizeOfTradeUnit
    #: Value of one pip.
    value_of_one_pip: float


class Snapshot(Model):
    """Market snapshot."""

    #: Bid price.
    bid: float
    #: Binary odds.
    binary_odds: float | None
    #: The number of points to add on each side of the market as an
    #: additional spread when placing a guaranteed stop trade.
    controlled_risk_extra_spread: float | None
    #: Number of decimal positions for market levels.
    decimal_places_factor: float
    #: Price delay time in minutes.
    delay_time: float
    #: Highest price of the day.
    high: float
    #: Lowest price of the day.
    low: float
    #: Describes the current status of a given market.
    market_status: MarketStatus
    #: Net price change on the day.
    net_change: float
    #: Offer price.
    offer: float
    #: Percentage price change on the day.
    percentage_change: float
    #: Multiplying factor to determine actual pip value for the levels used by
    #: the instrument.
    scaling_factor: float
    #: Price last update time (``hh:mm:ss``).
    update_time: str


class Market(Model):
    """Market details."""

    #: Dealing rules for this market.
    dealing_rules: DealingRules
    #: Instrument details.
    instrument: Instrument
    #: Market snapshot data.
    snapshot: Snapshot


class MarketOverview(Model):
    """Market overview."""

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
    #: Lot size, if given. Not returned by the ``/markets`` search-term
    #: endpoint, but present when this model is reused for
    #: ``/watchlists/{watchlist_id}``.
    lot_size: float | None = None
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
    update_time: str | None = None
    #: Time of last price update, in UTC.
    update_time_utc: str | None = pydantic.Field(
        None, alias="updateTimeUTC"
    )


class Markets(Model):
    """Markets matching a search term."""

    #: Markets matching the search term.
    markets: tuple[MarketOverview, ...]
    #: Current page number.
    page_number: int | None = None
    #: Page size.
    page_size: int | None = None
    #: Total number of pages.
    total_pages: int | None = None
    #: Total number of results.
    total_results: int | None = None
