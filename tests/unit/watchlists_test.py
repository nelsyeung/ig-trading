from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock


_market_overview: t.Final = {
    "bid": 1.1,
    "delayTime": 0,
    "epic": "CS.D.EURUSD.CFD.IP",
    "expiry": "-",
    "high": 1.2,
    "instrumentName": "EUR/USD",
    "instrumentType": "CURRENCIES",
    "low": 1.0,
    "marketStatus": "TRADEABLE",
    "netChange": 0.0,
    "offer": 1.1,
    "percentageChange": 0.0,
    "scalingFactor": 1,
    "streamingPricesAvailable": True,
}
_watchlist: t.Final = {
    "defaultSystemWatchlist": False,
    "deleteable": True,
    "editable": True,
    "id": "1",
    "name": "My Watchlist",
}


@pytest.fixture
def async_watchlists(
    async_requester: mock.AsyncMock,
) -> ig.AsyncWatchlistsResource:
    return ig.AsyncWatchlistsResource(async_requester)


@pytest.fixture
def watchlists(requester: mock.MagicMock) -> ig.WatchlistsResource:
    return ig.WatchlistsResource(requester)


async def test_async_create_given_epics(
    async_watchlists: ig.AsyncWatchlistsResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.post.return_value = {
        "status": "SUCCESS",
        "watchlistId": "1",
    }

    result: t.Final = await async_watchlists.create(
        "My Watchlist", epics=["CS.D.EURUSD.CFD.IP"]
    )

    async_requester.post.assert_awaited_once_with(
        "watchlists",
        json={"name": "My Watchlist", "epics": ["CS.D.EURUSD.CFD.IP"]},
    )
    assert result == ig.watchlists.v1.CreateResult.model_validate(
        {"status": "SUCCESS", "watchlistId": "1"}
    )


async def test_async_create_given_no_epics(
    async_watchlists: ig.AsyncWatchlistsResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.post.return_value = {
        "status": "SUCCESS",
        "watchlistId": "1",
    }

    await async_watchlists.create("My Watchlist")

    async_requester.post.assert_awaited_once_with(
        "watchlists", json={"name": "My Watchlist"}
    )


async def test_async_delete_given_no_epic(
    async_watchlists: ig.AsyncWatchlistsResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.delete.return_value = {"status": "SUCCESS"}

    result: t.Final = await async_watchlists.delete("1")

    async_requester.delete.assert_awaited_once_with("watchlists/1", json={})
    assert result == "SUCCESS"


async def test_async_delete_given_epic(
    async_watchlists: ig.AsyncWatchlistsResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.delete.return_value = {"status": "SUCCESS"}

    await async_watchlists.delete("1", "CS.D.EURUSD.CFD.IP")

    async_requester.delete.assert_awaited_once_with(
        "watchlists/1/CS.D.EURUSD.CFD.IP", json={}
    )


async def test_async_get(
    async_watchlists: ig.AsyncWatchlistsResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {"markets": [_market_overview]}

    result: t.Final = await async_watchlists.get("1")

    async_requester.get.assert_awaited_once_with("watchlists/1")
    assert result == (
        ig.markets.v1.MarketOverview.model_validate(_market_overview),
    )


async def test_async_list(
    async_watchlists: ig.AsyncWatchlistsResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {"watchlists": [_watchlist]}

    result: t.Final = await async_watchlists.list()

    async_requester.get.assert_awaited_once_with("watchlists")
    assert result == (ig.watchlists.v1.Watchlist.model_validate(_watchlist),)


async def test_async_update(
    async_watchlists: ig.AsyncWatchlistsResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.put.return_value = {"status": "SUCCESS"}

    result: t.Final = await async_watchlists.update(
        "1", epic="CS.D.EURUSD.CFD.IP"
    )

    async_requester.put.assert_awaited_once_with(
        "watchlists/1", json={"epic": "CS.D.EURUSD.CFD.IP"}
    )
    assert result == "SUCCESS"


def test_create_given_epics(
    watchlists: ig.WatchlistsResource, requester: mock.MagicMock
) -> None:
    requester.post.return_value = {
        "status": "SUCCESS",
        "watchlistId": "1",
    }

    result: t.Final = watchlists.create(
        "My Watchlist", epics=["CS.D.EURUSD.CFD.IP"]
    )

    requester.post.assert_called_once_with(
        "watchlists",
        json={"name": "My Watchlist", "epics": ["CS.D.EURUSD.CFD.IP"]},
    )
    assert result == ig.watchlists.v1.CreateResult.model_validate(
        {"status": "SUCCESS", "watchlistId": "1"}
    )


def test_create_given_no_epics(
    watchlists: ig.WatchlistsResource, requester: mock.MagicMock
) -> None:
    requester.post.return_value = {"status": "SUCCESS", "watchlistId": "1"}

    watchlists.create("My Watchlist")

    requester.post.assert_called_once_with(
        "watchlists", json={"name": "My Watchlist"}
    )


def test_delete_given_no_epic(
    watchlists: ig.WatchlistsResource, requester: mock.MagicMock
) -> None:
    requester.delete.return_value = {"status": "SUCCESS"}

    result: t.Final = watchlists.delete("1")

    requester.delete.assert_called_once_with("watchlists/1", json={})
    assert result == "SUCCESS"


def test_delete_given_epic(
    watchlists: ig.WatchlistsResource, requester: mock.MagicMock
) -> None:
    requester.delete.return_value = {"status": "SUCCESS"}

    watchlists.delete("1", "CS.D.EURUSD.CFD.IP")

    requester.delete.assert_called_once_with(
        "watchlists/1/CS.D.EURUSD.CFD.IP", json={}
    )


def test_get(
    watchlists: ig.WatchlistsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"markets": [_market_overview]}

    result: t.Final = watchlists.get("1")

    requester.get.assert_called_once_with("watchlists/1")
    assert result == (
        ig.markets.v1.MarketOverview.model_validate(_market_overview),
    )


def test_list(
    watchlists: ig.WatchlistsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"watchlists": [_watchlist]}

    result: t.Final = watchlists.list()

    requester.get.assert_called_once_with("watchlists")
    assert result == (ig.watchlists.v1.Watchlist.model_validate(_watchlist),)


def test_update(
    watchlists: ig.WatchlistsResource, requester: mock.MagicMock
) -> None:
    requester.put.return_value = {"status": "SUCCESS"}

    result: t.Final = watchlists.update("1", epic="CS.D.EURUSD.CFD.IP")

    requester.put.assert_called_once_with(
        "watchlists/1", json={"epic": "CS.D.EURUSD.CFD.IP"}
    )
    assert result == "SUCCESS"
