from __future__ import annotations

import typing_extensions as t

from _ig_trading.history import v1
from _ig_trading.resource import AsyncResource, Resource

if t.TYPE_CHECKING:
    from _ig_trading.api_requester import APIRequester, AsyncAPIRequester


class AsyncHistoryResource(AsyncResource):
    """Account history resource: ``/history``."""

    __slots__ = ("activity", "transactions")

    def __init__(self, requester: AsyncAPIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.activity: t.Final = AsyncHistoryActivityResource(requester)
        self.transactions: t.Final = AsyncHistoryTransactionsResource(
            requester
        )


class AsyncHistoryActivityResource(AsyncResource):
    """Account activity history resource: ``/history/activity``."""

    __slots__ = ()

    url: t.Final = "history/activity"

    async def list(
        self,
        *,
        from_date: str | None = None,
        last_period: int | None = None,
        to_date: str | None = None,
    ) -> tuple[v1.Activity, ...]:
        """Returns the account activity history.

        ``GET /history/activity/{from_date}/{to_date}`` or
        ``GET /history/activity/{last_period}``

        Args:
            from_date: Start date, in ``dd-mm-yyyy`` format. Mutually exclusive
                with ``last_period``, and must be given together with
                ``to_date``. Defaults to ``None``.
            last_period: Interval, in milliseconds, to fetch activity for.
                Mutually exclusive with ``from_date``/``to_date``. Defaults to
                ``None``.
            to_date: End date, in ``dd-mm-yyyy`` format. Mutually exclusive
                with ``last_period``, and must be given together with
                ``from_date``. Defaults to ``None``.
        """
        if (from_date is None) != (to_date is None):
            err = "`from_date` and `to_date` must be given together"
            raise ValueError(err)

        if (from_date is not None) == (last_period is not None):
            err = (
                "exactly one of (`from_date`, `to_date`) or `last_period` "
                "must be given"
            )
            raise ValueError(err)

        url: t.Final = (
            f"{self.url}/{from_date}/{to_date}"
            if from_date is not None
            else f"{self.url}/{last_period}"
        )
        return tuple(
            v1.Activity.model_validate(activity)
            for activity in (  # type: ignore[attr-defined]
                await self._requester.get(url)
            )["activities"]
        )


class AsyncHistoryTransactionsResource(AsyncResource):
    """Account transaction history resource: ``/history/transactions``."""

    __slots__ = ()

    url: t.Final = "history/transactions"

    async def list(
        self,
        *,
        from_date: str | None = None,
        last_period: int | None = None,
        to_date: str | None = None,
        transaction_type: v1.TransactionType = "ALL",
    ) -> tuple[v1.Transaction, ...]:
        """Returns the account transaction history.

        ``GET /history/transactions/{transaction_type}/{from_date}/{to_date}``
        or ``GET /history/transactions/{transaction_type}/{last_period}``

        Args:
            from_date: Start date, in ``dd-mm-yyyy`` format. Mutually exclusive
                with ``last_period``, and must be given together with
                ``to_date``. Defaults to ``None``.
            last_period: Interval, in milliseconds, to fetch transactions for.
                Mutually exclusive with ``from_date``/``to_date``. Defaults to
                ``None``.
            to_date: End date, in ``dd-mm-yyyy`` format. Mutually exclusive
                with ``last_period``, and must be given together with
                ``from_date``. Defaults to ``None``.
            transaction_type: The type of transaction to filter by. Defaults
                to ``ALL``.
        """
        if (from_date is None) != (to_date is None):
            err = "`from_date` and `to_date` must be given together"
            raise ValueError(err)

        if (from_date is not None) == (last_period is not None):
            err = (
                "exactly one of (`from_date`, `to_date`) or `last_period` "
                "must be given"
            )
            raise ValueError(err)

        url: t.Final = (
            f"{self.url}/{transaction_type}/{from_date}/{to_date}"
            if from_date is not None
            else f"{self.url}/{transaction_type}/{last_period}"
        )
        return tuple(
            v1.Transaction.model_validate(transaction)
            for transaction in (  # type: ignore[attr-defined]
                await self._requester.get(url)
            )["transactions"]
        )


class HistoryResource(Resource):
    """Account history resource: ``/history``."""

    __slots__ = ("activity", "transactions")

    def __init__(self, requester: APIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.activity: t.Final = HistoryActivityResource(requester)
        self.transactions: t.Final = HistoryTransactionsResource(requester)


class HistoryActivityResource(Resource):
    """Account activity history resource: ``/history/activity``."""

    __slots__ = ()

    url: t.Final = "history/activity"

    def list(
        self,
        *,
        from_date: str | None = None,
        last_period: int | None = None,
        to_date: str | None = None,
    ) -> tuple[v1.Activity, ...]:
        """Returns the account activity history.

        ``GET /history/activity/{from_date}/{to_date}`` or
        ``GET /history/activity/{last_period}``

        Args:
            from_date: Start date, in ``dd-mm-yyyy`` format. Mutually exclusive
                with ``last_period``, and must be given together with
                ``to_date``. Defaults to ``None``.
            last_period: Interval, in milliseconds, to fetch activity for.
                Mutually exclusive with ``from_date``/``to_date``. Defaults to
                ``None``.
            to_date: End date, in ``dd-mm-yyyy`` format. Mutually exclusive
                with ``last_period``, and must be given together with
                ``from_date``. Defaults to ``None``.
        """
        if (from_date is None) != (to_date is None):
            err = "`from_date` and `to_date` must be given together"
            raise ValueError(err)

        if (from_date is not None) == (last_period is not None):
            err = (
                "exactly one of (`from_date`, `to_date`) or `last_period` "
                "must be given"
            )
            raise ValueError(err)

        url: t.Final = (
            f"{self.url}/{from_date}/{to_date}"
            if from_date is not None
            else f"{self.url}/{last_period}"
        )
        return tuple(
            v1.Activity.model_validate(activity)
            for activity in (  # type: ignore[attr-defined]
                self._requester.get(url)
            )["activities"]
        )


class HistoryTransactionsResource(Resource):
    """Account transaction history resource: ``/history/transactions``."""

    __slots__ = ()

    url: t.Final = "history/transactions"

    def list(
        self,
        *,
        from_date: str | None = None,
        last_period: int | None = None,
        to_date: str | None = None,
        transaction_type: v1.TransactionType = "ALL",
    ) -> tuple[v1.Transaction, ...]:
        """Returns the account transaction history.

        ``GET /history/transactions/{transaction_type}/{from_date}/{to_date}``
        or ``GET /history/transactions/{transaction_type}/{last_period}``

        Args:
            from_date: Start date, in ``dd-mm-yyyy`` format. Mutually exclusive
                with ``last_period``, and must be given together with
                ``to_date``. Defaults to ``None``.
            last_period: Interval, in milliseconds, to fetch transactions for.
                Mutually exclusive with ``from_date``/``to_date``. Defaults to
                ``None``.
            to_date: End date, in ``dd-mm-yyyy`` format. Mutually exclusive
                with ``last_period``, and must be given together with
                ``from_date``. Defaults to ``None``.
            transaction_type: The type of transaction to filter by. Defaults
                to ``ALL``.
        """
        if (from_date is None) != (to_date is None):
            err = "`from_date` and `to_date` must be given together"
            raise ValueError(err)

        if (from_date is not None) == (last_period is not None):
            err = (
                "exactly one of (`from_date`, `to_date`) or `last_period` "
                "must be given"
            )
            raise ValueError(err)

        url: t.Final = (
            f"{self.url}/{transaction_type}/{from_date}/{to_date}"
            if from_date is not None
            else f"{self.url}/{transaction_type}/{last_period}"
        )
        return tuple(
            v1.Transaction.model_validate(transaction)
            for transaction in (  # type: ignore[attr-defined]
                self._requester.get(url)
            )["transactions"]
        )
