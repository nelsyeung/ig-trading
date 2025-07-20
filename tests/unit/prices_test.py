from __future__ import annotations

import datetime as dt

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock

_allowance: t.Final = {
    "allowanceExpiry": 600,
    "remainingAllowance": 9999,
    "totalAllowance": 10000,
}
_price_data: t.Final = {"ask": 1.1, "bid": 1.0, "lastTraded": None}
_price_v1: t.Final = {
    "closePrice": _price_data,
    "highPrice": _price_data,
    "lastTradedVolume": 100,
    "lowPrice": _price_data,
    "openPrice": _price_data,
    "snapshotTime": "2024-01-02T03:04:05",
}
_prices_v1: t.Final = {
    "allowance": _allowance,
    "instrumentType": "CURRENCIES",
    "prices": [_price_v1],
}
_prices_v3: t.Final = {
    "instrumentType": "CURRENCIES",
    "metadata": {"size": 1, "allowance": _allowance},
    "prices": [{**_price_v1, "snapshotTimeUTC": "2024-01-02T03:04:05"}],
}


@pytest.fixture
def async_prices(async_requester: mock.AsyncMock) -> ig.AsyncPricesResource:
    return ig.AsyncPricesResource(async_requester)


@pytest.fixture
def prices(requester: mock.MagicMock) -> ig.PricesResource:
    return ig.PricesResource(requester)


async def test_async_get_given_v3_default(
    async_prices: ig.AsyncPricesResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _prices_v3

    result: t.Final = await async_prices.get("CS.D.EURUSD.CFD.IP")

    async_requester.get.assert_awaited_once_with(
        "prices/CS.D.EURUSD.CFD.IP",
        params={
            "max": 10,
            "pageNumber": 1,
            "pageSize": 20,
            "resolution": "MINUTE",
        },
        version=3,
    )
    assert isinstance(result, ig.prices.v3.Prices)


async def test_async_get_given_v3_with_string_dates(
    async_prices: ig.AsyncPricesResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _prices_v3

    await async_prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date="2024-01-01T00:00:00",
        end_date="2024-01-02T00:00:00",
    )

    async_requester.get.assert_awaited_once_with(
        "prices/CS.D.EURUSD.CFD.IP",
        params={
            "max": 10,
            "pageNumber": 1,
            "pageSize": 20,
            "resolution": "MINUTE",
            "from": "2024-01-01T00:00:00",
            "to": "2024-01-02T00:00:00",
        },
        version=3,
    )


async def test_async_get_given_v3_with_datetime_dates(
    async_prices: ig.AsyncPricesResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _prices_v3

    await async_prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date=dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc),
        end_date=dt.datetime(2024, 1, 2, tzinfo=dt.timezone.utc),
    )

    async_requester.get.assert_awaited_once_with(
        "prices/CS.D.EURUSD.CFD.IP",
        params={
            "max": 10,
            "pageNumber": 1,
            "pageSize": 20,
            "resolution": "MINUTE",
            "from": "2024-01-01T00:00:00",
            "to": "2024-01-02T00:00:00",
        },
        version=3,
    )


async def test_async_get_given_v1_without_dates(
    async_prices: ig.AsyncPricesResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _prices_v1

    result: t.Final = await async_prices.get(
        "CS.D.EURUSD.CFD.IP", num_points=5, version=1
    )

    async_requester.get.assert_awaited_once_with(
        "prices/CS.D.EURUSD.CFD.IP/MINUTE/5", version=1
    )
    assert isinstance(result, ig.prices.v1.Prices)


async def test_async_get_given_v1_with_string_dates(
    async_prices: ig.AsyncPricesResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _prices_v1

    await async_prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date="2024:01:01-00:00:00",
        end_date="2024:01:02-00:00:00",
        version=1,
    )

    async_requester.get.assert_awaited_once_with(
        "prices/CS.D.EURUSD.CFD.IP/MINUTE?"
        "startdate=2024:01:01-00:00:00&enddate=2024:01:02-00:00:00",
        version=1,
    )


async def test_async_get_given_v1_with_datetime_dates(
    async_prices: ig.AsyncPricesResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _prices_v1

    await async_prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date=dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc),
        end_date=dt.datetime(2024, 1, 2, tzinfo=dt.timezone.utc),
        version=1,
    )

    async_requester.get.assert_awaited_once_with(
        "prices/CS.D.EURUSD.CFD.IP/MINUTE?"
        "startdate=2024:01:01-00:00:00&enddate=2024:01:02-00:00:00",
        version=1,
    )


