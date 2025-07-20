from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock


@pytest.fixture
def accounts(requester: mock.MagicMock) -> ig.AccountsResource:
    return ig.AccountsResource(requester)


@pytest.fixture
def async_accounts(
    async_requester: mock.AsyncMock,
) -> ig.AsyncAccountsResource:
    return ig.AsyncAccountsResource(async_requester)


_account: t.Final = {
    "accountAlias": None,
    "accountId": "ACC1",
    "accountName": "My Account",
    "accountType": "CFD",
    "balance": {
        "available": 100.0,
        "balance": 100.0,
        "deposit": 0.0,
        "profitLoss": 0.0,
    },
    "canTransferFrom": True,
    "canTransferTo": True,
    "currency": "GBP",
    "preferred": True,
    "status": "ENABLED",
}


async def test_async_list(
    async_accounts: ig.AsyncAccountsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"accounts": [_account]}

    result: t.Final = await async_accounts.list()

    async_requester.get.assert_awaited_once_with("accounts")
    assert result == (ig.accounts.v1.Account.model_validate(_account),)


async def test_async_preferences_get(
    async_accounts: ig.AsyncAccountsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"trailingStopsEnabled": True}

    result: t.Final = await async_accounts.preferences.get()

    async_requester.get.assert_awaited_once_with("accounts/preferences")
    assert result == ig.accounts.v1.Preferences.model_validate(
        {"trailingStopsEnabled": True}
    )


async def test_async_preferences_update(
    async_accounts: ig.AsyncAccountsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.put.return_value = {"status": "SUCCESS"}

    result: t.Final = await async_accounts.preferences.update(
        trailing_stops_enabled=True
    )

    async_requester.put.assert_awaited_once_with(
        "accounts/preferences",
        json={"trailingStopsEnabled": True},
    )
    assert result == "SUCCESS"


def test_list(
    accounts: ig.AccountsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"accounts": [_account]}

    result: t.Final = accounts.list()

    requester.get.assert_called_once_with("accounts")
    assert result == (ig.accounts.v1.Account.model_validate(_account),)


def test_preferences_get(
    accounts: ig.AccountsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"trailingStopsEnabled": True}

    result: t.Final = accounts.preferences.get()

    requester.get.assert_called_once_with("accounts/preferences")
    assert result == ig.accounts.v1.Preferences.model_validate(
        {"trailingStopsEnabled": True}
    )


def test_preferences_update(
    accounts: ig.AccountsResource, requester: mock.MagicMock
) -> None:
    requester.put.return_value = {"status": "SUCCESS"}

    result: t.Final = accounts.preferences.update(trailing_stops_enabled=True)

    requester.put.assert_called_once_with(
        "accounts/preferences",
        json={"trailingStopsEnabled": True},
    )
    assert result == "SUCCESS"
