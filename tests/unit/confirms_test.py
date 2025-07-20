from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock


_deal_confirmation: t.Final[dict[str, object]] = {
    "affectedDeals": [],
    "date": "2024-01-02T03:04:05",
    "dealId": "DEAL1",
    "dealReference": "REF1",
    "dealStatus": "ACCEPTED",
    "direction": "BUY",
    "epic": "CS.D.EURUSD.CFD.IP",
    "expiry": None,
    "guaranteedStop": False,
    "level": 1.1,
    "limitDistance": None,
    "limitLevel": None,
    "profit": None,
    "profitCurrency": None,
    "reason": "SUCCESS",
    "size": 1.0,
    "status": "OPEN",
    "stopDistance": None,
    "stopLevel": None,
    "trailingStop": False,
}


@pytest.fixture
def async_confirms(
    async_requester: mock.AsyncMock,
) -> ig.AsyncConfirmsResource:
    return ig.AsyncConfirmsResource(async_requester)


@pytest.fixture
def confirms(requester: mock.MagicMock) -> ig.ConfirmsResource:
    return ig.ConfirmsResource(requester)


async def test_async_get(
    async_confirms: ig.AsyncConfirmsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _deal_confirmation

    result: t.Final = await async_confirms.get("REF1")

    async_requester.get.assert_awaited_once_with("confirms/REF1")
    assert isinstance(result, ig.confirms.v1.DealConfirmation)
    assert result.deal_id == "DEAL1"
    assert result.reason == "SUCCESS"


def test_get(
    confirms: ig.ConfirmsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _deal_confirmation

    result: t.Final = confirms.get("REF1")

    requester.get.assert_called_once_with("confirms/REF1")
    assert isinstance(result, ig.confirms.v1.DealConfirmation)
    assert result.deal_id == "DEAL1"
    assert result.reason == "SUCCESS"
