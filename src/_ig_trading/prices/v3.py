from __future__ import annotations

import datetime as dt

import pydantic
import typing_extensions as t

from _ig_trading.markets.v1 import InstrumentType
from _ig_trading.model import DateTime, Model
from _ig_trading.prices import v1
from _ig_trading.prices.v1 import Allowance


class PageData(pydantic.BaseModel):
    """Pagination details."""

    #: Page number.
    page_number: int
    #: Page size.
    page_size: int
    #: Total number of pages.
    total_pages: int


class PricesMetaData(pydantic.BaseModel):
    """Prices response metadata."""

    #: Number of price points returned.
    size: int
    #: Allowance details.
    allowance: Allowance
    #: Pagination details.
    page_data: PageData | None = None


class Price(v1.Price):
    """Price."""

    #: Snapshot time, in UTC.
    snapshot_time_utc: t.Annotated[
        DateTime,
        pydantic.AfterValidator(lambda v: v.replace(tzinfo=dt.timezone.utc)),
    ] = pydantic.Field(alias="snapshotTimeUTC")


class Prices(Model):
    """Prices."""

    #: Instrument type.
    instrument_type: InstrumentType
    #: Metadata about this response.
    metadata: PricesMetaData
    #: Price points.
    prices: tuple[Price, ...]
