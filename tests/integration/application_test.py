from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig


@pytest.fixture
def async_application(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncApplicationResource:
    return ig.AsyncApplicationResource(async_requester)


@pytest.fixture
def application(requester: ig.APIRequester) -> ig.ApplicationResource:
    return ig.ApplicationResource(requester)


async def test_async_list(
    async_application: ig.AsyncApplicationResource,
) -> None:
    applications: t.Final = await async_application.list()
    assert applications
    assert all(
        isinstance(app, ig.application.v1.Application) for app in applications
    )


async def test_async_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncApplicationResource().list()


def test_list(application: ig.ApplicationResource) -> None:
    applications: t.Final = application.list()
    assert applications
    assert all(
        isinstance(app, ig.application.v1.Application) for app in applications
    )


def test_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.ApplicationResource().list()
