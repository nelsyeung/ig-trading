from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig


@pytest.fixture
def async_accounts(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncAccountsResource:
    return ig.AsyncAccountsResource(async_requester)


@pytest.fixture
def accounts(requester: ig.APIRequester) -> ig.AccountsResource:
    return ig.AccountsResource(requester)


async def test_async_list(async_accounts: ig.AsyncAccountsResource) -> None:
    assert all(
        isinstance(account, ig.accounts.v1.Account)
        for account in await async_accounts.list()
    )


async def test_async_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncAccountsResource().list()


async def test_async_preferences_get(
    async_accounts: ig.AsyncAccountsResource,
) -> None:
    assert isinstance(
        await async_accounts.preferences.get(), ig.accounts.v1.Preferences
    )


async def test_async_preferences_update(
    async_accounts: ig.AsyncAccountsResource,
) -> None:
    original: t.Final = await async_accounts.preferences.get()
    try:
        result: t.Final = await async_accounts.preferences.update(
            trailing_stops_enabled=not original.trailing_stops_enabled
        )
        assert result == "SUCCESS"
        assert (
            await async_accounts.preferences.get()
        ).trailing_stops_enabled == (not original.trailing_stops_enabled)
    finally:
        await async_accounts.preferences.update(
            trailing_stops_enabled=original.trailing_stops_enabled
        )


async def test_async_preferences_get_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncAccountsResource().preferences.get()


def test_list(accounts: ig.AccountsResource) -> None:
    assert all(
        isinstance(account, ig.accounts.v1.Account)
        for account in accounts.list()
    )


def test_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.AccountsResource().list()


def test_preferences_get(accounts: ig.AccountsResource) -> None:
    assert isinstance(
        accounts.preferences.get(), ig.accounts.v1.Preferences
    )


def test_preferences_update(accounts: ig.AccountsResource) -> None:
    original: t.Final = accounts.preferences.get()
    try:
        result: t.Final = accounts.preferences.update(
            trailing_stops_enabled=not original.trailing_stops_enabled
        )
        assert result == "SUCCESS"
        assert accounts.preferences.get().trailing_stops_enabled == (
            not original.trailing_stops_enabled
        )
    finally:
        accounts.preferences.update(
            trailing_stops_enabled=original.trailing_stops_enabled
        )


def test_preferences_get_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.AccountsResource().preferences.get()
