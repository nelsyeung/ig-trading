from __future__ import annotations

import asyncio as aio
import datetime as dt
import threading
from unittest import mock

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from collections.abc import Iterator


@pytest.fixture(autouse=True)
def _env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IG_API_KEY", "a-key")
    monkeypatch.setenv("IG_IDENTIFIER", "a-user")
    monkeypatch.setenv("IG_PASSWORD", "a-password")


@pytest.fixture
def async_session_resource() -> mock.AsyncMock:
    return mock.AsyncMock()


@pytest.fixture
def async_client(
    async_session_resource: mock.AsyncMock,
) -> Iterator[ig.AsyncClient]:
    with mock.patch(
        "_ig_trading.client.AsyncSessionResource",
        return_value=async_session_resource,
    ):
        yield ig.AsyncClient(http_session=mock.AsyncMock())


def test_async_init_given_defaults(async_client: ig.AsyncClient) -> None:
    assert async_client.api_key == "a-key"
    assert async_client.username == "a-user"
    assert async_client.password == "a-password"
    assert (
        async_client.refresh_threshold
        == ig.AsyncClient.default_refresh_threshold
    )


def test_async_init_given_explicit_arguments(
    async_session_resource: mock.AsyncMock,
) -> None:
    with mock.patch(
        "_ig_trading.client.AsyncSessionResource",
        return_value=async_session_resource,
    ):
        client: t.Final = ig.AsyncClient(
            api_key="explicit-key",
            http_session=mock.AsyncMock(),
            password="explicit-password",
            refresh_threshold=10,
            username="explicit-user",
        )

    assert client.api_key == "explicit-key"
    assert client.username == "explicit-user"
    assert client.password == "explicit-password"
    assert client.refresh_threshold == dt.timedelta(seconds=10)


async def test_async_login_sets_account_and_token(
    async_client: ig.AsyncClient, async_session_resource: mock.AsyncMock
) -> None:
    async_session_resource.create.return_value = _account_summary(
        account_id="AN-ACCOUNT"
    )

    try:
        await async_client.login()

        assert async_client.requester.account_id == "AN-ACCOUNT"
        assert async_client.requester.bearer_token == "an-access-token"
        assert async_client.oauth_token is not None
        assert async_client.oauth_token.access_token == "an-access-token"
        assert async_client.prev_refresh_time <= dt.datetime.now(
            dt.timezone.utc
        )
        async_session_resource.create.assert_awaited_once_with(
            identifier="a-user", password="a-password"
        )
    finally:
        await async_client.close()


async def test_async_login_twice_cancels_previous_refresh_task(
    async_client: ig.AsyncClient, async_session_resource: mock.AsyncMock
) -> None:
    async_session_resource.create.return_value = _account_summary()

    try:
        await async_client.login()
        first_task: t.Final = async_client._refresh_token_task
        assert first_task is not None

        await async_client.login()
        await aio.sleep(0)

        assert first_task.cancelled()
        assert async_client._refresh_token_task is not None
        assert async_client._refresh_token_task is not first_task
    finally:
        await async_client.close()


async def test_async_logout_clears_account_and_token(
    async_client: ig.AsyncClient, async_session_resource: mock.AsyncMock
) -> None:
    async_session_resource.create.return_value = _account_summary()
    await async_client.login()

    await async_client.logout()

    assert async_client.requester.account_id is None
    assert async_client.requester.bearer_token is None
    async_session_resource.delete.assert_awaited_once()


async def test_async_logout_suppresses_oauth_token_invalid_error(
    async_client: ig.AsyncClient, async_session_resource: mock.AsyncMock
) -> None:
    async_session_resource.create.return_value = _account_summary()
    await async_client.login()
    async_session_resource.delete.side_effect = ig.OAuthTokenInvalidError(
        status=401
    )

    await async_client.logout()  # Doesn't raise.


async def test_async_close_closes_owned_session(
    async_session_resource: mock.AsyncMock,
) -> None:
    with (
        mock.patch(
            "_ig_trading.client.AsyncSessionResource",
            return_value=async_session_resource,
        ),
        mock.patch("_ig_trading.client.AsyncSession") as async_session,
    ):
        async_session.return_value = mock.AsyncMock()
        client: t.Final = ig.AsyncClient()

        await client.close()

        async_session.return_value.close.assert_awaited_once()


async def test_async_close_does_not_close_given_session(
    async_client: ig.AsyncClient,
) -> None:
    await async_client.close()
    async_client._http_session.close.assert_not_called()  # type: ignore[attr-defined]


