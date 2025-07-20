from __future__ import annotations

import typing as t

from _ig_trading.api_requester import APIRequester, AsyncAPIRequester


class AsyncResource:
    """API resource base class.

    Args:
        requester: A REST API requester.
    """

    __slots__ = ("_requester",)

    def __init__(self, requester: AsyncAPIRequester | None = None, /) -> None:
        self._requester: t.Final = requester or AsyncAPIRequester()


class Resource:
    """API resource base class.

    Args:
        requester: A REST API requester.
    """

    __slots__ = ("_requester",)

    def __init__(self, requester: APIRequester | None = None, /) -> None:
        self._requester: t.Final = requester or APIRequester()
