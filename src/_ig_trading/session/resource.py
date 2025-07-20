from __future__ import annotations

import typing_extensions as t

from _ig_trading import env
from _ig_trading.resource import AsyncResource, Resource
from _ig_trading.session import v1, v3

if t.TYPE_CHECKING:
    from _ig_trading.api_requester import APIRequester, AsyncAPIRequester


class AsyncSessionResource(AsyncResource):
    """Session resource: ``/session``.

    Args:
        requester: A REST API requester. Defaults to creating an
            :class:`AsyncAPIRequester` using ``kwargs``.
    """

    __slots__ = ("encryption_key", "refresh_token")

    url: t.Final = "session"

    def __init__(self, requester: AsyncAPIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.encryption_key: t.Final = AsyncSessionEncryptionKeyResource(
            requester
        )
        self.refresh_token: t.Final = AsyncSessionRefreshTokenResource(
            requester
        )

    @t.overload
    async def create(
        self,
        *,
        encrypted_password: bool = False,
        identifier: str | None = None,
        password: str | None = None,
        version: t.Literal[1, 2],
    ) -> v1.AccountSummary: ...

    @t.overload
    async def create(
        self,
        *,
        identifier: str | None = None,
        password: str | None = None,
        version: t.Literal[3] = 3,
    ) -> v3.AccountSummary: ...

    async def create(
        self,
        *,
        encrypted_password: bool = False,
        identifier: str | None = None,
        password: str | None = None,
        version: t.Literal[1, 2, 3] = 3,
    ) -> v1.AccountSummary | v3.AccountSummary:
        """Creates a trading session.

        Obtaining session tokens for subsequent API access. Please note,
        region-specific login restrictions may apply.

        ``POST /session``

        Args:
            encrypted_password: Whether ``password`` is encrypted.
            identifier: The username. Defaults to the environmental variable
                ``IG_IDENTIFIER``.
            password: The password. Defaults to the environmental variable
                ``IG_PASSWORD``.
            version: The API version. Defaults to ``3``.
        """
        legacy_api_version: t.Final = 3
        # A login establishes a brand new session, so it shouldn't carry
        # whatever identity this requester already holds (e.g. from a previous
        # login): IG's API rejects the request outright if a stale CST,
        # security token, account ID or bearer token is attached, even though
        # the credentials being submitted here are otherwise valid. Callers
        # relying on a requester's previous identity for other, concurrent
        # calls (as this project's own integration tests did until this was
        # found) need a separate requester for logging in.
        self._requester.account_id = None
        self._requester.bearer_token = None
        self._requester.cst = None
        self._requester.x_security_token = None
        return (
            v1 if version < legacy_api_version else v3
        ).AccountSummary.model_validate(
            await self._requester.post(
                self.url,
                json={
                    "identifier": identifier or env.get_identifier(),
                    "password": password or env.get_password(),
                    **(
                        {"encryptedPassword": str(encrypted_password).lower()}
                        if version < legacy_api_version
                        else {}
                    ),
                },
                version=version,
            )
        )

    async def delete(self) -> None:
        """Log out of the current session.

        ``DELETE /session``
        """
        await self._requester.delete(self.url)

    async def get(self) -> v1.Session:
        """Returns the user's session details and optionally tokens.

        ``GET /session``
        """
        return v1.Session.model_validate(await self._requester.get(self.url))

    async def update(
        self, account_id: str, /, *, default_account: bool
    ) -> v1.SwitchAccount:
        """Switches active accounts, optionally setting the default account.

        ``PUT /session``

        Args:
            account_id: The identifier of the account being switched to.
            default_account: ``True`` if the specified account is to be set as
                the new default account.
        """
        return v1.SwitchAccount.model_validate(
            await self._requester.put(
                self.url,
                json={
                    "accountId": account_id,
                    "defaultAccount": default_account,
                },
            )
        )


class AsyncSessionEncryptionKeyResource(AsyncResource):
    """Session resource: ``/session/encryptionKey``."""

    url: t.Final = f"{AsyncSessionResource.url}/encryptionKey"

    async def get(self) -> v1.EncryptionKey:
        """Returns the encryption key for sending the user password securely.

        ``Get /session/encryptionKey``
        """
        return v1.EncryptionKey.model_validate(
            await self._requester.get(self.url)
        )


class AsyncSessionRefreshTokenResource(AsyncResource):
    """Session resource: ``/session/refresh-token``."""

    url: t.Final = f"{AsyncSessionResource.url}/refresh-token"

    async def create(self, refresh_token: str, /) -> v1.OAuthToken:
        """Returns new session tokens for subsequent API access.

        ``POST /session/refresh-token``

        Args:
            refresh_token: The original refresh token.
        """
        return v1.OAuthToken.model_validate(
            await self._requester.post(
                self.url, json={"refresh_token": refresh_token}
            )
        )


class SessionResource(Resource):
    """Session resource: ``/session``.

    Args:
        requester: A REST API requester. Defaults to creating an
            :class:`APIRequester` using ``kwargs``.
    """

    __slots__ = ("encryption_key", "refresh_token")

    url: t.Final = "session"

    def __init__(self, requester: APIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.encryption_key: t.Final = SessionEncryptionKeyResource(requester)
        self.refresh_token: t.Final = SessionRefreshTokenResource(requester)

    @t.overload
    def create(
        self,
        *,
        encrypted_password: bool = False,
        identifier: str | None = None,
        password: str | None = None,
        version: t.Literal[1, 2],
    ) -> v1.AccountSummary: ...

    @t.overload
    def create(
        self,
        *,
        identifier: str | None = None,
        password: str | None = None,
        version: t.Literal[3] = 3,
    ) -> v3.AccountSummary: ...

    def create(
        self,
        *,
        encrypted_password: bool = False,
        identifier: str | None = None,
        password: str | None = None,
        version: t.Literal[1, 2, 3] = 3,
    ) -> v1.AccountSummary | v3.AccountSummary:
        """Creates a trading session.

        Obtaining session tokens for subsequent API access. Please note,
        region-specific login restrictions may apply.

        ``POST /session``

        Args:
            encrypted_password: Whether ``password`` is encrypted.
            identifier: The username. Defaults to the environmental variable
                ``IG_IDENTIFIER``.
            password: The password. Defaults to the environmental variable
                ``IG_PASSWORD``.
            version: The API version. Defaults to ``3``.
        """
        legacy_api_version: t.Final = 3
        # See the equivalent comment in `AsyncSessionResource.create`.
        self._requester.account_id = None
        self._requester.bearer_token = None
        self._requester.cst = None
        self._requester.x_security_token = None
        return (
            v1 if version < legacy_api_version else v3
        ).AccountSummary.model_validate(
            self._requester.post(
                self.url,
                json={
                    "identifier": identifier or env.get_identifier(),
                    "password": password or env.get_password(),
                    **(
                        {"encryptedPassword": str(encrypted_password).lower()}
                        if version < legacy_api_version
                        else {}
                    ),
                },
                version=version,
            )
        )

    def delete(self) -> None:
        """Log out of the current session.

        ``DELETE /session``
        """
        self._requester.delete(self.url)

    def get(self) -> v1.Session:
        """Returns the user's session details and optionally tokens.

        ``GET /session``
        """
        return v1.Session.model_validate(self._requester.get(self.url))

    def update(
        self, account_id: str, /, *, default_account: bool
    ) -> v1.SwitchAccount:
        """Switches active accounts, optionally setting the default account.

        ``PUT /session``

        Args:
            account_id: The identifier of the account being switched to.
            default_account: ``True`` if the specified account is to be set as
                the new default account.
        """
        return v1.SwitchAccount.model_validate(
            self._requester.put(
                self.url,
                json={
                    "accountId": account_id,
                    "defaultAccount": default_account,
                },
            )
        )


class SessionEncryptionKeyResource(Resource):
    """Session resource: ``/session/encryptionKey``."""

    url: t.Final = f"{SessionResource.url}/encryptionKey"

    def get(self) -> v1.EncryptionKey:
        """Returns the encryption key for sending the user password securely.

        ``Get /session/encryptionKey``
        """
        return v1.EncryptionKey.model_validate(self._requester.get(self.url))


class SessionRefreshTokenResource(Resource):
    """Session resource: ``/session/refresh-token``."""

    url: t.Final = f"{SessionResource.url}/refresh-token"

    def create(self, refresh_token: str, /) -> v1.OAuthToken:
        """Returns new session tokens for subsequent API access.

        ``POST /session/refresh-token``

        Args:
            refresh_token: The original refresh token.
        """
        return v1.OAuthToken.model_validate(
            self._requester.post(
                self.url, json={"refresh_token": refresh_token}
            )
        )
