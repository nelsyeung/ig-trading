from __future__ import annotations

import typing_extensions as t

from _ig_trading.markets.v1 import MarketOverview
from _ig_trading.resource import AsyncResource, Resource
from _ig_trading.watchlists import v1

if t.TYPE_CHECKING:
    from collections.abc import Iterable


class AsyncWatchlistsResource(AsyncResource):
    """Watchlists resource: ``/watchlists``."""

    __slots__ = ()

    url: t.Final = "watchlists"

    async def create(
        self, name: str, /, *, epics: Iterable[str] | None = None
    ) -> v1.CreateResult:
        """Creates a new watchlist.

        ``POST /watchlists``

        Args:
            name: Watchlist name.
            epics: Market epics to be associated with this new watchlist.
                Defaults to ``None``.
        """
        return v1.CreateResult.model_validate(
            await self._requester.post(
                self.url,
                json={
                    "name": name,
                    **({"epics": list(epics)} if epics is not None else {}),
                },
            )
        )

    async def delete(
        self, watchlist_id: str, epic: str | None = None, /
    ) -> v1.DeleteStatus:
        """Deletes the given watchlist, or removes a market from it.

        ``DELETE /watchlists/{watchlist_id}`` or
        ``DELETE /watchlists/{watchlist_id}/{epic}``

        Args:
            watchlist_id: The watchlist identifier.
            epic: Instrument epic identifier of the market to remove. If
                ``None``, the whole watchlist is deleted instead. Defaults to
                ``None``.
        """
        url: t.Final = (
            f"{self.url}/{watchlist_id}/{epic}"
            if epic is not None
            else f"{self.url}/{watchlist_id}"
        )
        return (await self._requester.delete(url, json={}))["status"]  # type: ignore[return-value]

    async def get(self, watchlist_id: str, /) -> tuple[MarketOverview, ...]:
        """Returns the markets in the given watchlist.

        ``GET /watchlists/{watchlist_id}``

        Args:
            watchlist_id: The watchlist identifier.
        """
        return tuple(
            MarketOverview.model_validate(market)
            for market in (  # type: ignore[attr-defined]
                await self._requester.get(f"{self.url}/{watchlist_id}")
            )["markets"]
        )

    async def list(self) -> tuple[v1.Watchlist, ...]:
        """Returns all watchlists belonging to the active account.

        ``GET /watchlists``
        """
        return tuple(
            v1.Watchlist.model_validate(watchlist)
            for watchlist in (  # type: ignore[attr-defined]
                await self._requester.get(self.url)
            )["watchlists"]
        )

    async def update(
        self, watchlist_id: str, /, *, epic: str
    ) -> v1.UpdateStatus:
        """Adds a market to the given watchlist.

        ``PUT /watchlists/{watchlist_id}``

        Args:
            watchlist_id: The watchlist identifier.
            epic: Instrument epic identifier.
        """
        return (  # type: ignore[return-value]
            await self._requester.put(
                f"{self.url}/{watchlist_id}", json={"epic": epic}
            )
        )["status"]


class WatchlistsResource(Resource):
    """Watchlists resource: ``/watchlists``."""

    __slots__ = ()

    url: t.Final = "watchlists"

    def create(
        self, name: str, /, *, epics: Iterable[str] | None = None
    ) -> v1.CreateResult:
        """Creates a new watchlist.

        ``POST /watchlists``

        Args:
            name: Watchlist name.
            epics: Market epics to be associated with this new watchlist.
                Defaults to ``None``.
        """
        return v1.CreateResult.model_validate(
            self._requester.post(
                self.url,
                json={
                    "name": name,
                    **({"epics": list(epics)} if epics is not None else {}),
                },
            )
        )

    def delete(
        self, watchlist_id: str, epic: str | None = None, /
    ) -> v1.DeleteStatus:
        """Deletes the given watchlist, or removes a market from it.

        ``DELETE /watchlists/{watchlist_id}`` or
        ``DELETE /watchlists/{watchlist_id}/{epic}``

        Args:
            watchlist_id: The watchlist identifier.
            epic: Instrument epic identifier of the market to remove. If
                ``None``, the whole watchlist is deleted instead. Defaults to
                ``None``.
        """
        url: t.Final = (
            f"{self.url}/{watchlist_id}/{epic}"
            if epic is not None
            else f"{self.url}/{watchlist_id}"
        )
        return self._requester.delete(url, json={})["status"]  # type: ignore[return-value]

    def get(self, watchlist_id: str, /) -> tuple[MarketOverview, ...]:
        """Returns the markets in the given watchlist.

        ``GET /watchlists/{watchlist_id}``

        Args:
            watchlist_id: The watchlist identifier.
        """
        return tuple(
            MarketOverview.model_validate(market)
            for market in (  # type: ignore[attr-defined]
                self._requester.get(f"{self.url}/{watchlist_id}")
            )["markets"]
        )

    def list(self) -> tuple[v1.Watchlist, ...]:
        """Returns all watchlists belonging to the active account.

        ``GET /watchlists``
        """
        return tuple(
            v1.Watchlist.model_validate(watchlist)
            for watchlist in (  # type: ignore[attr-defined]
                self._requester.get(self.url)
            )["watchlists"]
        )

    def update(self, watchlist_id: str, /, *, epic: str) -> v1.UpdateStatus:
        """Adds a market to the given watchlist.

        ``PUT /watchlists/{watchlist_id}``

        Args:
            watchlist_id: The watchlist identifier.
            epic: Instrument epic identifier.
        """
        return self._requester.put(  # type: ignore[return-value]
            f"{self.url}/{watchlist_id}", json={"epic": epic}
        )["status"]