async def test_async_refresh_token(
    async_client: ig.AsyncClient, async_session_resource: mock.AsyncMock
) -> None:
    async_session_resource.create.return_value = _account_summary()
    await async_client.login()

    async_session_resource.refresh_token.create.return_value = _oauth_token(
        access_token="a-new-access-token", refresh_token="a-new-refresh-token"
    )

    try:
        await async_client.refresh_token()

        assert async_client.requester.bearer_token == "a-new-access-token"
        async_session_resource.refresh_token.create.assert_awaited_once_with(
            "a-refresh-token"
        )
    finally:
        await async_client.close()


async def test_async_refresh_token_given_no_token_does_nothing(
    async_client: ig.AsyncClient, async_session_resource: mock.AsyncMock
) -> None:
    await async_client.refresh_token()
    async_session_resource.refresh_token.create.assert_not_called()


async def test_async_auto_refresh_token_calls_refresh_token(
    async_client: ig.AsyncClient,
) -> None:
    async_client._oauth_token = _oauth_token()

    async def _stop_the_loop() -> None:
        # `_auto_refresh_token`'s `while self._oauth_token:` loop otherwise
        # never ends. Clear the slot directly (bypassing the `_oauth_token`
        # setter, which assumes a real token and would crash on `None`).
        async_client._AsyncClient__oauth_token = None  # type: ignore[attr-defined]

    with (
        # Patch on the class, not the instance: `AsyncClient` uses
        # `__slots__` (with no `__dict__`), so instance-level patching
        # would fail.
        mock.patch.object(
            ig.AsyncClient,
            "refresh_token",
            mock.AsyncMock(side_effect=_stop_the_loop),
        ) as refresh_token,
        mock.patch("_ig_trading.client.aio.sleep", mock.AsyncMock()),
    ):
        await async_client._auto_refresh_token()

    refresh_token.assert_awaited_once()


async def test_async_client_as_context_manager(
    async_client: ig.AsyncClient, async_session_resource: mock.AsyncMock
) -> None:
    async_session_resource.create.return_value = _account_summary()

    async with async_client as entered:
        assert entered is async_client
        assert async_client.requester.account_id == "AN-ACCOUNT"

    async_session_resource.delete.assert_awaited_once()


def _account_summary(
    *, account_id: str = "AN-ACCOUNT", expires_in: int = 60
) -> ig.session.v3.AccountSummary:
    return ig.session.v3.AccountSummary.model_validate(
        {
            "accountId": account_id,
            "clientId": "A-CLIENT",
            "lightstreamerEndpoint": "https://example.com",
            "oauthToken": {
                "access_token": "an-access-token",
                "expires_in": expires_in,
                "refresh_token": "a-refresh-token",
                "scope": "profile",
                "token_type": "Bearer",
            },
            "timezoneOffset": 0,
        }
    )


def _oauth_token(
    *, access_token: str = "an-access-token", refresh_token: str = "a-token"
) -> ig.session.v1.OAuthToken:
    return ig.session.v1.OAuthToken.model_validate(
        {
            "access_token": access_token,
            "expires_in": 60,
            "refresh_token": refresh_token,
            "scope": "profile",
            "token_type": "Bearer",
        }
    )


@pytest.fixture
def session_resource() -> mock.MagicMock:
    return mock.MagicMock()


@pytest.fixture
def client(session_resource: mock.MagicMock) -> Iterator[ig.Client]:
    with mock.patch(
        "_ig_trading.client.SessionResource",
        return_value=session_resource,
    ):
        yield ig.Client(http_session=mock.MagicMock())


def test_init_given_defaults(client: ig.Client) -> None:
    assert client.api_key == "a-key"
    assert client.username == "a-user"
    assert client.password == "a-password"
    assert client.refresh_threshold == ig.Client.default_refresh_threshold


def test_init_given_explicit_arguments(
    session_resource: mock.MagicMock,
) -> None:
    with mock.patch(
        "_ig_trading.client.SessionResource",
        return_value=session_resource,
    ):
        client: t.Final = ig.Client(
            api_key="explicit-key",
            http_session=mock.MagicMock(),
            password="explicit-password",
            refresh_threshold=10,
            username="explicit-user",
        )

    assert client.api_key == "explicit-key"
    assert client.username == "explicit-user"
    assert client.password == "explicit-password"
    assert client.refresh_threshold == dt.timedelta(seconds=10)


