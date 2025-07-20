from __future__ import annotations

import typing_extensions as t

from _ig_trading.application import v1
from _ig_trading.resource import AsyncResource, Resource

if t.TYPE_CHECKING:
    from _ig_trading.api_requester import APIRequester, AsyncAPIRequester


class AsyncApplicationResource(AsyncResource):
    """Application resource: ``/operations/application``."""

    __slots__ = ("disable",)

    url: t.Final = "operations/application"

    def __init__(self, requester: AsyncAPIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.disable: t.Final = AsyncApplicationDisableResource(requester)

    async def list(self) -> tuple[v1.Application, ...]:
        """Returns a list of client-owned applications.

        ``GET /operations/application``
        """
        return tuple(
            v1.Application.model_validate(application)
            for application in await self._requester.get(self.url)
        )

    async def update(
        self,
        *,
        allowance_account_overall: float,
        allowance_account_trading: float,
        api_key: str,
        status: v1.Status | None = None,
    ) -> tuple[v1.Application, ...]:
        """Updates the details of the given application.

        ``PUT /operations/application``

        Args:
            allowance_account_overall: Per account request per minute
                allowance.
            allowance_account_trading: Per account trading request per minute
                allowance.
            api_key: API key.
            status: Application status. Defaults to ``None``.
        """
        return tuple(
            v1.Application.model_validate(application)
            for application in (  # type: ignore[attr-defined]
                await self._requester.put(
                    self.url,
                    json={
                        "allowanceAccountOverall": allowance_account_overall,
                        "allowanceAccountTrading": allowance_account_trading,
                        "apiKey": api_key,
                        **({"status": status} if status is not None else {}),
                    },
                )
            )
        )


class AsyncApplicationDisableResource(AsyncResource):
    """Application resource: ``/operations/application/disable``."""

    __slots__ = ()

    url: t.Final = f"{AsyncApplicationResource.url}/disable"

    async def update(self) -> tuple[v1.Application, ...]:
        """Disables the current application key.

        ``PUT /operations/application/disable``
        """
        return tuple(
            v1.Application.model_validate(application)
            for application in (  # type: ignore[attr-defined]
                await self._requester.put(self.url, json={})
            )
        )


class ApplicationResource(Resource):
    """Application resource: ``/operations/application``."""

    __slots__ = ("disable",)

    url: t.Final = "operations/application"

    def __init__(self, requester: APIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.disable: t.Final = ApplicationDisableResource(requester)

    def list(self) -> tuple[v1.Application, ...]:
        """Returns a list of client-owned applications.

        ``GET /operations/application``
        """
        return tuple(
            v1.Application.model_validate(application)
            for application in self._requester.get(self.url)
        )

    def update(
        self,
        *,
        allowance_account_overall: float,
        allowance_account_trading: float,
        api_key: str,
        status: v1.Status | None = None,
    ) -> tuple[v1.Application, ...]:
        """Updates the details of the given application.

        ``PUT /operations/application``

        Args:
            allowance_account_overall: Per account request per minute
                allowance.
            allowance_account_trading: Per account trading request per minute
                allowance.
            api_key: API key.
            status: Application status. Defaults to ``None``.
        """
        return tuple(
            v1.Application.model_validate(application)
            for application in (  # type: ignore[attr-defined]
                self._requester.put(
                    self.url,
                    json={
                        "allowanceAccountOverall": allowance_account_overall,
                        "allowanceAccountTrading": allowance_account_trading,
                        "apiKey": api_key,
                        **({"status": status} if status is not None else {}),
                    },
                )
            )
        )


class ApplicationDisableResource(Resource):
    """Application resource: ``/operations/application/disable``."""

    __slots__ = ()

    url: t.Final = f"{ApplicationResource.url}/disable"

    def update(self) -> tuple[v1.Application, ...]:
        """Disables the current application key.

        ``PUT /operations/application/disable``
        """
        return tuple(
            v1.Application.model_validate(application)
            for application in (  # type: ignore[attr-defined]
                self._requester.put(self.url, json={})
            )
        )
