from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock

_oauth_token: t.Final = {
    "access_token": "an-access-token",
    "expires_in": 60,
    "refresh_token": "a-refresh-token",
    "scope": "profile",
    "token_type": "Bearer",
}
_account_summary_v3: t.Final = {
    "accountId": "ACC1",
    "clientId": "CLIENT1",
    "lightstreamerEndpoint": "https://example.com",
    "oauthToken": _oauth_token,
    "timezoneOffset": 0,
}


@pytest.fixture
def async_session(async_requester: mock.AsyncMock) -> ig.AsyncSessionResource:
    return ig.AsyncSessionResource(async_requester)


@pytest.fixture
def session(requester: mock.MagicMock) -> ig.SessionResource:
    return ig.SessionResource(requester)


async def test_async_create_given_v1(
    async_session: ig.AsyncSessionResource, async_requester: mock.AsyncMock
) -> None:
    balance: t.Final = {
        "available": 100.0,
        "balance": 100.0,
        "deposit": 0.0,
        "profitLoss": 0.0,
    }
    async_requester.post.return_value = {
        "accountInfo": balance,
        "accountType": "CFD",
        "accounts": [
            {
                "accountId": "ACC1",
                "accountName": "My Account",
                "accountType": "CFD",
                "preferred": True,
            }
        ],
        "clientId": "CLIENT1",
        "currencyIsoCode": "GBP",
        "currencySymbol": "£",
        "currentAccountId": "ACC1",
        "dealingEnabled": True,
        "hasActiveDemoAccounts": True,
        "hasActiveLiveAccounts": False,
        "lightstreamerEndpoint": "https://example.com",
        "reroutingEnvironment": None,
        "timezoneOffset": 0,
        "trailingStopsEnabled": True,
    }

    result: t.Final = await async_session.create(
        encrypted_password=True,
        identifier="a-user",
        password="a-password",
        version=1,
    )

    async_requester.post.assert_awaited_once_with(
        "session",
        json={
            "identifier": "a-user",
            "password": "a-password",
            "encryptedPassword": "true",
        },
        version=1,
    )
    assert isinstance(result, ig.session.v1.AccountSummary)