def test_login_sets_account_and_token(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    session_resource.create.return_value = _account_summary(
        account_id="AN-ACCOUNT"
    )

    try:
        client.login()

        assert client.requester.account_id == "AN-ACCOUNT"
        assert client.requester.bearer_token == "an-access-token"
        assert client.oauth_token is not None
        assert client.oauth_token.access_token == "an-access-token"
        assert client.prev_refresh_time <= dt.datetime.now(dt.timezone.utc)
        session_resource.create.assert_called_once_with(
            identifier="a-user", password="a-password"
        )
    finally:
        client.close()


def test_login_twice_stops_previous_refresh_thread(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    session_resource.create.return_value = _account_summary()

    try:
        client.login()
        first_thread: t.Final = client._refresh_token_thread
        assert first_thread is not None

        client.login()

        assert not first_thread.is_alive()
        assert client._refresh_token_thread is not None
        assert client._refresh_token_thread is not first_thread
    finally:
        client.close()


def test_logout_clears_account_and_token(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    session_resource.create.return_value = _account_summary()
    client.login()

    client.logout()

    assert client.requester.account_id is None
    assert client.requester.bearer_token is None
    session_resource.delete.assert_called_once()


def test_logout_stops_refresh_thread(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    session_resource.create.return_value = _account_summary()
    client.login()
    thread: t.Final = client._refresh_token_thread
    assert thread is not None

    client.logout()

    assert not thread.is_alive()
    assert client._refresh_token_thread is None


def test_logout_clears_token_despite_in_flight_refresh(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    # Regression test: unlike the async client's task cancellation, stopping
    # the background thread doesn't interrupt an in-flight `refresh_token()`
    # HTTP call. If `logout()` cleared the tokens *before* stopping (and
    # joining) that thread, a refresh already in flight could complete
    # afterwards and silently resurrect the bearer token it just cleared.
    session_resource.create.return_value = _account_summary()
    client.login()
    client._stop_refresh_token_thread()

    entered_refresh: t.Final = threading.Event()
    release_refresh: t.Final = threading.Event()

    def slow_refresh_token_create(
        *_: object, **__: object
    ) -> ig.session.v1.OAuthToken:
        entered_refresh.set()
        release_refresh.wait()
        return _oauth_token(access_token="resurrected-token")

    session_resource.refresh_token.create.side_effect = (
        slow_refresh_token_create
    )

    # Stand in for a scheduled refresh that happens to be mid-flight when
    # `logout()` is called, by putting a thread inside `refresh_token()`
    # and registering it as the client's background thread directly.
    refresh_thread = threading.Thread(target=client.refresh_token, daemon=True)
    client._refresh_token_thread = refresh_thread
    refresh_thread.start()
    assert entered_refresh.wait(timeout=1)

    threading.Timer(0.05, release_refresh.set).start()
    client.logout()

    assert client.requester.bearer_token is None
    assert client.requester.account_id is None


def test_logout_suppresses_oauth_token_invalid_error(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    session_resource.create.return_value = _account_summary()
    client.login()
    session_resource.delete.side_effect = ig.OAuthTokenInvalidError(
        status=401
    )

    client.logout()  # Doesn't raise.


def test_close_closes_owned_session(
    session_resource: mock.MagicMock,
) -> None:
    with (
        mock.patch(
            "_ig_trading.client.SessionResource",
            return_value=session_resource,
        ),
        mock.patch("_ig_trading.client.Session") as session,
    ):
        session.return_value = mock.MagicMock()
        client: t.Final = ig.Client()

        client.close()

        session.return_value.close.assert_called_once()


def test_close_does_not_close_given_session(
    client: ig.Client,
) -> None:
    client.close()
    client._http_session.close.assert_not_called()  # type: ignore[attr-defined]


def test_refresh_token(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    session_resource.create.return_value = _account_summary()
    client.login()

    session_resource.refresh_token.create.return_value = _oauth_token(
        access_token="a-new-access-token", refresh_token="a-new-refresh-token"
    )

    try:
        client.refresh_token()

        assert client.requester.bearer_token == "a-new-access-token"
        session_resource.refresh_token.create.assert_called_once_with(
            "a-refresh-token"
        )
    finally:
        client.close()


def test_refresh_token_given_no_token_does_nothing(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    client.refresh_token()
    session_resource.refresh_token.create.assert_not_called()


def test_auto_refresh_token_calls_refresh_token(
    client: ig.Client,
) -> None:
    client._oauth_token = _oauth_token()

    def _stop_the_loop() -> None:
        # `_auto_refresh_token`'s `while self._oauth_token:` loop otherwise
        # never ends. Clear the slot directly (bypassing the `_oauth_token`
        # setter, which assumes a real token and would crash on `None`).
        client._Client__oauth_token = None  # type: ignore[attr-defined]

    with (
        # Patch on the class, not the instance: `Client` uses `__slots__`
        # (with no `__dict__`), so instance-level patching would fail.
        mock.patch.object(
            ig.Client, "refresh_token", mock.Mock(side_effect=_stop_the_loop)
        ) as refresh_token,
        mock.patch.object(
            client._refresh_token_stop_event, "wait", return_value=False
        ),
    ):
        client._auto_refresh_token()

    refresh_token.assert_called_once()


def test_client_as_context_manager(
    client: ig.Client, session_resource: mock.MagicMock
) -> None:
    session_resource.create.return_value = _account_summary()

    with client as entered:
        assert entered is client
        assert client.requester.account_id == "AN-ACCOUNT"

    session_resource.delete.assert_called_once()
