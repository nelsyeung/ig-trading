from __future__ import annotations

from unittest import mock

import pytest
import typing_extensions as t

import ig_trading as ig
from tests.unit.conftest import make_response, make_sync_response


@pytest.fixture
def async_http_session() -> mock.AsyncMock:
    # `aiohttp.ClientSession.request` is not an `async def` method (it returns
    # a hybrid awaitable/context-manager object instead), so autospeccing it
    # would make `.request` a plain, non-awaitable `Mock`.
    return mock.AsyncMock()


@pytest.fixture
def async_requester(
    async_http_session: mock.AsyncMock,
) -> ig.AsyncAPIRequester:
    return ig.AsyncAPIRequester(http_session=async_http_session, key="a-key")


def test_async_headers_given_only_key(
    async_requester: ig.AsyncAPIRequester,
) -> None:
    assert async_requester.headers == {"X-IG-API-KEY": "a-key"}


def test_async_headers_given_everything(
    async_requester: ig.AsyncAPIRequester,
) -> None:
    async_requester.bearer_token = "a-token"
    async_requester.cst = "a-cst"
    async_requester.account_id = "an-account"
    async_requester.x_security_token = "a-security-token"

    assert async_requester.headers == {
        "X-IG-API-KEY": "a-key",
        "Authorization": "Bearer a-token",
        "CST": "a-cst",
        "IG-ACCOUNT-ID": "an-account",
        "X-SECURITY-TOKEN": "a-security-token",
    }


async def test_async_get_given_success(
    async_http_session: mock.AsyncMock, async_requester: ig.AsyncAPIRequester
) -> None:
    async_http_session.request.return_value = make_response(
        headers={"CST": "new-cst", "X-SECURITY-TOKEN": "new-token"},
        json={"key": "value"},
    )

    result: t.Final = await async_requester.get(
        "some/url", params={"a": 1}, version=2
    )

    assert result == {"key": "value"}
    assert async_requester.cst == "new-cst"
    assert async_requester.x_security_token == "new-token"
    async_http_session.request.assert_awaited_once_with(
        "GET",
        f"{async_requester.url}/some/url",
        headers={"X-IG-API-KEY": "a-key", "VERSION": "2"},
        params={"a": 1},
        json=None,
    )


async def test_async_post_sends_json_body(
    async_http_session: mock.AsyncMock, async_requester: ig.AsyncAPIRequester
) -> None:
    async_http_session.request.return_value = make_response(json={})

    await async_requester.post("some/url", json={"a": 1})

    async_http_session.request.assert_awaited_once_with(
        "POST",
        f"{async_requester.url}/some/url",
        headers={"X-IG-API-KEY": "a-key"},
        params=None,
        json={"a": 1},
    )


async def test_async_put_sends_json_body(
    async_http_session: mock.AsyncMock, async_requester: ig.AsyncAPIRequester
) -> None:
    async_http_session.request.return_value = make_response(json={})

    await async_requester.put("some/url", json={"a": 1})

    async_http_session.request.assert_awaited_once_with(
        "PUT",
        f"{async_requester.url}/some/url",
        headers={"X-IG-API-KEY": "a-key"},
        params=None,
        json={"a": 1},
    )


async def test_async_delete_sends_post_with_method_header(
    async_http_session: mock.AsyncMock, async_requester: ig.AsyncAPIRequester
) -> None:
    async_http_session.request.return_value = make_response(json={})

    await async_requester.delete("some/url", json={"a": 1})

    async_http_session.request.assert_awaited_once_with(
        "POST",
        f"{async_requester.url}/some/url",
        headers={"X-IG-API-KEY": "a-key", "_method": "DELETE"},
        params=None,
        json={"a": 1},
    )


async def test_async_request_given_known_error(
    async_http_session: mock.AsyncMock, async_requester: ig.AsyncAPIRequester
) -> None:
    status: t.Final = 404
    async_http_session.request.return_value = make_response(
        json={"errorCode": "error.confirms.deal-not-found"},
        ok=False,
        status=status,
    )

    with pytest.raises(ig.DealNotFoundError) as exc_info:
        await async_requester.get("some/url")

    assert exc_info.value.status == status


async def test_async_request_given_unrecognized_json_error(
    async_http_session: mock.AsyncMock, async_requester: ig.AsyncAPIRequester
) -> None:
    status: t.Final = 500
    async_http_session.request.return_value = make_response(
        json={"errorCode": "some.unrecognized.error"},
        ok=False,
        status=status,
        text='{"errorCode": "some.unrecognized.error"}',
    )

    with pytest.raises(ig.UnknownAPIError) as exc_info:
        await async_requester.get("some/url")

    # Unrecognized JSON error codes still fall back to a generic error code;
    # only the raw response body distinguishes them.
    assert exc_info.value.error_code == "_unknown"
    assert exc_info.value.description == (
        '{"errorCode": "some.unrecognized.error"}'
    )
    assert exc_info.value.status == status


async def test_async_request_given_non_json_error(
    async_http_session: mock.AsyncMock, async_requester: ig.AsyncAPIRequester
) -> None:
    status: t.Final = 502
    async_http_session.request.return_value = make_response(
        content_type="text/plain",
        ok=False,
        status=status,
        text="Bad Gateway",
    )

    with pytest.raises(ig.UnknownAPIError) as exc_info:
        await async_requester.get("some/url")

    assert exc_info.value.description == "Bad Gateway"
    assert exc_info.value.status == status


