from __future__ import annotations

import contextlib

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

_epic: t.Final = "CS.D.AUDUSD.CFD.IP"


@pytest.fixture
def async_watchlists(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncWatchlistsResource:
    return ig.AsyncWatchlistsResource(async_requester)


@pytest.fixture
def watchlists(requester: ig.APIRequester) -> ig.WatchlistsResource:
    return ig.WatchlistsResource(requester)


@pytest.fixture
async def async_create_watchlist(
    async_watchlists: ig.AsyncWatchlistsResource,
) -> AsyncIterator[str]:
    result: t.Final = await async_watchlists.create(
        "ig_trading_test", epics=[_epic]
    )
    try:
        yield result.watchlist_id
    finally:
        with contextlib.suppress(ig.APIError):
            await async_watchlists.delete(result.watchlist_id)


@pytest.fixture
def create_watchlist(
    watchlists: ig.WatchlistsResource,
) -> Iterator[str]:
    result: t.Final = watchlists.create("ig_trading_test", epics=[_epic])
    try:
        yield result.watchlist_id
    finally:
        with contextlib.suppress(ig.APIError):
            watchlists.delete(result.watchlist_id)


async def test_async_create(async_create_watchlist: str) -> None:
    assert async_create_watchlist


async def test_async_delete(
    async_create_watchlist: str, async_watchlists: ig.AsyncWatchlistsResource
) -> None:
    assert await async_watchlists.delete(async_create_watchlist) == "SUCCESS"
    assert not any(
        watchlist.id == async_create_watchlist
        for watchlist in await async_watchlists.list()
    )


async def test_async_delete_market(
    async_create_watchlist: str, async_watchlists: ig.AsyncWatchlistsResource
) -> None:
    assert (
        await async_watchlists.delete(async_create_watchlist, _epic)
    ) == "SUCCESS"
    markets: t.Final = await async_watchlists.get(async_create_watchlist)
    assert not any(market.epic == _epic for market in markets)


async def test_async_list(
    async_create_watchlist: str, async_watchlists: ig.AsyncWatchlistsResource
) -> None:
    assert any(
        watchlist.id == async_create_watchlist
        for watchlist in await async_watchlists.list()
    )


async def test_async_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncWatchlistsResource().list()


async def test_async_get(
    async_create_watchlist: str, async_watchlists: ig.AsyncWatchlistsResource
) -> None:
    markets: t.Final = await async_watchlists.get(async_create_watchlist)
    assert any(market.epic == _epic for market in markets)


async def test_async_update(
    async_create_watchlist: str, async_watchlists: ig.AsyncWatchlistsResource
) -> None:
    epic: t.Final = "CS.D.EURGBP.CFD.IP"
    assert (
        await async_watchlists.update(async_create_watchlist, epic=epic)
    ) == "SUCCESS"
    markets: t.Final = await async_watchlists.get(async_create_watchlist)
    assert any(market.epic == epic for market in markets)


def test_create(create_watchlist: str) -> None:
    assert create_watchlist


def test_delete(
    create_watchlist: str, watchlists: ig.WatchlistsResource
) -> None:
    assert watchlists.delete(create_watchlist) == "SUCCESS"
    assert not any(
        watchlist.id == create_watchlist for watchlist in watchlists.list()
    )


def test_delete_market(
    create_watchlist: str, watchlists: ig.WatchlistsResource
) -> None:
    assert (watchlists.delete(create_watchlist, _epic)) == "SUCCESS"
    markets: t.Final = watchlists.get(create_watchlist)
    assert not any(market.epic == _epic for market in markets)


def test_list(
    create_watchlist: str, watchlists: ig.WatchlistsResource
) -> None:
    assert any(
        watchlist.id == create_watchlist for watchlist in watchlists.list()
    )


def test_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.WatchlistsResource().list()


def test_get(
    create_watchlist: str, watchlists: ig.WatchlistsResource
) -> None:
    markets: t.Final = watchlists.get(create_watchlist)
    assert any(market.epic == _epic for market in markets)


def test_update(
    create_watchlist: str, watchlists: ig.WatchlistsResource
) -> None:
    epic: t.Final = "CS.D.EURGBP.CFD.IP"
    assert (watchlists.update(create_watchlist, epic=epic)) == "SUCCESS"
    markets: t.Final = watchlists.get(create_watchlist)
    assert any(market.epic == epic for market in markets)
