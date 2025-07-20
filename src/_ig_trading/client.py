from __future__ import annotations

import asyncio as aio
import contextlib
import datetime as dt
import threading

import typing_extensions as t

from _ig_trading import env
from _ig_trading.accounts.resource import (
    AccountsResource,
    AsyncAccountsResource,
)
from _ig_trading.api_error import OAuthTokenInvalidError
from _ig_trading.api_requester import (
    APIRequester,
    AsyncAPIRequester,
    AsyncSession,
    Session,
)
from _ig_trading.application.resource import (
    ApplicationResource,
    AsyncApplicationResource,
)
from _ig_trading.categories.resource import (
    AsyncCategoriesResource,
    CategoriesResource,
)
from _ig_trading.client_sentiment.resource import (
    AsyncClientSentimentResource,
    ClientSentimentResource,
)
from _ig_trading.confirms.resource import (
    AsyncConfirmsResource,
    ConfirmsResource,
)
from _ig_trading.history.resource import AsyncHistoryResource, HistoryResource
from _ig_trading.markets.resource import AsyncMarketsResource, MarketsResource
from _ig_trading.positions.resource import (
    AsyncPositionsResource,
    PositionsResource,
)
from _ig_trading.prices.resource import AsyncPricesResource, PricesResource
from _ig_trading.session.resource import AsyncSessionResource, SessionResource
from _ig_trading.watchlists.resource import (
    AsyncWatchlistsResource,
    WatchlistsResource,
)
from _ig_trading.working_orders.resource import (
    AsyncWorkingOrdersResource,
    WorkingOrdersResource,
)

if t.TYPE_CHECKING:
    from _ig_trading.session.v3 import OAuthToken


