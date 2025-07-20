from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock

_market_v1: t.Final = {
    "bid": 1.1,
    "delayTime": 0,
    "epic": "CS.D.EURUSD.CFD.IP",
    "expiry": "-",
    "high": 1.2,
    "instrumentName": "EUR/USD",
    "instrumentType": "CURRENCIES",
    "lotSize": 1.0,
    "low": 1.0,
    "marketStatus": "TRADEABLE",
    "netChange": 0.0,
    "offer": 1.1,
    "percentageChange": 0.0,
    "scalingFactor": 1,
    "streamingPricesAvailable": True,
    "updateTime": "12:00:00",
}
_market_v2: t.Final = {**_market_v1, "updateTimeUTC": "12:00:00"}
_position_data_v1: t.Final = {
    "contractSize": 1.0,
    "controlledRisk": False,
    "createdDate": "2024-01-02T03:04:05",
    "currency": "USD",
    "dealId": "DEAL1",
    "dealSize": 1.0,
    "direction": "BUY",
    "limitLevel": None,
    "limitedRiskPremium": None,
    "openLevel": 1.1,
    "stopLevel": None,
    "trailingStep": None,
    "trailingStopDistance": None,
}
_position_data_v2: t.Final = {
    "contractSize": 1.0,
    "controlledRisk": False,
    "createdDate": "2024-01-02T03:04:05",
    "createdDateUTC": "2024-01-02T03:04:05",
    "currency": "USD",
    "dealId": "DEAL1",
    "dealReference": "REF1",
    "direction": "BUY",
    "level": 1.1,
    "limitLevel": None,
    "limitedRiskPremium": None,
    "size": 1.0,
    "stopLevel": None,
    "trailingStep": None,
    "trailingStopDistance": None,
}


@pytest.fixture
def async_positions(
    async_requester: mock.AsyncMock,
) -> ig.AsyncPositionsResource:
    return ig.AsyncPositionsResource(async_requester)


@pytest.fixture
def positions(requester: mock.MagicMock) -> ig.PositionsResource:
    return ig.PositionsResource(requester)


