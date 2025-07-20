from __future__ import annotations

import typing_extensions as t

from _ig_trading.accounts import v1
from _ig_trading.resource import AsyncResource, Resource

if t.TYPE_CHECKING:
    from _ig_trading.api_requester import APIRequester, AsyncAPIRequester


class AsyncAccountsResource(AsyncResource):
    """Accounts resource: ``/accounts``."""

    __slots__ = ("preferences",)

    url: t.Final = "accounts"

    def __init__(self, requester: AsyncAPIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.preferences: t.Final = AsyncAccountsPreferencesResource(requester)

    async def list(self) -> tuple[v1.Account, ...]:
        """Returns the user's session details and optionally tokens.

        ``GET /accounts``
        """
        return tuple(
            v1.Account.model_validate(account)
            for account in (await self._requester.get(self.url))["accounts"]  # type: ignore[attr-defined]
        )


class AsyncAccountsPreferencesResource(AsyncResource):
    """Accounts resource: ``/accounts/preferences``."""

    url: t.Final = f"{AsyncAccountsResource.url}/preferences"

    async def get(self) -> v1.Preferences:
        """Returns the account preferences.

        ``GET /accounts/preferences``
        """
        return v1.Preferences.model_validate(
            await self._requester.get(self.url)
        )

    async def update(
        self, *, trailing_stops_enabled: bool
    ) -> v1.UpdatePreferencesStatus:
        """Updates the account preferences.

        ``PUT /accounts/preferences``

        Args:
            trailing_stops_enabled: New trailing stop preference.
        """
        return (  # type: ignore[return-value]
            await self._requester.put(
                self.url,
                json={"trailingStopsEnabled": trailing_stops_enabled},
            )
        )["status"]


class AccountsResource(Resource):
    """Accounts resource: ``/accounts``."""

    __slots__ = ("preferences",)

    url: t.Final = "accounts"

    def __init__(self, requester: APIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.preferences: t.Final = AccountsPreferencesResource(requester)

    def list(self) -> tuple[v1.Account, ...]:
        """Returns the user's session details and optionally tokens.

        ``GET /accounts``
        """
        return tuple(
            v1.Account.model_validate(account)
            for account in self._requester.get(self.url)["accounts"]  # type: ignore[attr-defined]
        )


class AccountsPreferencesResource(Resource):
    """Accounts resource: ``/accounts/preferences``."""

    url: t.Final = f"{AccountsResource.url}/preferences"

    def get(self) -> v1.Preferences:
        """Returns the account preferences.

        ``GET /accounts/preferences``
        """
        return v1.Preferences.model_validate(self._requester.get(self.url))

    def update(
        self, *, trailing_stops_enabled: bool
    ) -> v1.UpdatePreferencesStatus:
        """Updates the account preferences.

        ``PUT /accounts/preferences``

        Args:
            trailing_stops_enabled: New trailing stop preference.
        """
        return self._requester.put(  # type: ignore[return-value]
            self.url,
            json={"trailingStopsEnabled": trailing_stops_enabled},
        )["status"]