class AsyncClient(contextlib.AbstractAsyncContextManager):
    """API client.

    Args:
        api_key: The API key. Defaults to the environmental variable
            ``IG_API_KEY``.
        http_session: The HTTP session. Defaults to :obj:`.ClientSession`.
        password: The password. Defaults to the environmental variable
            ``IG_PASSWORD``.
        refresh_threshold: The time window, in seconds, before the OAuth
            token's expiry during which the token should be refreshed. This
            ensures that the token is refreshed proactively, avoiding potential
            authorization issues due to token expiry. Defaults to 5 seconds.
        url: The REST API server base URL. Defaults to
            ``https://demo-api.ig.com/gateway/deal``.
        username: The username. Defaults to the environmental variable
            ``IG_IDENTIFIER``.
    """

    __slots__ = (
        "__oauth_token",
        "_http_session",
        "_prev_refresh_time",
        "_refresh_token_task",
        "_should_close_session",
        "accounts",
        "api_key",
        "application",
        "categories",
        "client_sentiment",
        "confirms",
        "history",
        "markets",
        "password",
        "positions",
        "prices",
        "refresh_threshold",
        "requester",
        "session",
        "url",
        "username",
        "watchlists",
        "working_orders",
    )

    default_refresh_threshold: t.Final = dt.timedelta(seconds=5)

    def __init__(
        self,
        *,
        api_key: str | None = None,
        http_session: AsyncSession | None = None,
        password: str | None = None,
        refresh_threshold: float | dt.timedelta = default_refresh_threshold,
        url: str = AsyncAPIRequester.default_url,
        username: str | None = None,
    ) -> None:
        self._http_session: t.Final = http_session or AsyncSession()
        self._should_close_session: t.Final = http_session is None
        self.api_key: t.Final = api_key or env.get_api_key()
        self.requester: t.Final = AsyncAPIRequester(
            http_session=self._http_session, key=self.api_key, url=url
        )
        self.accounts: t.Final = AsyncAccountsResource(self.requester)
        self.application: t.Final = AsyncApplicationResource(self.requester)
        self.categories: t.Final = AsyncCategoriesResource(self.requester)
        self.client_sentiment: t.Final = AsyncClientSentimentResource(
            self.requester
        )
        self.confirms: t.Final = AsyncConfirmsResource(self.requester)
        self.history: t.Final = AsyncHistoryResource(self.requester)
        self.markets: t.Final = AsyncMarketsResource(self.requester)
        self.password: t.Final = password or env.get_password()
        self.positions: t.Final = AsyncPositionsResource(self.requester)
        self.prices: t.Final = AsyncPricesResource(self.requester)
        self.refresh_threshold: t.Final = (
            refresh_threshold
            if isinstance(refresh_threshold, dt.timedelta)
            else dt.timedelta(seconds=refresh_threshold)
        )
        self.session: t.Final = AsyncSessionResource(self.requester)
        self.url: t.Final = url
        self.username: t.Final = username or env.get_identifier()
        self.watchlists: t.Final = AsyncWatchlistsResource(self.requester)
        self.working_orders: t.Final = AsyncWorkingOrdersResource(
            self.requester
        )

        self.__oauth_token: OAuthToken | None = None
        self._prev_refresh_time = dt.datetime.now(dt.timezone.utc)
        self._refresh_token_task: aio.Task | None = None

    async def __aenter__(self) -> t.Self:
        await self.login()
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    @property
    def oauth_token(self) -> OAuthToken | None:
        """The current OAuth token, if logged in."""
        return self._oauth_token

    @property
    def prev_refresh_time(self) -> dt.datetime:
        """When the OAuth token was last refreshed (or first obtained)."""
        return self._prev_refresh_time

    @property
    def _oauth_token(self) -> OAuthToken | None:
        return self.__oauth_token

    @_oauth_token.setter
    def _oauth_token(self, oauth_token: OAuthToken) -> None:
        self._prev_refresh_time = dt.datetime.now(dt.timezone.utc)
        self.__oauth_token = oauth_token
        self.requester.bearer_token = oauth_token.access_token

    async def close(self) -> None:
        """Logout and, if needed, close the HTTP session."""
        await self.logout()
        if self._should_close_session:
            await self._http_session.close()

    async def login(self) -> None:
        """Login to account."""
        response: t.Final = await self.session.create(
            identifier=self.username, password=self.password
        )
        self.requester.account_id = response.account_id
        self._oauth_token = response.oauth_token
        self._stop_refresh_token_task()
        self._refresh_token_task = aio.create_task(self._auto_refresh_token())

    async def logout(self) -> None:
        """Logout and remove the account id and bearer token."""
        with contextlib.suppress(OAuthTokenInvalidError):
            await self.session.delete()

        self._stop_refresh_token_task()
        self.requester.account_id = None
        self.requester.bearer_token = None

    async def refresh_token(self) -> None:
        """Refreshes the OAuth token."""
        if self._oauth_token:
            self._oauth_token = await self.session.refresh_token.create(
                self._oauth_token.refresh_token
            )

    async def _auto_refresh_token(self) -> None:
        while self._oauth_token:
            await aio.sleep(
                (
                    self._prev_refresh_time
                    + self._oauth_token.expires_in
                    - self.refresh_threshold
                    - dt.datetime.now(dt.timezone.utc)
                ).total_seconds()
            )
            await self.refresh_token()

    def _stop_refresh_token_task(self) -> None:
        if self._refresh_token_task:
            self._refresh_token_task.cancel()
            self._refresh_token_task = None


