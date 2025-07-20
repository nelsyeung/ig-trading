from __future__ import annotations

import typing_extensions as t

from _ig_trading.markets import v1, v4
from _ig_trading.resource import AsyncResource, Resource

if t.TYPE_CHECKING:
    from collections.abc import Iterable


class AsyncMarketsResource(AsyncResource):
    """Markets resource: ``/markets``."""

    __slots__ = ("encryption_key", "refresh_token")

    url: t.Final = "markets"

    @t.overload
    async def get(
        self, epic: str, /, *, version: t.Literal[1, 2, 3]
    ) -> v1.Market: ...

    @t.overload
    async def get(
        self, epic: str, /, *, version: t.Literal[4] = ...
    ) -> v4.Market: ...

    async def get(
        self, epic: str, /, *, version: t.Literal[1, 2, 3, 4] = 4
    ) -> v1.Market | v4.Market:
        """Returns the details of the given market.

        ``GET /markets/{epic}``

        Args:
            epic: The epic of the market to be retrieved.
            version: The API version. Defaults to ``4``.
        """
        legacy_api_version: t.Final = 4
        return (
            v1 if version < legacy_api_version else v4
        ).Market.model_validate(
            await self._requester.get(f"{self.url}/{epic}", version=version)
        )

    @t.overload
    async def list(
        self,
        epics: Iterable[str],
        /,
        *,
        filter: t.Literal["ALL", "SNAPSHOT_ONLY"] = ...,
        version: t.Literal[1, 2] = ...,
    ) -> tuple[v1.Market, ...]: ...

    @t.overload
    async def list(
        self,
        *,
        page_num: int = ...,
        page_size: int = ...,
        search_term: str,
        version: t.Literal[1, 2] = ...,
    ) -> tuple[v1.MarketOverview, ...]: ...

    async def list(
        self,
        epics: Iterable[str] | None = None,
        *,
        filter: t.Literal["ALL", "SNAPSHOT_ONLY"] = "ALL",  # noqa: A002
        page_num: int = 1,
        page_size: int = 50,
        search_term: str | None = None,
        version: t.Literal[1, 2] = 2,
    ) -> tuple[v1.Market, ...] | tuple[v1.MarketOverview, ...]:
        """Returns markets, given epics or a search term.

        ``GET /markets``

        Args:
            epics: The epics of the market to be retrieved, separated by a
                comma. Max number of epics is limited to 50. Must match
                ``^(?>(?:[A-Za-z0-9._]){6,30},?){0,200}$``. Mutually
                exclusive with ``search_term``. Defaults to ``None``.
            filter: If ``ALL``, display all market details. Market details
                includes all instrument data, dealing rules and market snapshot
                values for all epics specified. If ``SNAPSHOT_ONLY``, display
                the market snapshot and minimal instrument data fields. This
                mode is faster because it only sets the epic and instrument
                type in the instrument data and the market data snapshot values
                with all the other fields being unset for each epic specified.
                Only applies when ``epics`` is given.
            page_num: Page number to be fetched. Only applies when
                ``search_term`` is given, on version ``2``. Defaults to ``1``.
            page_size: Page size. Only applies when ``search_term`` is given,
                on version ``2``. Defaults to ``50``.
            search_term: The term to be used in the market search. Mutually
                exclusive with ``epics``. Defaults to ``None``.
            version: The API version. Defaults to ``2``.
        """
        err: t.Final = "Exactly one of 'epics' or 'search_term' must be given"

        if epics is not None:
            if search_term is not None:
                raise ValueError(err)

            return tuple(
                v1.Market.model_validate(market)
                for market in (  # type: ignore[attr-defined]
                    await self._requester.get(
                        self.url,
                        params={"epics": ",".join(epics), "filter": filter},
                        version=version,
                    )
                )["marketDetails"]
            )

        if search_term is None:
            raise ValueError(err)

        paginated_api_version: t.Final = 2
        return v1.Markets.model_validate(
            await self._requester.get(
                self.url,
                params={
                    "searchTerm": search_term,
                    **(
                        {"pageNumber": page_num, "pageSize": page_size}
                        if version == paginated_api_version
                        else {}
                    ),
                },
                version=version,
            )
        ).markets


