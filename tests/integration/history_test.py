from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

_thirty_days_ms: t.Final = 30 * 24 * 60 * 60 * 1000


@pytest.fixture
def async_history(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncHistoryResource:
    return ig.AsyncHistoryResource(async_requester)


@pytest.fixture
def history(requester: ig.APIRequester) -> ig.HistoryResource:
    return ig.HistoryResource(requester)


async def test_async_activity_list_given_last_period(
    async_history: ig.AsyncHistoryResource,
) -> None:
    activities: t.Final = await async_history.activity.list(
        last_period=_thirty_days_ms
    )
    assert all(
        isinstance(activity, ig.history.v1.Activity) for activity in activities
    )


async def test_async_activity_list_given_neither(
    async_history: ig.AsyncHistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one"):
        await async_history.activity.list()


async def test_async_activity_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncHistoryResource().activity.list(
            last_period=_thirty_days_ms
        )


async def test_async_transactions_list_given_last_period(
    async_history: ig.AsyncHistoryResource,
) -> None:
    result: t.Final = await async_history.transactions.list(
        last_period=_thirty_days_ms
    )
    assert all(
        isinstance(transaction, ig.history.v1.Transaction)
        for transaction in result
    )


async def test_async_transactions_list_given_neither(
    async_history: ig.AsyncHistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one"):
        await async_history.transactions.list()


async def test_async_transactions_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncHistoryResource().transactions.list(
            last_period=_thirty_days_ms
        )


def test_activity_list_given_last_period(
    history: ig.HistoryResource,
) -> None:
    activities: t.Final = history.activity.list(last_period=_thirty_days_ms)
    assert all(
        isinstance(activity, ig.history.v1.Activity) for activity in activities
    )


def test_activity_list_given_neither(history: ig.HistoryResource) -> None:
    with pytest.raises(ValueError, match="exactly one"):
        history.activity.list()


def test_activity_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.HistoryResource().activity.list(last_period=_thirty_days_ms)


def test_transactions_list_given_last_period(
    history: ig.HistoryResource,
) -> None:
    result: t.Final = history.transactions.list(last_period=_thirty_days_ms)
    assert all(
        isinstance(transaction, ig.history.v1.Transaction)
        for transaction in result
    )


def test_transactions_list_given_neither(
    history: ig.HistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one"):
        history.transactions.list()


def test_transactions_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.HistoryResource().transactions.list(last_period=_thirty_days_ms)
