from __future__ import annotations

import typing_extensions as t

from _ig_trading.prices import v1, v3
from _ig_trading.resource import AsyncResource, Resource

if t.TYPE_CHECKING:
    import datetime as dt


class AsyncPricesResource(AsyncResource):
    """Prices resource: ``/prices``."""

    __slots__ = ()

    url: t.Final = "prices"

    @t.overload
    async def get(
        self,
        epic: str,
        /,
        *,
        end_date: str | dt.datetime | None = ...,
        num_points: int = ...,
        resolution: v1.PriceResolution = ...,
        start_date: str | dt.datetime | None = ...,
        version: t.Literal[1, 2],
    ) -> v1.Prices: ...

    @t.overload
    async def get(
        self,
        epic: str,
        /,
        *,
        end_date: str | dt.datetime | None = ...,
        num_points: int = ...,
        page_num: int = ...,
        page_size: int = ...,
        resolution: v1.PriceResolution = ...,
        start_date: str | dt.datetime | None = ...,
        version: t.Literal[3] = ...,
    ) -> v3.Prices: ...

    async def get(
        self,
        epic: str,
        /,
        *,
        end_date: str | dt.datetime | None = None,
        num_points: int = 10,
        page_num: int = 1,
        page_size: int = 20,
        resolution: v1.PriceResolution = "MINUTE",
        start_date: str | dt.datetime | None = None,
        version: t.Literal[1, 2, 3] = 3,
    ) -> v1.Prices | v3.Prices:
        """Returns the user's session details and optionally tokens.

        v1:
        ``/prices/{epic}/{resolution}?startdate={startdate}&enddate={enddate}``

        v1/v2: ``GET /prices/{epic}/{resolution}/{numPoints}``

        v2: ``GET /prices/{epic}/{resolution}/{startDate}/{endDate}``

        v3: ``GET /prices/{epic}``

        Args:
            epic: Instrument epic.
            end_date: Date range end date time, where v1 format is
                ``yyyy:MM:dd-HH:mm:ss``, v2 format is ``yyyy-MM-dd HH:mm:ss``
                and v3 format is ``yyyy-MM-dd'T'HH:mm:ss``). Defaults to
                ``None``.
            num_points: Limits the number of price points (not applicable
                if a date range has been specified). Defaults to ``10``.
            page_num: Page size (``0`` to disable paging). Defaults to ``1``.
            page_size: Page size (``0`` to disable paging). Defaults to ``20``.
            resolution: Price resolution Defines the resolution of requested
                prices. Defaults to ``MINUTE``.
            start_date: Date range start date time, where v1 format is
                ``yyyy:MM:dd-HH:mm:ss``, v2 format is ``yyyy-MM-dd HH:mm:ss``
                and v3 format is ``yyyy-MM-dd'T'HH:mm:ss``). Defaults to
                ``None``.
            version: The API version. Defaults to ``3``.
        """
        if version == 1 and start_date and end_date:
            v1_datetime_format: t.Final = "%Y:%m:%d-%H:%M:%S"
            start_date = (
                start_date
                if isinstance(start_date, str)
                else start_date.strftime(v1_datetime_format)
            )
            end_date = (
                end_date
                if isinstance(end_date, str)
                else end_date.strftime(v1_datetime_format)
            )
            return v1.Prices.model_validate(
                await self._requester.get(
                    (
                        f"{self.url}/{epic}/{resolution}?"
                        f"startdate={start_date}&enddate={end_date}"
                    ),
                    version=version,
                )
            )

        if version == 2 and start_date and end_date:  # noqa: PLR2004
            v2_datetime_format: t.Final = "%Y-%m-%d %H:%M:%S"
            start_date = (
                start_date
                if isinstance(start_date, str)
                else start_date.strftime(v2_datetime_format)
            )
            end_date = (
                end_date
                if isinstance(end_date, str)
                else end_date.strftime(v2_datetime_format)
            )
            return v1.Prices.model_validate(
                await self._requester.get(
                    f"{self.url}/{epic}/{resolution}/{start_date}/{end_date}",
                    version=version,
                )
            )

        legacy_api_version: t.Final = 3
        if version < legacy_api_version:
            return v1.Prices.model_validate(
                await self._requester.get(
                    (f"{self.url}/{epic}/{resolution}/{num_points}"),
                    version=version,
                )
            )

        v3_datetime_format: t.Final = "%Y-%m-%dT%H:%M:%S"
        start_date = (
            start_date
            if isinstance(start_date, str) or start_date is None
            else start_date.strftime(v3_datetime_format)
        )
        end_date = (
            end_date
            if isinstance(end_date, str) or end_date is None
            else end_date.strftime(v3_datetime_format)
        )
        return v3.Prices.model_validate(
            await self._requester.get(
                f"{self.url}/{epic}",
                params={
                    "max": num_points,
                    "pageNumber": page_num,
                    "pageSize": page_size,
                    "resolution": resolution,
                    **({"from": start_date} if start_date else {}),
                    **({"to": end_date} if end_date else {}),
                },
                version=3,
            )
        )

    @staticmethod
    def get_url(epic: str = "", /) -> str:
        return "prices" + (f"/{epic}" if epic else "")


