from __future__ import annotations

import datetime as dt

import pytest
import typing_extensions as t

import ig_trading as ig

_epic: t.Final = "CS.D.AUDUSD.CFD.IP"


@pytest.fixture
def async_markets(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncMarketsResource:
    return ig.AsyncMarketsResource(async_requester)


@pytest.fixture
def markets(requester: ig.APIRequester) -> ig.MarketsResource:
    return ig.MarketsResource(requester)


@pytest.fixture
def async_prices(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncPricesResource:
    return ig.AsyncPricesResource(async_requester)


@pytest.fixture
def prices(requester: ig.APIRequester) -> ig.PricesResource:
    return ig.PricesResource(requester)


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.prices.v1.Prices),
        (2, ig.prices.v2.Prices),
        (3, ig.prices.v3.Prices),
    ],
    ids=("v1", "v2", "v3"),
)
async def test_async_get(
    async_prices: ig.AsyncPricesResource,
    expected: type,
    version: t.Literal[1, 2, 3],
) -> None:
    assert isinstance(await async_prices.get(_epic, version=version), expected)


async def test_async_get_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncPricesResource().get(_epic, version=1)


@pytest.mark.parametrize("version", [1, 3], ids=("v1", "v3"))
async def test_async_get_num_points(
    async_prices: ig.AsyncPricesResource, version: t.Literal[1, 3]
) -> None:
    num_points: t.Final = 3
    price: t.Final = await async_prices.get(
        _epic, version=version, num_points=num_points
    )
    assert len(price.prices) == num_points


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.prices.v1.Prices),
        (2, ig.prices.v2.Prices),
        (3, ig.prices.v3.Prices),
    ],
    ids=("v1", "v2", "v3"),
)
async def test_async_get_given_datetime_date_range(
    async_markets: ig.AsyncMarketsResource,
    async_prices: ig.AsyncPricesResource,
    expected: type,
    version: t.Literal[1, 2, 3],
) -> None:
    market: t.Final = await async_markets.get(_epic, version=1)

    if market.snapshot.market_status != "TRADEABLE":
        pytest.skip(
            f"{_epic} isn't tradeable right now "
            f"(status: {market.snapshot.market_status})"
        )

    end_date: t.Final = dt.datetime.now(dt.timezone.utc)
    start_date: t.Final = end_date - dt.timedelta(hours=6)

    price: t.Final = await async_prices.get(
        _epic,
        version=version,
        start_date=start_date,
        end_date=end_date,
    )

    assert isinstance(price, expected)
    assert price.prices
    for entry in price.prices:
        assert (
            start_date - dt.timedelta(minutes=1)
            <= entry.snapshot_time
            <= end_date + dt.timedelta(minutes=1)
        )


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.prices.v1.Prices),
        (2, ig.prices.v2.Prices),
        (3, ig.prices.v3.Prices),
    ],
    ids=("v1", "v2", "v3"),
)
def test_get(
    expected: type, prices: ig.PricesResource, version: t.Literal[1, 2, 3]
) -> None:
    assert isinstance(prices.get(_epic, version=version), expected)


def test_get_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.PricesResource().get(_epic, version=1)


@pytest.mark.parametrize("version", [1, 3], ids=("v1", "v3"))
def test_get_num_points(
    prices: ig.PricesResource, version: t.Literal[1, 3]
) -> None:
    num_points: t.Final = 3
    price: t.Final = prices.get(_epic, version=version, num_points=num_points)
    assert len(price.prices) == num_points


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.prices.v1.Prices),
        (2, ig.prices.v2.Prices),
        (3, ig.prices.v3.Prices),
    ],
    ids=("v1", "v2", "v3"),
)
def test_get_given_datetime_date_range(
    expected: type,
    markets: ig.MarketsResource,
    prices: ig.PricesResource,
    version: t.Literal[1, 2, 3],
) -> None:
    market: t.Final = markets.get(_epic, version=1)

    if market.snapshot.market_status != "TRADEABLE":
        pytest.skip(
            f"{_epic} isn't tradeable right now "
            f"(status: {market.snapshot.market_status})"
        )

    end_date: t.Final = dt.datetime.now(dt.timezone.utc)
    start_date: t.Final = end_date - dt.timedelta(hours=6)

    price: t.Final = prices.get(
        _epic,
        version=version,
        start_date=start_date,
        end_date=end_date,
    )

    assert isinstance(price, expected)
    assert price.prices
    for entry in price.prices:
        assert (
            start_date - dt.timedelta(minutes=1)
            <= entry.snapshot_time
            <= end_date + dt.timedelta(minutes=1)
        )
