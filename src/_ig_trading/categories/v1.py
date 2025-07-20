from __future__ import annotations

from _ig_trading.markets.v1 import InstrumentType, MarketStatus
from _ig_trading.model import Model


class Category(Model):
    """Instrument category."""

    #: Category code.
    code: str
    #: ``True`` if the category is non-tradeable.
    non_tradeable: bool


class Categories(Model):
    """Instrument categories."""

    #: Instrument categories.
    categories: tuple[Category, ...]


class Instrument(Model):
    """Instrument, within a category."""

    #: Bid price.
    bid: float | None = None
    #: Price delay time for market data, in minutes.
    delay_time: float | None = None
    #: Instrument epic identifier.
    epic: str
    #: Instrument expiry period.
    expiry: str | None = None
    #: Instrument expiry, in seconds since epoch.
    expiry_timestamp: int | None = None
    #: Highest session price.
    high: float | None = None
    #: Instrument name.
    instrument_name: str
    #: Instrument type.
    instrument_type: InstrumentType | None = None
    #: Size of an instrument lot for this instrument.
    lot_size: float | None = None
    #: Lowest session price.
    low: float | None = None
    #: Describes the current status of a given market.
    market_status: MarketStatus | None = None
    #: Net price change.
    net_change: float | None = None
    #: Offer price.
    offer: float | None = None
    #: ``True`` if the instrument can be traded OTC.
    otc_tradeable: bool | None = None
    #: Percentage price change.
    percentage_change: float | None = None
    #: How popular the instrument is, relative to other instruments.
    popularity: int | None = None
    #: Multiplying factor to determine actual pip value for the levels used by
    #: the instrument.
    scaling_factor: float | None = None
    #: The name of the instrument this one derives from, if any.
    underlying_name: str | None = None
    #: Last price update timestamp.
    update_time: str | None = None


class InstrumentsMetaData(Model):
    """Pagination details."""

    #: Current page number.
    page_number: int
    #: Items per page.
    page_size: int
    #: Total number of pages.
    total_pages: int
    #: Total number of results.
    total_results: int


class Instruments(Model):
    """Instruments, within a category."""

    #: Instruments.
    instruments: tuple[Instrument, ...]
    #: Pagination details.
    metadata: InstrumentsMetaData
