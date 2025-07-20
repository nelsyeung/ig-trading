from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock

_market: t.Final = {
    "bid": 1.1,
    "delayTime": 0,
    "epic": "CS.D.EURUSD.CFD.IP",
    "exchangeId": "EXCH",
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
_working_order_data_v1: t.Final = {
    "contingentLimit": None,
    "contingentStop": None,
    "controlledRisk": False,
    "createdDate": "2024/01/02 03:04:05:000",
    "currencyCode": "USD",
    "dealId": "DEAL1",
    "direction": "BUY",
    "dma": False,
    "epic": "CS.D.EURUSD.CFD.IP",
    "goodTill": None,
    "limitedRiskPremium": None,
    "level": 1.1,
    "requestType": "LIMIT_ORDER",
    "size": 1.0,
    "trailingStopDistance": None,
    "trailingStopIncrement": None,
    "trailingTriggerDistance": None,
    "trailingTriggerIncrement": None,
}
_working_order_data_v2: t.Final = {
    "createdDate": "2024/01/02 03:04:05:000",
    "createdDateUTC": "2024-01-02T03:04:05",
    "currencyCode": "USD",
    "dealId": "DEAL1",
    "direction": "BUY",
    "dma": False,
    "epic": "CS.D.EURUSD.CFD.IP",
    "goodTillDate": None,
    "goodTillDateISO": None,
    "guaranteedStop": False,
    "limitDistance": None,
    "limitedRiskPremium": None,
    "orderLevel": 1.1,
    "orderSize": 1.0,
    "orderType": "LIMIT",
    "stopDistance": None,
    "timeInForce": "GOOD_TILL_CANCELLED",
}


@pytest.fixture
def async_working_orders(
    async_requester: mock.AsyncMock,
) -> ig.AsyncWorkingOrdersResource:
    return ig.AsyncWorkingOrdersResource(async_requester)


@pytest.fixture
def working_orders(requester: mock.MagicMock) -> ig.WorkingOrdersResource:
    return ig.WorkingOrdersResource(requester)


async def test_async_list_given_v1(
    async_working_orders: ig.AsyncWorkingOrdersResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {
        "workingOrders": [
            {
                "marketData": _market,
                "workingOrderData": _working_order_data_v1,
            }
        ]
    }

    result: t.Final = await async_working_orders.list(version=1)

    async_requester.get.assert_awaited_once_with("workingorders", version=1)
    assert len(result) == 1
    assert isinstance(result[0], ig.working_orders.v1.WorkingOrder)


async def test_async_list_given_v2_default(
    async_working_orders: ig.AsyncWorkingOrdersResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {
        "workingOrders": [
            {
                "marketData": _market,
                "workingOrderData": _working_order_data_v2,
            }
        ]
    }

    result: t.Final = await async_working_orders.list()

    async_requester.get.assert_awaited_once_with("workingorders", version=2)
    assert len(result) == 1
    assert isinstance(result[0], ig.working_orders.v2.WorkingOrder)


async def test_async_otc_create(
    async_working_orders: ig.AsyncWorkingOrdersResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.post.return_value = {"dealReference": "REF1"}

    result: t.Final = await async_working_orders.otc.create(
        currency_code="USD",
        direction="BUY",
        epic="CS.D.EURUSD.CFD.IP",
        expiry="-",
        guaranteed_stop=False,
        level=1.1,
        order_type="LIMIT",
        size=1.0,
        time_in_force="GOOD_TILL_CANCELLED",
    )

    async_requester.post.assert_awaited_once_with(
        "workingorders/otc",
        json={
            "currencyCode": "USD",
            "direction": "BUY",
            "epic": "CS.D.EURUSD.CFD.IP",
            "expiry": "-",
            "guaranteedStop": False,
            "level": 1.1,
            "size": 1.0,
            "timeInForce": "GOOD_TILL_CANCELLED",
            "type": "LIMIT",
        },
        version=2,
    )
    assert result == "REF1"


async def test_async_otc_delete(
    async_working_orders: ig.AsyncWorkingOrdersResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.delete.return_value = {"dealReference": "REF1"}

    result: t.Final = await async_working_orders.otc.delete("DEAL1")

    async_requester.delete.assert_awaited_once_with(
        "workingorders/otc/DEAL1", json={}
    )
    assert result == "REF1"


async def test_async_otc_update(
    async_working_orders: ig.AsyncWorkingOrdersResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.put.return_value = {"dealReference": "REF1"}

    result: t.Final = await async_working_orders.otc.update(
        "DEAL1",
        order_type="LIMIT",
        time_in_force="GOOD_TILL_CANCELLED",
        level=1.2,
    )

    async_requester.put.assert_awaited_once_with(
        "workingorders/otc/DEAL1",
        json={
            "level": 1.2,
            "timeInForce": "GOOD_TILL_CANCELLED",
            "type": "LIMIT",
        },
    )
    assert result == "REF1"


def test_list_given_v1(
    working_orders: ig.WorkingOrdersResource,
    requester: mock.MagicMock,
) -> None:
    requester.get.return_value = {
        "workingOrders": [
            {
                "marketData": _market,
                "workingOrderData": _working_order_data_v1,
            }
        ]
    }

    result: t.Final = working_orders.list(version=1)

    requester.get.assert_called_once_with("workingorders", version=1)
    assert len(result) == 1
    assert isinstance(result[0], ig.working_orders.v1.WorkingOrder)


def test_list_given_v2_default(
    working_orders: ig.WorkingOrdersResource,
    requester: mock.MagicMock,
) -> None:
    requester.get.return_value = {
        "workingOrders": [
            {
                "marketData": _market,
                "workingOrderData": _working_order_data_v2,
            }
        ]
    }

    result: t.Final = working_orders.list()

    requester.get.assert_called_once_with("workingorders", version=2)
    assert len(result) == 1
    assert isinstance(result[0], ig.working_orders.v2.WorkingOrder)


def test_otc_create(
    working_orders: ig.WorkingOrdersResource,
    requester: mock.MagicMock,
) -> None:
    requester.post.return_value = {"dealReference": "REF1"}

    result: t.Final = working_orders.otc.create(
        currency_code="USD",
        direction="BUY",
        epic="CS.D.EURUSD.CFD.IP",
        expiry="-",
        guaranteed_stop=False,
        level=1.1,
        order_type="LIMIT",
        size=1.0,
        time_in_force="GOOD_TILL_CANCELLED",
    )

    requester.post.assert_called_once_with(
        "workingorders/otc",
        json={
            "currencyCode": "USD",
            "direction": "BUY",
            "epic": "CS.D.EURUSD.CFD.IP",
            "expiry": "-",
            "guaranteedStop": False,
            "level": 1.1,
            "size": 1.0,
            "timeInForce": "GOOD_TILL_CANCELLED",
            "type": "LIMIT",
        },
        version=2,
    )
    assert result == "REF1"


def test_otc_delete(
    working_orders: ig.WorkingOrdersResource,
    requester: mock.MagicMock,
) -> None:
    requester.delete.return_value = {"dealReference": "REF1"}

    result: t.Final = working_orders.otc.delete("DEAL1")

    requester.delete.assert_called_once_with(
        "workingorders/otc/DEAL1", json={}
    )
    assert result == "REF1"


def test_otc_update(
    working_orders: ig.WorkingOrdersResource,
    requester: mock.MagicMock,
) -> None:
    requester.put.return_value = {"dealReference": "REF1"}

    result: t.Final = working_orders.otc.update(
        "DEAL1",
        order_type="LIMIT",
        time_in_force="GOOD_TILL_CANCELLED",
        level=1.2,
    )

    requester.put.assert_called_once_with(
        "workingorders/otc/DEAL1",
        json={
            "level": 1.2,
            "timeInForce": "GOOD_TILL_CANCELLED",
            "type": "LIMIT",
        },
    )
    assert result == "REF1"