async def test_async_get_given_v1(
    async_positions: ig.AsyncPositionsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {
        "market": _market_v1,
        "position": _position_data_v1,
    }

    result: t.Final = await async_positions.get("DEAL1", version=1)

    async_requester.get.assert_awaited_once_with("positions/DEAL1", version=1)
    assert isinstance(result, ig.positions.v1.Position)


async def test_async_get_given_v2_default(
    async_positions: ig.AsyncPositionsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {
        "market": _market_v2,
        "position": _position_data_v2,
    }

    result: t.Final = await async_positions.get("DEAL1")

    async_requester.get.assert_awaited_once_with("positions/DEAL1", version=2)
    assert isinstance(result, ig.positions.v2.Position)


async def test_async_list_given_v1(
    async_positions: ig.AsyncPositionsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {
        "positions": [{"market": _market_v1, "position": _position_data_v1}]
    }

    result: t.Final = await async_positions.list(version=1)

    async_requester.get.assert_awaited_once_with("positions", version=1)
    assert len(result) == 1
    assert isinstance(result[0], ig.positions.v1.Position)


async def test_async_list_given_v2_default(
    async_positions: ig.AsyncPositionsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {
        "positions": [{"market": _market_v2, "position": _position_data_v2}]
    }

    result: t.Final = await async_positions.list()

    async_requester.get.assert_awaited_once_with("positions", version=2)
    assert len(result) == 1
    assert isinstance(result[0], ig.positions.v2.Position)


async def test_async_otc_create(
    async_positions: ig.AsyncPositionsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.post.return_value = {"dealReference": "REF1"}

    result: t.Final = await async_positions.otc.create(
        currency_code="USD",
        direction="BUY",
        epic="CS.D.EURUSD.CFD.IP",
        expiry="-",
        force_open=True,
        guaranteed_stop=False,
        order_type="MARKET",
        size=1.0,
    )

    async_requester.post.assert_awaited_once_with(
        "positions/otc",
        json={
            "currencyCode": "USD",
            "dealReference": None,
            "direction": "BUY",
            "epic": "CS.D.EURUSD.CFD.IP",
            "expiry": "-",
            "forceOpen": True,
            "guaranteedStop": False,
            "level": None,
            "limitDistance": None,
            "limitLevel": None,
            "orderType": "MARKET",
            "quoteId": None,
            "size": 1.0,
            "stopDistance": None,
            "stopLevel": None,
            "trailingStop": None,
            "trailingStopIncrement": None,
        },
        version=2,
    )
    assert result == "REF1"


async def test_async_otc_delete(
    async_positions: ig.AsyncPositionsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.delete.return_value = {"dealReference": "REF1"}

    result: t.Final = await async_positions.otc.delete(
        deal_id="DEAL1", direction="BUY", order_type="MARKET", size=1.0
    )

    async_requester.delete.assert_awaited_once_with(
        "positions/otc",
        json={
            "dealId": "DEAL1",
            "direction": "BUY",
            "epic": None,
            "expiry": None,
            "level": None,
            "orderType": "MARKET",
            "quoteId": None,
            "size": 1.0,
            "timeInForce": None,
        },
    )
    assert result == "REF1"


async def test_async_otc_update(
    async_positions: ig.AsyncPositionsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.put.return_value = {"dealReference": "REF1"}

    result: t.Final = await async_positions.otc.update(
        "DEAL1", limit_level=1.2, stop_level=1.0
    )

    async_requester.put.assert_awaited_once_with(
        "positions/otc/DEAL1",
        json={
            "guaranteedStop": None,
            "limitLevel": 1.2,
            "stopLevel": 1.0,
            "trailingStop": None,
            "trailingStopDistance": None,
            "trailingStopIncrement": None,
        },
    )
    assert result == "REF1"


def test_get_given_v1(
    positions: ig.PositionsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {
        "market": _market_v1,
        "position": _position_data_v1,
    }

    result: t.Final = positions.get("DEAL1", version=1)

    requester.get.assert_called_once_with("positions/DEAL1", version=1)
    assert isinstance(result, ig.positions.v1.Position)


def test_get_given_v2_default(
    positions: ig.PositionsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {
        "market": _market_v2,
        "position": _position_data_v2,
    }

    result: t.Final = positions.get("DEAL1")

    requester.get.assert_called_once_with("positions/DEAL1", version=2)
    assert isinstance(result, ig.positions.v2.Position)


def test_list_given_v1(
    positions: ig.PositionsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {
        "positions": [{"market": _market_v1, "position": _position_data_v1}]
    }

    result: t.Final = positions.list(version=1)

    requester.get.assert_called_once_with("positions", version=1)
    assert len(result) == 1
    assert isinstance(result[0], ig.positions.v1.Position)


def test_list_given_v2_default(
    positions: ig.PositionsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {
        "positions": [{"market": _market_v2, "position": _position_data_v2}]
    }

    result: t.Final = positions.list()

    requester.get.assert_called_once_with("positions", version=2)
    assert len(result) == 1
    assert isinstance(result[0], ig.positions.v2.Position)


def test_otc_create(
    positions: ig.PositionsResource, requester: mock.MagicMock
) -> None:
    requester.post.return_value = {"dealReference": "REF1"}

    result: t.Final = positions.otc.create(
        currency_code="USD",
        direction="BUY",
        epic="CS.D.EURUSD.CFD.IP",
        expiry="-",
        force_open=True,
        guaranteed_stop=False,
        order_type="MARKET",
        size=1.0,
    )

    requester.post.assert_called_once_with(
        "positions/otc",
        json={
            "currencyCode": "USD",
            "dealReference": None,
            "direction": "BUY",
            "epic": "CS.D.EURUSD.CFD.IP",
            "expiry": "-",
            "forceOpen": True,
            "guaranteedStop": False,
            "level": None,
            "limitDistance": None,
            "limitLevel": None,
            "orderType": "MARKET",
            "quoteId": None,
            "size": 1.0,
            "stopDistance": None,
            "stopLevel": None,
            "trailingStop": None,
            "trailingStopIncrement": None,
        },
        version=2,
    )
    assert result == "REF1"


def test_otc_delete(
    positions: ig.PositionsResource, requester: mock.MagicMock
) -> None:
    requester.delete.return_value = {"dealReference": "REF1"}

    result: t.Final = positions.otc.delete(
        deal_id="DEAL1", direction="BUY", order_type="MARKET", size=1.0
    )

    requester.delete.assert_called_once_with(
        "positions/otc",
        json={
            "dealId": "DEAL1",
            "direction": "BUY",
            "epic": None,
            "expiry": None,
            "level": None,
            "orderType": "MARKET",
            "quoteId": None,
            "size": 1.0,
            "timeInForce": None,
        },
    )
    assert result == "REF1"


def test_otc_update(
    positions: ig.PositionsResource, requester: mock.MagicMock
) -> None:
    requester.put.return_value = {"dealReference": "REF1"}

    result: t.Final = positions.otc.update(
        "DEAL1", limit_level=1.2, stop_level=1.0
    )

    requester.put.assert_called_once_with(
        "positions/otc/DEAL1",
        json={
            "guaranteedStop": None,
            "limitLevel": 1.2,
            "stopLevel": 1.0,
            "trailingStop": None,
            "trailingStopDistance": None,
            "trailingStopIncrement": None,
        },
    )
    assert result == "REF1"
