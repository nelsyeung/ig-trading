from __future__ import annotations

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


@pytest.mark.parametrize(
    ("version", "expected"),
    [(1, ig.markets.v1.Market), (2, ig.markets.v2.Market)],
)
async def test_async_list(
    async_markets: ig.AsyncMarketsResource,
    expected: type,
    version: t.Literal[1, 2],
) -> None:
    assert all(
        isinstance(market, expected)
        for market in await async_markets.list([_epic], version=version)
    )


async def test_async_list_given_both_epics_and_search_term() -> None:
    with pytest.raises(ValueError, match="Exactly one"):
        await ig.AsyncMarketsResource().list(  # type: ignore[call-overload]
            (_epic,), search_term="AUDUSD"
        )


async def test_async_list_given_neither_epics_nor_search_term() -> None:
    with pytest.raises(ValueError, match="Exactly one"):
        await ig.AsyncMarketsResource().list()  # type: ignore[call-overload]


async def test_async_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncMarketsResource().list([_epic])


@pytest.mark.parametrize("version", [1, 2], ids=("v1", "v2"))
async def test_async_list_given_search_term(
    async_markets: ig.AsyncMarketsResource, version: t.Literal[1, 2]
) -> None:
    result: t.Final = await async_markets.list(
        search_term="AUDUSD", version=version
    )
    assert result
    assert all(
        isinstance(market, ig.markets.v1.MarketOverview) for market in result
    )


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.markets.v1.Market),
        (2, ig.markets.v2.Market),
        (3, ig.markets.v3.Market),
        (4, ig.markets.v4.Market),
    ],
)
async def test_async_get(
    async_markets: ig.AsyncMarketsResource,
    expected: type,
    version: t.Literal[1, 2, 3, 4],
) -> None:
    assert isinstance(
        await async_markets.get(_epic, version=version), expected
    )


@pytest.mark.parametrize(
    ("version", "expected"),
    [(1, ig.markets.v1.Market), (2, ig.markets.v2.Market)],
)
def test_list(
    expected: type, markets: ig.MarketsResource, version: t.Literal[1, 2]
) -> None:
    assert all(
        isinstance(market, expected)
        for market in markets.list([_epic], version=version)
    )


def test_list_given_both_epics_and_search_term() -> None:
    with pytest.raises(ValueError, match="Exactly one"):
        ig.MarketsResource().list(  # type: ignore[call-overload]
            (_epic,), search_term="AUDUSD"
        )


def test_list_given_neither_epics_nor_search_term() -> None:
    with pytest.raises(ValueError, match="Exactly one"):
        ig.MarketsResource().list()  # type: ignore[call-overload]


def test_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.MarketsResource().list([_epic])


@pytest.mark.parametrize("version", [1, 2], ids=("v1", "v2"))
def test_list_given_search_term(
    markets: ig.MarketsResource, version: t.Literal[1, 2]
) -> None:
    result: t.Final = markets.list(search_term="AUDUSD", version=version)
    assert result
    assert all(
        isinstance(market, ig.markets.v1.MarketOverview) for market in result
    )


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.markets.v1.Market),
        (2, ig.markets.v2.Market),
        (3, ig.markets.v3.Market),
        (4, ig.markets.v4.Market),
    ],
)
def test_get(
    expected: type,
    markets: ig.MarketsResource,
    version: t.Literal[1, 2, 3, 4],
) -> None:
    assert isinstance(markets.get(_epic, version=version), expected)
