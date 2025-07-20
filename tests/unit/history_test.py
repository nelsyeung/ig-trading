from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock


@pytest.fixture
def async_history(async_requester: mock.AsyncMock) -> ig.AsyncHistoryResource:
    return ig.AsyncHistoryResource(async_requester)


@pytest.fixture
def history(requester: mock.MagicMock) -> ig.HistoryResource:
    return ig.HistoryResource(requester)


_activity: t.Final = {
    "actionStatus": "ACCEPT",
    "activity": "Order",
    "activityHistoryId": "1",
    "channel": "WEB",
    "currency": "£",
    "date": "01/01/24",
    "dealId": "DEAL1",
    "epic": "CS.D.EURUSD.CFD.IP",
    "level": "1.1",
    "limit": "",
    "marketName": "EUR/USD",
    "period": "-",
    "result": "SUCCESS",
    "size": "1",
    "stop": "",
    "stopType": "",
    "time": "12:00",
}
_transaction: t.Final = {
    "cashTransaction": False,
    "closeLevel": "1.2",
    "currency": "£",
    "date": "01-Jan-2024",
    "instrumentName": "EUR/USD",
    "openLevel": "1.1",
    "period": "-",
    "profitAndLoss": "£10.00",
    "reference": "REF1",
    "size": "+1",
    "transactionType": "ALL_DEAL",
}


async def test_async_activity_list_given_date_range(
    async_history: ig.AsyncHistoryResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"activities": [_activity]}

    result: t.Final = await async_history.activity.list(
        from_date="01-01-2024", to_date="02-01-2024"
    )

    async_requester.get.assert_awaited_once_with(
        "history/activity/01-01-2024/02-01-2024"
    )
    assert result == (ig.history.v1.Activity.model_validate(_activity),)


async def test_async_activity_list_given_last_period(
    async_history: ig.AsyncHistoryResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"activities": [_activity]}

    await async_history.activity.list(last_period=600000)

    async_requester.get.assert_awaited_once_with("history/activity/600000")


async def test_async_activity_list_given_neither(
    async_history: ig.AsyncHistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one of"):
        await async_history.activity.list()


async def test_async_activity_list_given_both(
    async_history: ig.AsyncHistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one of"):
        await async_history.activity.list(
            from_date="01-01-2024", to_date="02-01-2024", last_period=600000
        )


async def test_async_activity_list_given_from_date_without_to_date(
    async_history: ig.AsyncHistoryResource,
) -> None:
    with pytest.raises(ValueError, match="must be given together"):
        await async_history.activity.list(from_date="01-01-2024")


async def test_async_transactions_list_given_date_range(
    async_history: ig.AsyncHistoryResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"transactions": [_transaction]}

    result: t.Final = await async_history.transactions.list(
        from_date="01-01-2024",
        to_date="02-01-2024",
        transaction_type="DEPOSIT",
    )

    async_requester.get.assert_awaited_once_with(
        "history/transactions/DEPOSIT/01-01-2024/02-01-2024"
    )
    assert result == (ig.history.v1.Transaction.model_validate(_transaction),)


async def test_async_transactions_list_given_last_period_default_type(
    async_history: ig.AsyncHistoryResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"transactions": [_transaction]}

    await async_history.transactions.list(last_period=600000)

    async_requester.get.assert_awaited_once_with(
        "history/transactions/ALL/600000"
    )


async def test_async_transactions_list_given_neither(
    async_history: ig.AsyncHistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one of"):
        await async_history.transactions.list()


async def test_async_transactions_list_given_to_date_without_from_date(
    async_history: ig.AsyncHistoryResource,
) -> None:
    with pytest.raises(ValueError, match="must be given together"):
        await async_history.transactions.list(to_date="02-01-2024")


def test_activity_list_given_date_range(
    history: ig.HistoryResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"activities": [_activity]}

    result: t.Final = history.activity.list(
        from_date="01-01-2024", to_date="02-01-2024"
    )

    requester.get.assert_called_once_with(
        "history/activity/01-01-2024/02-01-2024"
    )
    assert result == (ig.history.v1.Activity.model_validate(_activity),)


def test_activity_list_given_last_period(
    history: ig.HistoryResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"activities": [_activity]}

    history.activity.list(last_period=600000)

    requester.get.assert_called_once_with("history/activity/600000")


def test_activity_list_given_neither(
    history: ig.HistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one of"):
        history.activity.list()


def test_activity_list_given_both(
    history: ig.HistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one of"):
        history.activity.list(
            from_date="01-01-2024", to_date="02-01-2024", last_period=600000
        )


def test_activity_list_given_from_date_without_to_date(
    history: ig.HistoryResource,
) -> None:
    with pytest.raises(ValueError, match="must be given together"):
        history.activity.list(from_date="01-01-2024")


def test_transactions_list_given_date_range(
    history: ig.HistoryResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"transactions": [_transaction]}

    result: t.Final = history.transactions.list(
        from_date="01-01-2024",
        to_date="02-01-2024",
        transaction_type="DEPOSIT",
    )

    requester.get.assert_called_once_with(
        "history/transactions/DEPOSIT/01-01-2024/02-01-2024"
    )
    assert result == (ig.history.v1.Transaction.model_validate(_transaction),)


def test_transactions_list_given_last_period_default_type(
    history: ig.HistoryResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"transactions": [_transaction]}

    history.transactions.list(last_period=600000)

    requester.get.assert_called_once_with("history/transactions/ALL/600000")


def test_transactions_list_given_neither(
    history: ig.HistoryResource,
) -> None:
    with pytest.raises(ValueError, match="exactly one of"):
        history.transactions.list()


def test_transactions_list_given_to_date_without_from_date(
    history: ig.HistoryResource,
) -> None:
    with pytest.raises(ValueError, match="must be given together"):
        history.transactions.list(to_date="02-01-2024")
