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


# Cheap per-attempt cost (1s), so worth retrying persistently: these transient
# errors have been observed to sometimes outlast even a 10-attempt budget (this
# project's test suite runs several deal-execution operations against a shared
# demo account, and IG's confirmation propagation delay seems to grow, not stay
# "brief", under that load), and a few extra seconds of wall-clock time in that
# case is a much better trade than a flaky CI failure.
_quick_max_attempts: t.Final = 30
# Expensive per-attempt cost (60s): kept lower so a genuinely exhausted
# allowance doesn't stall a run for too long before giving up.
_slow_max_attempts: t.Final = 5


def _make_async_request_with_retry(
    request: t.Callable[..., t.Coroutine[object, object, dict[str, object]]],
) -> t.Callable[..., t.Coroutine[object, object, dict[str, object]]]:
    async def request_with_retry(
        self: ig.AsyncAPIRequester, *args: object, **kwargs: object
    ) -> dict[str, object]:
        quick_attempt = 0
        slow_attempt = 0

        while True:
            try:
                return await request(self, *args, **kwargs)
            except (  # noqa: PERF203
                ig.DealExecutionNotFoundError,
                ig.PositionNotionalDetailsNullError,
                ig.SessionAuthenticationFailureError,
            ):
                quick_attempt += 1
                if quick_attempt == _quick_max_attempts:
                    raise

                await aio.sleep(1)
            except (
                ig.ExceededAPIKeyAllowanceError,
                ig.ExceededAccountAllowanceError,
                ig.ExceededAccountTradingAllowanceError,
            ):
                slow_attempt += 1
                if slow_attempt == _slow_max_attempts:
                    raise

                await aio.sleep(60)

    return request_with_retry


def _make_request_with_retry(
    request: t.Callable[..., dict[str, object]],
) -> t.Callable[..., dict[str, object]]:
    def request_with_retry(
        self: ig.APIRequester, *args: object, **kwargs: object
    ) -> dict[str, object]:
        quick_attempt = 0
        slow_attempt = 0

        while True:
            try:
                return request(self, *args, **kwargs)
            except (  # noqa: PERF203
                ig.DealExecutionNotFoundError,
                ig.PositionNotionalDetailsNullError,
                ig.SessionAuthenticationFailureError,
            ):
                quick_attempt += 1
                if quick_attempt == _quick_max_attempts:
                    raise

                time.sleep(1)
            except (
                ig.ExceededAPIKeyAllowanceError,
                ig.ExceededAccountAllowanceError,
                ig.ExceededAccountTradingAllowanceError,
            ):
                slow_attempt += 1
                if slow_attempt == _slow_max_attempts:
                    raise

                time.sleep(60)

    return request_with_retry


@pytest.fixture(autouse=True, scope="session")
def _retry_rate_limited_requests() -> Iterator[None]:
    """Retry API calls that hit IG's rate limits or a known transient issue.

    The whole test suite shares one demo account/API key, so running it
    repeatedly can trip IG's traffic allowance. Rather than fail outright, wait
    a minute and retry instead of erroring the test.

    :class:`.ExceededAccountHistoricalDataAllowanceError` is deliberately
    *not* retried here: unlike the other allowance errors (which reset within
    seconds/minutes), IG's historical data allowance is a much longer-lived
    quota, so retrying it for a few minutes can't help and only makes a
    failing run take that much longer before reporting the (same) failure.

    Separately, IG's demo environment can occasionally fail to find a deal
    (:class:`.DealExecutionNotFoundError`), compute a position's market value
    (:class:`.PositionNotionalDetailsNullError`), or authenticate a session
    created shortly after another one
    (:class:`.SessionAuthenticationFailureError`). These resolve almost
    immediately, so retry them quickly instead.
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
