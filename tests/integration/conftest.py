from __future__ import annotations

import asyncio as aio
import time
from unittest import mock

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator


@pytest.fixture(scope="session")
async def async_requester(
    _retry_rate_limited_requests: None,
) -> AsyncIterator[ig.AsyncAPIRequester]:
    requester: t.Final = ig.AsyncAPIRequester()
    session: t.Final = ig.AsyncSessionResource(requester)
    account: t.Final = await session.create()
    requester.account_id = account.account_id
    requester.bearer_token = account.oauth_token.access_token
    try:
        yield requester
    finally:
        await session.delete()


@pytest.fixture(scope="session")
def requester(_retry_rate_limited_requests: None) -> Iterator[ig.APIRequester]:
    requester: t.Final = ig.APIRequester()
    session: t.Final = ig.SessionResource(requester)
    account: t.Final = session.create()
    requester.account_id = account.account_id
    requester.bearer_token = account.oauth_token.access_token
    try:
        yield requester
    finally:
        session.delete()


_max_attempts: t.Final = 5


def _make_async_request_with_retry(
    request: t.Callable[..., t.Coroutine[object, object, dict[str, object]]],
) -> t.Callable[..., t.Coroutine[object, object, dict[str, object]]]:
    async def request_with_retry(
        self: ig.AsyncAPIRequester, *args: object, **kwargs: object
    ) -> dict[str, object]:
        for attempt in range(_max_attempts):
            try:
                return await request(self, *args, **kwargs)
            except ig.DealExecutionNotFoundError:  # noqa: PERF203
                if attempt == _max_attempts - 1:
                    raise

                await aio.sleep(1)
            except (
                ig.ExceededAPIKeyAllowanceError,
                ig.ExceededAccountAllowanceError,
                ig.ExceededAccountTradingAllowanceError,
                ig.ExceededAccountHistoricalDataAllowanceError,
            ):
                if attempt == _max_attempts - 1:
                    raise

                await aio.sleep(60)

        err: t.Final = "unreachable"
        raise AssertionError(err)

    return request_with_retry


def _make_request_with_retry(
    request: t.Callable[..., dict[str, object]],
) -> t.Callable[..., dict[str, object]]:
    def request_with_retry(
        self: ig.APIRequester, *args: object, **kwargs: object
    ) -> dict[str, object]:
        for attempt in range(_max_attempts):
            try:
                return request(self, *args, **kwargs)
            except ig.DealExecutionNotFoundError:  # noqa: PERF203
                if attempt == _max_attempts - 1:
                    raise

                time.sleep(1)
            except (
                ig.ExceededAPIKeyAllowanceError,
                ig.ExceededAccountAllowanceError,
                ig.ExceededAccountTradingAllowanceError,
                ig.ExceededAccountHistoricalDataAllowanceError,
            ):
                if attempt == _max_attempts - 1:
                    raise

                time.sleep(60)

        err: t.Final = "unreachable"
        raise AssertionError(err)

    return request_with_retry


@pytest.fixture(autouse=True, scope="session")
def _retry_rate_limited_requests() -> Iterator[None]:
    """Retry API calls that hit IG's rate limits or a known transient issue.

    The whole test suite shares one demo account/API key, so running it
    repeatedly can trip IG's traffic allowance. Rather than fail outright, wait
    a minute and retry instead of erroring the test.

    Separately, IG's demo environment can occasionally fail to find a deal
    (:class:`.DealExecutionNotFoundError`) for a moment right after it was
    created, even though the deal confirmation already succeeded. That resolves
    almost immediately, so retry it quickly instead.
    """
    with (
        mock.patch.object(
            ig.AsyncAPIRequester,
            "_request",
            _make_async_request_with_retry(ig.AsyncAPIRequester._request),
        ),
        mock.patch.object(
            ig.APIRequester,
            "_request",
            _make_request_with_retry(ig.APIRequester._request),
        ),
    ):
        yield