async def test_async_get_given_v2_with_string_dates(
    async_prices: ig.AsyncPricesResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _prices_v1

    await async_prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date="2024-01-01 00:00:00",
        end_date="2024-01-02 00:00:00",
        version=2,
    )

    async_requester.get.assert_awaited_once_with(
        "prices/CS.D.EURUSD.CFD.IP/MINUTE/"
        "2024-01-01 00:00:00/2024-01-02 00:00:00",
        version=2,
    )


def test_async_get_url_given_no_epic() -> None:
    assert ig.AsyncPricesResource.get_url() == "prices"


def test_async_get_url_given_epic() -> None:
    assert (
        ig.AsyncPricesResource.get_url("CS.D.EURUSD.CFD.IP")
        == "prices/CS.D.EURUSD.CFD.IP"
    )


def test_get_given_v3_default(
    prices: ig.PricesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _prices_v3

    result: t.Final = prices.get("CS.D.EURUSD.CFD.IP")

    requester.get.assert_called_once_with(
        "prices/CS.D.EURUSD.CFD.IP",
        params={
            "max": 10,
            "pageNumber": 1,
            "pageSize": 20,
            "resolution": "MINUTE",
        },
        version=3,
    )
    assert isinstance(result, ig.prices.v3.Prices)


def test_get_given_v3_with_string_dates(
    prices: ig.PricesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _prices_v3

    prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date="2024-01-01T00:00:00",
        end_date="2024-01-02T00:00:00",
    )

    requester.get.assert_called_once_with(
        "prices/CS.D.EURUSD.CFD.IP",
        params={
            "max": 10,
            "pageNumber": 1,
            "pageSize": 20,
            "resolution": "MINUTE",
            "from": "2024-01-01T00:00:00",
            "to": "2024-01-02T00:00:00",
        },
        version=3,
    )


def test_get_given_v3_with_datetime_dates(
    prices: ig.PricesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _prices_v3

    prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date=dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc),
        end_date=dt.datetime(2024, 1, 2, tzinfo=dt.timezone.utc),
    )

    requester.get.assert_called_once_with(
        "prices/CS.D.EURUSD.CFD.IP",
        params={
            "max": 10,
            "pageNumber": 1,
            "pageSize": 20,
            "resolution": "MINUTE",
            "from": "2024-01-01T00:00:00",
            "to": "2024-01-02T00:00:00",
        },
        version=3,
    )


def test_get_given_v1_without_dates(
    prices: ig.PricesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _prices_v1

    result: t.Final = prices.get(
        "CS.D.EURUSD.CFD.IP", num_points=5, version=1
    )

    requester.get.assert_called_once_with(
        "prices/CS.D.EURUSD.CFD.IP/MINUTE/5", version=1
    )
    assert isinstance(result, ig.prices.v1.Prices)


def test_get_given_v1_with_string_dates(
    prices: ig.PricesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _prices_v1

    prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date="2024:01:01-00:00:00",
        end_date="2024:01:02-00:00:00",
        version=1,
    )

    requester.get.assert_called_once_with(
        "prices/CS.D.EURUSD.CFD.IP/MINUTE?"
        "startdate=2024:01:01-00:00:00&enddate=2024:01:02-00:00:00",
        version=1,
    )


def test_get_given_v1_with_datetime_dates(
    prices: ig.PricesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _prices_v1

    prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date=dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc),
        end_date=dt.datetime(2024, 1, 2, tzinfo=dt.timezone.utc),
        version=1,
    )

    requester.get.assert_called_once_with(
        "prices/CS.D.EURUSD.CFD.IP/MINUTE?"
        "startdate=2024:01:01-00:00:00&enddate=2024:01:02-00:00:00",
        version=1,
    )


def test_get_given_v2_with_string_dates(
    prices: ig.PricesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _prices_v1

    prices.get(
        "CS.D.EURUSD.CFD.IP",
        start_date="2024-01-01 00:00:00",
        end_date="2024-01-02 00:00:00",
        version=2,
    )

    requester.get.assert_called_once_with(
        "prices/CS.D.EURUSD.CFD.IP/MINUTE/"
        "2024-01-01 00:00:00/2024-01-02 00:00:00",
        version=2,
    )


def test_get_url_given_no_epic() -> None:
    assert ig.PricesResource.get_url() == "prices"


def test_get_url_given_epic() -> None:
    assert (
        ig.PricesResource.get_url("CS.D.EURUSD.CFD.IP")
        == "prices/CS.D.EURUSD.CFD.IP"
    )
