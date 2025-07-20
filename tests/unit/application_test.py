from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock

_application: t.Final = {
    "apiKey": "a-key",
    "allowEquities": True,
    "allowQuoteOrders": True,
    "allowanceAccountOverall": 60.0,
    "allowanceAccountTrading": 100.0,
    "allowanceAccountHistoricalData": 10000.0,
    "allowanceApplicationOverall": 6000.0,
    "concurrentSubscriptionsLimit": 40.0,
    "createdDate": "2024-01-01",
    "name": "My App",
    "status": "ENABLED",
}


@pytest.fixture
def async_application(
    async_requester: mock.AsyncMock,
) -> ig.AsyncApplicationResource:
    return ig.AsyncApplicationResource(async_requester)


@pytest.fixture
def application(requester: mock.MagicMock) -> ig.ApplicationResource:
    return ig.ApplicationResource(requester)


async def test_async_disable_update(
    async_application: ig.AsyncApplicationResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.put.return_value = [_application]

    result: t.Final = await async_application.disable.update()

    async_requester.put.assert_awaited_once_with(
        "operations/application/disable", json={}
    )
    assert result == (
        ig.application.v1.Application.model_validate(_application),
    )


async def test_async_list(
    async_application: ig.AsyncApplicationResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = [_application]

    result: t.Final = await async_application.list()

    async_requester.get.assert_awaited_once_with("operations/application")
    assert result == (
        ig.application.v1.Application.model_validate(_application),
    )


async def test_async_update(
    async_application: ig.AsyncApplicationResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.put.return_value = [_application]

    result: t.Final = await async_application.update(
        allowance_account_overall=60.0,
        allowance_account_trading=100.0,
        api_key="a-key",
        status="ENABLED",
    )

    async_requester.put.assert_awaited_once_with(
        "operations/application",
        json={
            "allowanceAccountOverall": 60.0,
            "allowanceAccountTrading": 100.0,
            "apiKey": "a-key",
            "status": "ENABLED",
        },
    )
    assert result == (
        ig.application.v1.Application.model_validate(_application),
    )


async def test_async_update_given_no_status(
    async_application: ig.AsyncApplicationResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.put.return_value = [_application]

    await async_application.update(
        allowance_account_overall=60.0,
        allowance_account_trading=100.0,
        api_key="a-key",
    )

    async_requester.put.assert_awaited_once_with(
        "operations/application",
        json={
            "allowanceAccountOverall": 60.0,
            "allowanceAccountTrading": 100.0,
            "apiKey": "a-key",
        },
    )


def test_disable_update(
    application: ig.ApplicationResource, requester: mock.MagicMock
) -> None:
    requester.put.return_value = [_application]

    result: t.Final = application.disable.update()

    requester.put.assert_called_once_with(
        "operations/application/disable", json={}
    )
    assert result == (
        ig.application.v1.Application.model_validate(_application),
    )


def test_list(
    application: ig.ApplicationResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = [_application]

    result: t.Final = application.list()

    requester.get.assert_called_once_with("operations/application")
    assert result == (
        ig.application.v1.Application.model_validate(_application),
    )


def test_update(
    application: ig.ApplicationResource, requester: mock.MagicMock
) -> None:
    requester.put.return_value = [_application]

    result: t.Final = application.update(
        allowance_account_overall=60.0,
        allowance_account_trading=100.0,
        api_key="a-key",
        status="ENABLED",
    )

    requester.put.assert_called_once_with(
        "operations/application",
        json={
            "allowanceAccountOverall": 60.0,
            "allowanceAccountTrading": 100.0,
            "apiKey": "a-key",
            "status": "ENABLED",
        },
    )
    assert result == (
        ig.application.v1.Application.model_validate(_application),
    )


def test_update_given_no_status(
    application: ig.ApplicationResource, requester: mock.MagicMock
) -> None:
    requester.put.return_value = [_application]

    application.update(
        allowance_account_overall=60.0,
        allowance_account_trading=100.0,
        api_key="a-key",
    )

    requester.put.assert_called_once_with(
        "operations/application",
        json={
            "allowanceAccountOverall": 60.0,
            "allowanceAccountTrading": 100.0,
            "apiKey": "a-key",
        },
    )