class Client(contextlib.AbstractContextManager):
    """API client.

    Args:
        api_key: The API key. Defaults to the environmental variable
            ``IG_API_KEY``.
        http_session: The HTTP session. Defaults to :obj:`.Session`.
        password: The password. Defaults to the environmental variable
            ``IG_PASSWORD``.
        refresh_threshold: The time window, in seconds, before the OAuth
            token's expiry during which the token should be refreshed. This
            ensures that the token is refreshed proactively, avoiding potential
            authorization issues due to token expiry. Defaults to 5 seconds.
        url: The REST API server base URL. Defaults to
            ``https://demo-api.ig.com/gateway/deal``.
        username: The username. Defaults to the environmental variable
            ``IG_IDENTIFIER``.
    """

    __slots__ = (
        "__oauth_token",
        "_http_session",
        "_prev_refresh_time",
        "_refresh_token_stop_event",
        "_refresh_token_thread",
        "_should_close_session",
        "accounts",
        "api_key",
        "application",
        "categories",
        "client_sentiment",
        "confirms",
        "history",
        "markets",
        "password",
        "positions",
        "prices",
        "refresh_threshold",
        "requester",
        "session",
        "url",
        "username",
        "watchlists",
        "working_orders",
    )

    default_refresh_threshold: t.Final = dt.timedelta(seconds=5)

    def __init__(
        self,
        *,
        api_key: str | None = None,
        http_session: Session | None = None,
        password: str | None = None,
        refresh_threshold: float | dt.timedelta = default_refresh_threshold,
        url: str = APIRequester.default_url,
        username: str | None = None,
    ) -> None:
        self._http_session: t.Final = http_session or Session()
        self._refresh_token_stop_event: t.Final = threading.Event()
        self._should_close_session: t.Final = http_session is None
        self.api_key: t.Final = api_key or env.get_api_key()
        self.requester: t.Final = APIRequester(
            http_session=self._http_session, key=self.api_key, url=url
        )
        self.accounts: t.Final = AccountsResource(self.requester)
        self.application: t.Final = ApplicationResource(self.requester)
        self.categories: t.Final = CategoriesResource(self.requester)
        self.client_sentiment: t.Final = ClientSentimentResource(
            self.requester
        )
        self.confirms: t.Final = ConfirmsResource(self.requester)
        self.history: t.Final = HistoryResource(self.requester)
        self.markets: t.Final = MarketsResource(self.requester)
        self.password: t.Final = password or env.get_password()
        self.positions: t.Final = PositionsResource(self.requester)
        self.prices: t.Final = PricesResource(self.requester)
        self.refresh_threshold: t.Final = (
            refresh_threshold
            if isinstance(refresh_threshold, dt.timedelta)
            else dt.timedelta(seconds=refresh_threshold)
        )
        self.session: t.Final = SessionResource(self.requester)
        self.url: t.Final = url
        self.username: t.Final = username or env.get_identifier()
        self.watchlists: t.Final = WatchlistsResource(self.requester)
        self.working_orders: t.Final = WorkingOrdersResource(self.requester)

        self.__oauth_token: OAuthToken | None = None
        self._prev_refresh_time = dt.datetime.now(dt.timezone.utc)
        self._refresh_token_thread: threading.Thread | None = None

    def __enter__(self) -> t.Self:
        self.login()
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    @property
    def oauth_token(self) -> OAuthToken | None:
        """The current OAuth token, if logged in."""
        return self._oauth_token

    @property
    def prev_refresh_time(self) -> dt.datetime:
        """When the OAuth token was last refreshed (or first obtained)."""
        return self._prev_refresh_time

    @property
    def _oauth_token(self) -> OAuthToken | None:
        return self.__oauth_token

    @_oauth_token.setter
    def _oauth_token(self, oauth_token: OAuthToken) -> None:
        self._prev_refresh_time = dt.datetime.now(dt.timezone.utc)
        self.__oauth_token = oauth_token
        self.requester.bearer_token = oauth_token.access_token

    def close(self) -> None:
        """Logout and, if needed, close the HTTP session."""
        self.logout()
        if self._should_close_session:
            self._http_session.close()

    def login(self) -> None:
        """Login to account."""
        response: t.Final = self.session.create(
            identifier=self.username, password=self.password
        )
        self.requester.account_id = response.account_id
        self._oauth_token = response.oauth_token
        self._stop_refresh_token_thread()
        self._refresh_token_thread = threading.Thread(
            target=self._auto_refresh_token, daemon=True
        )
        self._refresh_token_thread.start()

    def logout(self) -> None:
        """Logout and remove the account id and bearer token."""
        with contextlib.suppress(OAuthTokenInvalidError):
            self.session.delete()

        self._stop_refresh_token_thread()
        self.requester.account_id = None
        self.requester.bearer_token = None

    def refresh_token(self) -> None:
        """Refreshes the OAuth token."""
        if self._oauth_token:
            self._oauth_token = self.session.refresh_token.create(
                self._oauth_token.refresh_token
            )

    def _auto_refresh_token(self) -> None:
        while self._oauth_token:
            if self._refresh_token_stop_event.wait(
                timeout=max(
                    (
                        self._prev_refresh_time
                        + self._oauth_token.expires_in
                        - self.refresh_threshold
                        - dt.datetime.now(dt.timezone.utc)
                    ).total_seconds(),
                    0,
                )
            ):
                return

            self.refresh_token()

    def _stop_refresh_token_thread(self) -> None:
        if self._refresh_token_thread is not None:
            self._refresh_token_stop_event.set()
            self._refresh_token_thread.join()
            self._refresh_token_thread = None
            self._refresh_token_stop_event.clear()
