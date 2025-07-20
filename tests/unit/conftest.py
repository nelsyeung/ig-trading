from __future__ import annotations

from unittest import mock

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from collections.abc import Mapping


@pytest.fixture
def async_requester() -> mock.AsyncMock:
    """A fake :class:`ig.AsyncAPIRequester` that never touches the network."""
    return mock.AsyncMock(spec=ig.AsyncAPIRequester)


@pytest.fixture
def requester() -> mock.MagicMock:
    """A fake :class:`ig.APIRequester` that never touches the network."""
    return mock.MagicMock(spec=ig.APIRequester)


def make_response(
    *,
    content_type: str = "application/json",
    headers: Mapping[str, str] | None = None,
    json: object = None,
    ok: bool = True,
    status: int = 200,
    text: str = "",
) -> mock.AsyncMock:
    """A fake :class:`aiohttp.ClientResponse`."""
    response: t.Final = mock.AsyncMock()
    response.content_type = content_type
    response.headers = dict(headers or {})
    response.json = mock.AsyncMock(return_value=json)
    response.ok = ok
    response.status = status
    response.text = mock.AsyncMock(return_value=text)
    return response


def make_sync_response(
    *,
    content: bytes = b"{}",
    headers: Mapping[str, str] | None = None,
    json: object = None,
    ok: bool = True,
    status_code: int = 200,
    text: str = "",
) -> mock.MagicMock:
    """A fake :class:`requests.Response`."""
    response: t.Final = mock.MagicMock()
    response.content = content
    response.headers = {"Content-Type": "application/json", **(headers or {})}
    response.json = mock.Mock(return_value=json)
    response.ok = ok
    response.status_code = status_code
    response.text = text
    return response