class MarketsResource(Resource):
    """Markets resource: ``/markets``."""

    __slots__ = ("encryption_key", "refresh_token")

    url: t.Final = "markets"

    @t.overload
    def get(
        self, epic: str, /, *, version: t.Literal[1, 2, 3]
    ) -> v1.Market: ...

    @t.overload
    def get(
        self, epic: str, /, *, version: t.Literal[4] = ...
    ) -> v4.Market: ...

    def get(
        self, epic: str, /, *, version: t.Literal[1, 2, 3, 4] = 4
    ) -> v1.Market | v4.Market:
        """Returns the details of the given market.

        ``GET /markets/{epic}``

        Args:
            epic: The epic of the market to be retrieved.
            version: The API version. Defaults to ``4``.
        """
        legacy_api_version: t.Final = 4
        return (
            v1 if version < legacy_api_version else v4
        ).Market.model_validate(
            self._requester.get(f"{self.url}/{epic}", version=version)
        )

    @t.overload
    def list(
        self,
        epics: Iterable[str],
        /,
        *,
        filter: t.Literal["ALL", "SNAPSHOT_ONLY"] = ...,
        version: t.Literal[1, 2] = ...,
    ) -> tuple[v1.Market, ...]: ...

    @t.overload
    def list(
        self,
        *,
        page_num: int = ...,
        page_size: int = ...,
        search_term: str,
        version: t.Literal[1, 2] = ...,
    ) -> tuple[v1.MarketOverview, ...]: ...

    def list(
        self,
        epics: Iterable[str] | None = None,
        *,
        filter: t.Literal["ALL", "SNAPSHOT_ONLY"] = "ALL",  # noqa: A002
        page_num: int = 1,
        page_size: int = 50,
        search_term: str | None = None,
        version: t.Literal[1, 2] = 2,
    ) -> tuple[v1.Market, ...] | tuple[v1.MarketOverview, ...]:
        """Returns markets, given epics or a search term.

        ``GET /markets``

        Args:
            epics: The epics of the market to be retrieved, separated by a
                comma. Max number of epics is limited to 50. Must match
                ``^(?>(?:[A-Za-z0-9._]){6,30},?){0,200}$``. Mutually
                exclusive with ``search_term``. Defaults to ``None``.
            filter: If ``ALL``, display all market details. Market details
                includes all instrument data, dealing rules and market snapshot
                values for all epics specified. If ``SNAPSHOT_ONLY``, display
                the market snapshot and minimal instrument data fields. This
                mode is faster because it only sets the epic and instrument
                type in the instrument data and the market data snapshot values
                with all the other fields being unset for each epic specified.
                Only applies when ``epics`` is given.
            page_num: Page number to be fetched. Only applies when
                ``search_term`` is given, on version ``2``. Defaults to ``1``.
            page_size: Page size. Only applies when ``search_term`` is given,
                on version ``2``. Defaults to ``50``.
            search_term: The term to be used in the market search. Mutually
                exclusive with ``epics``. Defaults to ``None``.
            version: The API version. Defaults to ``2``.
        """
        err: t.Final = "Exactly one of 'epics' or 'search_term' must be given"

        if epics is not None:
            if search_term is not None:
                raise ValueError(err)

            return tuple(
                v1.Market.model_validate(market)
                for market in (  # type: ignore[attr-defined]
                    self._requester.get(
                        self.url,
                        params={"epics": ",".join(epics), "filter": filter},
                        version=version,
                    )
                )["marketDetails"]
            )

        if search_term is None:
            raise ValueError(err)

        paginated_api_version: t.Final = 2
        return v1.Markets.model_validate(
            self._requester.get(
                self.url,
                params={
                    "searchTerm": search_term,
                    **(
                        {"pageNumber": page_num, "pageSize": page_size}
                        if version == paginated_api_version
                        else {}
                    ),
                },
                version=version,
            )
        ).markets