async def test_async_create_given_v3(
    async_session: ig.AsyncSessionResource,
    async_requester: mock.AsyncMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IG_IDENTIFIER", "env-user")
    monkeypatch.setenv("IG_PASSWORD", "env-password")
    async_requester.post.return_value = _account_summary_v3

    result: t.Final = await async_session.create()

    async_requester.post.assert_awaited_once_with(
        "session",
        json={"identifier": "env-user", "password": "env-password"},
        version=3,
    )
    assert result == ig.session.v3.AccountSummary.model_validate(
        _account_summary_v3
    )


async def test_async_delete(
    async_session: ig.AsyncSessionResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.delete.return_value = None

    await async_session.delete()

    async_requester.delete.assert_awaited_once_with("session")


async def test_async_get(
    async_session: ig.AsyncSessionResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {
        "accountId": "ACC1",
        "clientId": "CLIENT1",
        "currency": "GBP",
        "lightstreamerEndpoint": "https://example.com",
        "locale": "en_GB",
        "timezoneOffset": 0,
    }

    result: t.Final = await async_session.get()

    async_requester.get.assert_awaited_once_with("session")
    assert isinstance(result, ig.session.v1.Session)


async def test_async_update(
    async_session: ig.AsyncSessionResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.put.return_value = {
        "dealingEnabled": True,
        "hasActiveDemoAccounts": True,
        "hasActiveLiveAccounts": False,
        "trailingStopsEnabled": True,
    }

    result: t.Final = await async_session.update("ACC2", default_account=True)

    async_requester.put.assert_awaited_once_with(
        "session",
        json={"accountId": "ACC2", "defaultAccount": True},
    )
    assert isinstance(result, ig.session.v1.SwitchAccount)


async def test_async_encryption_key_get(
    async_session: ig.AsyncSessionResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {
        "encryptionKey": "a-key",
        "timeStamp": 1704067200000,
    }

    result: t.Final = await async_session.encryption_key.get()

    async_requester.get.assert_awaited_once_with("session/encryptionKey")
    assert isinstance(result, ig.session.v1.EncryptionKey)


async def test_async_refresh_token_create(
    async_session: ig.AsyncSessionResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.post.return_value = _oauth_token

    result: t.Final = await async_session.refresh_token.create(
        "a-refresh-token"
    )

    async_requester.post.assert_awaited_once_with(
        "session/refresh-token", json={"refresh_token": "a-refresh-token"}
    )
    assert result == ig.session.v1.OAuthToken.model_validate(_oauth_token)


def test_create_given_v1(
    session: ig.SessionResource, requester: mock.MagicMock
) -> None:
    balance: t.Final = {
        "available": 100.0,
        "balance": 100.0,
        "deposit": 0.0,
        "profitLoss": 0.0,
    }
    requester.post.return_value = {
        "accountInfo": balance,
        "accountType": "CFD",
        "accounts": [
            {
                "accountId": "ACC1",
                "accountName": "My Account",
                "accountType": "CFD",
                "preferred": True,
            }
        ],
        "clientId": "CLIENT1",
        "currencyIsoCode": "GBP",
        "currencySymbol": "£",
        "currentAccountId": "ACC1",
        "dealingEnabled": True,
        "hasActiveDemoAccounts": True,
        "hasActiveLiveAccounts": False,
        "lightstreamerEndpoint": "https://example.com",
        "reroutingEnvironment": None,
        "timezoneOffset": 0,
        "trailingStopsEnabled": True,
    }

    result: t.Final = session.create(
        encrypted_password=True,
        identifier="a-user",
        password="a-password",
        version=1,
    )

    requester.post.assert_called_once_with(
        "session",
        json={
            "identifier": "a-user",
            "password": "a-password",
            "encryptedPassword": "true",
        },
        version=1,
    )
    assert isinstance(result, ig.session.v1.AccountSummary)


def test_create_given_v3(
    session: ig.SessionResource,
    requester: mock.MagicMock,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IG_IDENTIFIER", "env-user")
    monkeypatch.setenv("IG_PASSWORD", "env-password")
    requester.post.return_value = _account_summary_v3

    result: t.Final = session.create()

    requester.post.assert_called_once_with(
        "session",
        json={"identifier": "env-user", "password": "env-password"},
        version=3,
    )
    assert result == ig.session.v3.AccountSummary.model_validate(
        _account_summary_v3
    )


def test_delete(
    session: ig.SessionResource, requester: mock.MagicMock
) -> None:
    requester.delete.return_value = None

    session.delete()

    requester.delete.assert_called_once_with("session")


def test_get(
    session: ig.SessionResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {
        "accountId": "ACC1",
        "clientId": "CLIENT1",
        "currency": "GBP",
        "lightstreamerEndpoint": "https://example.com",
        "locale": "en_GB",
        "timezoneOffset": 0,
    }

    result: t.Final = session.get()

    requester.get.assert_called_once_with("session")
    assert isinstance(result, ig.session.v1.Session)


def test_update(
    session: ig.SessionResource, requester: mock.MagicMock
) -> None:
    requester.put.return_value = {
        "dealingEnabled": True,
        "hasActiveDemoAccounts": True,
        "hasActiveLiveAccounts": False,
        "trailingStopsEnabled": True,
    }

    result: t.Final = session.update("ACC2", default_account=True)

    requester.put.assert_called_once_with(
        "session",
        json={"accountId": "ACC2", "defaultAccount": True},
    )
    assert isinstance(result, ig.session.v1.SwitchAccount)


def test_encryption_key_get(
    session: ig.SessionResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {
        "encryptionKey": "a-key",
        "timeStamp": 1704067200000,
    }

    result: t.Final = session.encryption_key.get()

    requester.get.assert_called_once_with("session/encryptionKey")
    assert isinstance(result, ig.session.v1.EncryptionKey)


def test_refresh_token_create(
    session: ig.SessionResource, requester: mock.MagicMock
) -> None:
    requester.post.return_value = _oauth_token

    result: t.Final = session.refresh_token.create("a-refresh-token")

    requester.post.assert_called_once_with(
        "session/refresh-token", json={"refresh_token": "a-refresh-token"}
    )
    assert result == ig.session.v1.OAuthToken.model_validate(_oauth_token)