class PricesResource(Resource):
    """Prices resource: ``/prices``."""

    __slots__ = ()

    url: t.Final = "prices"

    @t.overload
    def get(
        self,
        epic: str,
        /,
        *,
        end_date: str | dt.datetime | None = ...,
        num_points: int = ...,
        resolution: v1.PriceResolution = ...,
        start_date: str | dt.datetime | None = ...,
        version: t.Literal[1, 2],
    ) -> v1.Prices: ...

    @t.overload
    def get(
        self,
        epic: str,
        /,
        *,
        end_date: str | dt.datetime | None = ...,
        num_points: int = ...,
        page_num: int = ...,
        page_size: int = ...,
        resolution: v1.PriceResolution = ...,
        start_date: str | dt.datetime | None = ...,
        version: t.Literal[3] = ...,
    ) -> v3.Prices: ...

    def get(
        self,
        epic: str,
        /,
        *,
        end_date: str | dt.datetime | None = None,
        num_points: int = 10,
        page_num: int = 1,
        page_size: int = 20,
        resolution: v1.PriceResolution = "MINUTE",
        start_date: str | dt.datetime | None = None,
        version: t.Literal[1, 2, 3] = 3,
    ) -> v1.Prices | v3.Prices:
        """Returns the user's session details and optionally tokens.

        v1:
        ``/prices/{epic}/{resolution}?startdate={startdate}&enddate={enddate}``

        v1/v2: ``GET /prices/{epic}/{resolution}/{numPoints}``

        v2: ``GET /prices/{epic}/{resolution}/{startDate}/{endDate}``

        v3: ``GET /prices/{epic}``

        Args:
            epic: Instrument epic.
            end_date: Date range end date time, where v1 format is
                ``yyyy:MM:dd-HH:mm:ss``, v2 format is ``yyyy-MM-dd HH:mm:ss``
                and v3 format is ``yyyy-MM-dd'T'HH:mm:ss``). Defaults to
                ``None``.
            num_points: Limits the number of price points (not applicable
                if a date range has been specified). Defaults to ``10``.
            page_num: Page size (``0`` to disable paging). Defaults to ``1``.
            page_size: Page size (``0`` to disable paging). Defaults to ``20``.
            resolution: Price resolution Defines the resolution of requested
                prices. Defaults to ``MINUTE``.
            start_date: Date range start date time, where v1 format is
                ``yyyy:MM:dd-HH:mm:ss``, v2 format is ``yyyy-MM-dd HH:mm:ss``
                and v3 format is ``yyyy-MM-dd'T'HH:mm:ss``). Defaults to
                ``None``.
            version: The API version. Defaults to ``3``.
        """
        if version == 1 and start_date and end_date:
            v1_datetime_format: t.Final = "%Y:%m:%d-%H:%M:%S"
            start_date = (
                start_date
                if isinstance(start_date, str)
                else start_date.strftime(v1_datetime_format)
            )
            end_date = (
                end_date
                if isinstance(end_date, str)
                else end_date.strftime(v1_datetime_format)
            )
            return v1.Prices.model_validate(
                self._requester.get(
                    (
                        f"{self.url}/{epic}/{resolution}?"
                        f"startdate={start_date}&enddate={end_date}"
                    ),
                    version=version,
                )
            )

        if version == 2 and start_date and end_date:  # noqa: PLR2004
            v2_datetime_format: t.Final = "%Y-%m-%d %H:%M:%S"
            start_date = (
                start_date
                if isinstance(start_date, str)
                else start_date.strftime(v2_datetime_format)
            )
            end_date = (
                end_date
                if isinstance(end_date, str)
                else end_date.strftime(v2_datetime_format)
            )
            return v1.Prices.model_validate(
                self._requester.get(
                    f"{self.url}/{epic}/{resolution}/{start_date}/{end_date}",
                    version=version,
                )
            )

        legacy_api_version: t.Final = 3
        if version < legacy_api_version:
            return v1.Prices.model_validate(
                self._requester.get(
                    (f"{self.url}/{epic}/{resolution}/{num_points}"),
                    version=version,
                )
            )

        v3_datetime_format: t.Final = "%Y-%m-%dT%H:%M:%S"
        start_date = (
            start_date
            if isinstance(start_date, str) or start_date is None
            else start_date.strftime(v3_datetime_format)
        )
        end_date = (
            end_date
            if isinstance(end_date, str) or end_date is None
            else end_date.strftime(v3_datetime_format)
        )
        return v3.Prices.model_validate(
            self._requester.get(
                f"{self.url}/{epic}",
                params={
                    "max": num_points,
                    "pageNumber": page_num,
                    "pageSize": page_size,
                    "resolution": resolution,
                    **({"from": start_date} if start_date else {}),
                    **({"to": end_date} if end_date else {}),
                },
                version=3,
            )
        )

    @staticmethod
    def get_url(epic: str = "", /) -> str:
        return "prices" + (f"/{epic}" if epic else "")