async def test_async_request_opens_own_session_when_none_given() -> None:
    requester: t.Final = ig.AsyncAPIRequester(key="a-key")
    response: t.Final = make_response(json={})

    session: t.Final = mock.AsyncMock()
    session.__aenter__.return_value = session
    session.request.return_value = response

    with mock.patch(
        "_ig_trading.api_requester.AsyncSession", return_value=session
    ):
        result: t.Final = await requester.get("some/url")

    assert result == {}
    session.request.assert_awaited_once()


@pytest.fixture
def http_session() -> mock.MagicMock:
    return mock.MagicMock()


@pytest.fixture
def requester(http_session: mock.MagicMock) -> ig.APIRequester:
    return ig.APIRequester(http_session=http_session, key="a-key")


def test_headers_given_only_key(requester: ig.APIRequester) -> None:
    assert requester.headers == {"X-IG-API-KEY": "a-key"}


def test_headers_given_everything(
    requester: ig.APIRequester,
) -> None:
    requester.bearer_token = "a-token"
    requester.cst = "a-cst"
    requester.account_id = "an-account"
    requester.x_security_token = "a-security-token"

    assert requester.headers == {
        "X-IG-API-KEY": "a-key",
        "Authorization": "Bearer a-token",
        "CST": "a-cst",
        "IG-ACCOUNT-ID": "an-account",
        "X-SECURITY-TOKEN": "a-security-token",
    }


def test_get_given_success(
    http_session: mock.MagicMock, requester: ig.APIRequester
) -> None:
    http_session.request.return_value = make_sync_response(
        headers={"CST": "new-cst", "X-SECURITY-TOKEN": "new-token"},
        json={"key": "value"},
    )

    result: t.Final = requester.get("some/url", params={"a": 1}, version=2)

    assert result == {"key": "value"}
    assert requester.cst == "new-cst"
    assert requester.x_security_token == "new-token"
    http_session.request.assert_called_once_with(
        "GET",
        f"{requester.url}/some/url",
        headers={"X-IG-API-KEY": "a-key", "VERSION": "2"},
        params={"a": 1},
        json=None,
    )


def test_post_sends_json_body(
    http_session: mock.MagicMock, requester: ig.APIRequester
) -> None:
    http_session.request.return_value = make_sync_response(json={})

    requester.post("some/url", json={"a": 1})

    http_session.request.assert_called_once_with(
        "POST",
        f"{requester.url}/some/url",
        headers={"X-IG-API-KEY": "a-key"},
        params=None,
        json={"a": 1},
    )


def test_put_sends_json_body(
    http_session: mock.MagicMock, requester: ig.APIRequester
) -> None:
    http_session.request.return_value = make_sync_response(json={})

    requester.put("some/url", json={"a": 1})

    http_session.request.assert_called_once_with(
        "PUT",
        f"{requester.url}/some/url",
        headers={"X-IG-API-KEY": "a-key"},
        params=None,
        json={"a": 1},
    )


def test_delete_sends_post_with_method_header(
    http_session: mock.MagicMock, requester: ig.APIRequester
) -> None:
    http_session.request.return_value = make_sync_response(json={})

    requester.delete("some/url", json={"a": 1})

    http_session.request.assert_called_once_with(
        "POST",
        f"{requester.url}/some/url",
        headers={"X-IG-API-KEY": "a-key", "_method": "DELETE"},
        params=None,
        json={"a": 1},
    )


def test_get_given_empty_body_success(
    http_session: mock.MagicMock, requester: ig.APIRequester
) -> None:
    # IG's `204 No Content` responses (e.g. `DELETE /session`) still claim a
    # JSON content type but have a genuinely empty body, which `requests`
    # (unlike aiohttp) refuses to `.json()`-decode.
    http_session.request.return_value = make_sync_response(
        content=b"", status_code=204
    )

    result: t.Final = requester.get("some/url")

    assert result is None


def test_request_given_known_error(
    http_session: mock.MagicMock, requester: ig.APIRequester
) -> None:
    status: t.Final = 404
    http_session.request.return_value = make_sync_response(
        json={"errorCode": "error.confirms.deal-not-found"},
        ok=False,
        status_code=status,
    )

    with pytest.raises(ig.DealNotFoundError) as exc_info:
        requester.get("some/url")

    assert exc_info.value.status == status


def test_request_given_unrecognized_json_error(
    http_session: mock.MagicMock, requester: ig.APIRequester
) -> None:
    status: t.Final = 500
    http_session.request.return_value = make_sync_response(
        json={"errorCode": "some.unrecognized.error"},
        ok=False,
        status_code=status,
        text='{"errorCode": "some.unrecognized.error"}',
    )

    with pytest.raises(ig.UnknownAPIError) as exc_info:
        requester.get("some/url")

    assert exc_info.value.error_code == "_unknown"
    assert exc_info.value.description == (
        '{"errorCode": "some.unrecognized.error"}'
    )
    assert exc_info.value.status == status


def test_request_given_non_json_error(
    http_session: mock.MagicMock, requester: ig.APIRequester
) -> None:
    status: t.Final = 502
    http_session.request.return_value = make_sync_response(
        headers={"Content-Type": "text/plain"},
        ok=False,
        status_code=status,
        text="Bad Gateway",
    )

    with pytest.raises(ig.UnknownAPIError) as exc_info:
        requester.get("some/url")

    assert exc_info.value.description == "Bad Gateway"
    assert exc_info.value.status == status


def test_request_opens_own_session_when_none_given() -> None:
    requester: t.Final = ig.APIRequester(key="a-key")
    response: t.Final = make_sync_response(json={})

    session: t.Final = mock.MagicMock()
    session.__enter__.return_value = session
    session.request.return_value = response

    with mock.patch("_ig_trading.api_requester.Session", return_value=session):
        result: t.Final = requester.get("some/url")

    assert result == {}
    session.request.assert_called_once()
