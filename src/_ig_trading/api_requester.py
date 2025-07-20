from __future__ import annotations

import contextlib

import aiohttp
import requests
import typing_extensions as t

from _ig_trading import env
from _ig_trading.api_error import APIError, UnknownAPIError

if t.TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    # Mirrors the value type aiohttp's `ClientSession.request` accepts for its
    # `params` argument (`aiohttp.typedefs.Query`, restricted to the mapping
    # form), so any value it supports can be passed through here too.
    _AsyncQueryValue = (
        str | t.SupportsInt | float | Sequence[str | t.SupportsInt | float]
    )
    # Mirrors the value type `requests.Session.request` accepts for its
    # `params` argument when given as a mapping.
    _QueryValue = str | int | float | Sequence[str | int | float]

AsyncSession = aiohttp.ClientSession
Session = requests.Session
_Version = t.Literal[1, 2, 3, 4]


class AsyncAPIRequester:
    """REST API requester.

    Args:
        account_id: The v3 API account ID from logging in. Defaults to
            ``None``.
        bearer_token: The v3 API authentication bearer token from logging in.
            Defaults to ``None``.
        cst: A v1 and v2 API access token identifying the client. Defaults to
            ``None``.
        http_session: The HTTP session. If ``None``, a new HTTP session will
            be opened for every request. Defaults to ``None``.
        key: The API key. Defaults to the environmental variable
            ``IG_API_KEY``.
        url: The REST API server base URL. Defaults to
            ``https://demo-api.ig.com/gateway/deal``.
        x_security_token: A v1 and v2 API account token identifying the
            client's current account. Defaults to ``None``.

    .. |json| replace:: A JSON dictionary to be sent as the body of the
        request. Defaults to ``None``.
    .. |url| replace:: The REST API endpoint.
    .. |version| replace:: The API version to be sent as the ``VERSION``
        header. Defaults to ``None``.
    """

    __slots__ = (
        "_session",
        "account_id",
        "bearer_token",
        "cst",
        "key",
        "url",
        "x_security_token",
    )

    default_url: t.Final = "https://demo-api.ig.com/gateway/deal"

    def __init__(
        self,
        account_id: str | None = None,
        bearer_token: str | None = None,
        cst: str | None = None,
        http_session: AsyncSession | None = None,
        key: str | None = None,
        url: str = default_url,
        x_security_token: str | None = None,
    ) -> None:
        self._session: t.Final = http_session
        self.key: t.Final = key or env.get_api_key()
        self.url: t.Final = url
        self.account_id = account_id
        self.bearer_token = bearer_token
        self.cst = cst
        self.x_security_token = x_security_token

    @property
    def headers(self) -> dict[str, str]:
        """The authentication headers to send with every request."""
        headers: t.Final = {"X-IG-API-KEY": self.key}
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        if self.cst:
            headers["CST"] = self.cst
        if self.account_id:
            headers["IG-ACCOUNT-ID"] = self.account_id
        if self.x_security_token:
            headers["X-SECURITY-TOKEN"] = self.x_security_token
        return headers

    async def delete(
        self,
        url: str,
        *,
        json: Mapping[str, object] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        """Send a delete request.

        Args:
            url: |url|
            json: |json|
            version: |version|
        """
        # IG trading API seems to require POST with _method header instead. See
        # https://github.com/ig-python/trading-ig/blob/master/trading_ig/rest.py#L143
        return await self._request(
            "post",
            url,
            json=json,
            headers={"_method": "DELETE"},
            version=version,
        )

    async def get(
        self,
        url: str,
        /,
        *,
        params: Mapping[str, _AsyncQueryValue] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        """Send a get request and returns a JSON dictionary.

        Args:
            url: |url|
            params: Get parameters. Defaults to ``None``.
            version: |version|
        """
        return await self._request("get", url, params=params, version=version)

    async def post(
        self,
        url: str,
        /,
        *,
        json: Mapping[str, object] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        """Send a post request with some data and returns a JSON dictionary.

        Args:
            url: |url|
            json: |json|
            version: |version|
        """
        return await self._request("post", url, version=version, json=json)

    async def put(
        self,
        url: str,
        /,
        *,
        json: dict[str, object] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        """Send a put request with some data and returns a JSON dictionary.

        Args:
            url: |url|
            json: |json|
            version: |version|
        """
        return await self._request("put", url, version=version, json=json)

    async def _request(
        self,
        method: t.Literal["delete", "get", "post", "put"],
        url: str,
        /,
        *,
        headers: Mapping[str, str] | None = None,
        json: Mapping[str, object] | None = None,
        params: Mapping[str, _AsyncQueryValue] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        async with contextlib.AsyncExitStack() as stack:
            session: t.Final = (
                await stack.enter_async_context(AsyncSession())
                if self._session is None
                else self._session
            )
            response: t.Final = await session.request(
                method.upper(),
                f"{self.url}/{url}",
                headers=(
                    self.headers
                    | ({"VERSION": str(version)} if version else {})
                    | dict(headers or {})
                ),
                params=params,
                json=json,
            )

            if response.ok:
                self.cst = response.headers.get("CST")
                self.x_security_token = response.headers.get(
                    "X-SECURITY-TOKEN"
                )
                return await response.json()

            error_code = "_unknown"

            if response.content_type == "application/json":
                error_code = (await response.json())["errorCode"]

                if api_error := APIError.from_error_code(
                    error_code, status=response.status
                ):
                    raise api_error

            raise UnknownAPIError(
                description=await response.text(),
                error_code="_unknown",
                status=response.status,
            )


class APIRequester:
    """REST API requester.

    Args:
        account_id: The v3 API account ID from logging in. Defaults to
            ``None``.
        bearer_token: The v3 API authentication bearer token from logging in.
            Defaults to ``None``.
        cst: A v1 and v2 API access token identifying the client. Defaults to
            ``None``.
        http_session: The HTTP session. If ``None``, a new HTTP session will
            be opened for every request. Defaults to ``None``.
        key: The API key. Defaults to the environmental variable
            ``IG_API_KEY``.
        url: The REST API server base URL. Defaults to
            ``https://demo-api.ig.com/gateway/deal``.
        x_security_token: A v1 and v2 API account token identifying the
            client's current account. Defaults to ``None``.
    """

    __slots__ = (
        "_session",
        "account_id",
        "bearer_token",
        "cst",
        "key",
        "url",
        "x_security_token",
    )

    default_url: t.Final = "https://demo-api.ig.com/gateway/deal"

    def __init__(
        self,
        account_id: str | None = None,
        bearer_token: str | None = None,
        cst: str | None = None,
        http_session: Session | None = None,
        key: str | None = None,
        url: str = default_url,
        x_security_token: str | None = None,
    ) -> None:
        self._session: t.Final = http_session
        self.key: t.Final = key or env.get_api_key()
        self.url: t.Final = url
        self.account_id = account_id
        self.bearer_token = bearer_token
        self.cst = cst
        self.x_security_token = x_security_token

    @property
    def headers(self) -> dict[str, str]:
        """The authentication headers to send with every request."""
        headers: t.Final = {"X-IG-API-KEY": self.key}
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        if self.cst:
            headers["CST"] = self.cst
        if self.account_id:
            headers["IG-ACCOUNT-ID"] = self.account_id
        if self.x_security_token:
            headers["X-SECURITY-TOKEN"] = self.x_security_token
        return headers

    def delete(
        self,
        url: str,
        *,
        json: Mapping[str, object] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        """Send a delete request.

        Args:
            url: |url|
            json: |json|
            version: |version|
        """
        # IG trading API seems to require POST with _method header instead. See
        # https://github.com/ig-python/trading-ig/blob/master/trading_ig/rest.py#L143
        return self._request(
            "post",
            url,
            json=json,
            headers={"_method": "DELETE"},
            version=version,
        )

    def get(
        self,
        url: str,
        /,
        *,
        params: Mapping[str, _QueryValue] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        """Send a get request and returns a JSON dictionary.

        Args:
            url: |url|
            params: Get parameters. Defaults to ``None``.
            version: |version|
        """
        return self._request("get", url, params=params, version=version)

    def post(
        self,
        url: str,
        /,
        *,
        json: Mapping[str, object] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        """Send a post request with some data and returns a JSON dictionary.

        Args:
            url: |url|
            json: |json|
            version: |version|
        """
        return self._request("post", url, version=version, json=json)

    def put(
        self,
        url: str,
        /,
        *,
        json: dict[str, object] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        """Send a put request with some data and returns a JSON dictionary.

        Args:
            url: |url|
            json: |json|
            version: |version|
        """
        return self._request("put", url, version=version, json=json)

    def _request(
        self,
        method: t.Literal["delete", "get", "post", "put"],
        url: str,
        /,
        *,
        headers: Mapping[str, str] | None = None,
        json: Mapping[str, object] | None = None,
        params: Mapping[str, _QueryValue] | None = None,
        version: _Version | None = None,
    ) -> dict[str, object]:
        with contextlib.ExitStack() as stack:
            session: t.Final = (
                stack.enter_context(Session())
                if self._session is None
                else self._session
            )
            response: t.Final = session.request(
                method.upper(),
                f"{self.url}/{url}",
                headers=(
                    self.headers
                    | ({"VERSION": str(version)} if version else {})
                    | dict(headers or {})
                ),
                params=params,
                json=json,
            )

            if response.ok:
                self.cst = response.headers.get("CST")
                self.x_security_token = response.headers.get(
                    "X-SECURITY-TOKEN"
                )
                # Unlike aiohttp's `ClientResponse.json()`, `requests`
                # doesn't tolerate an empty body (e.g. IG's `204 No
                # Content` responses, which still claim a JSON content
                # type), and raises instead.
                if not response.content.strip():
                    return None  # type: ignore[return-value]
                return response.json()

            error_code = "_unknown"
            content_type = response.headers.get("Content-Type", "")

            if content_type.split(";")[0].strip() == "application/json":
                error_code = response.json()["errorCode"]

                if api_error := APIError.from_error_code(
                    error_code, status=response.status_code
                ):
                    raise api_error

            raise UnknownAPIError(
                description=response.text,
                error_code="_unknown",
                status=response.status_code,
            )
