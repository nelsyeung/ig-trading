from __future__ import annotations

import typing_extensions as t

import ig_trading as ig
from _ig_trading.resource import AsyncResource, Resource

if t.TYPE_CHECKING:
    from unittest import mock

    import pytest


def test_async_init_given_requester(async_requester: mock.AsyncMock) -> None:
    resource: t.Final = AsyncResource(async_requester)
    assert resource._requester is async_requester


def test_async_init_given_no_requester(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IG_API_KEY", "key")
    resource: t.Final = AsyncResource()
    assert isinstance(resource._requester, ig.AsyncAPIRequester)


def test_init_given_requester(requester: mock.MagicMock) -> None:
    resource: t.Final = Resource(requester)
    assert resource._requester is requester


def test_init_given_no_requester(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("IG_API_KEY", "key")
    resource: t.Final = Resource()
    assert isinstance(resource._requester, ig.APIRequester)
