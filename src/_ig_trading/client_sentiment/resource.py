from __future__ import annotations

import typing_extensions as t

from _ig_trading.client_sentiment import v1
from _ig_trading.resource import AsyncResource, Resource

if t.TYPE_CHECKING:
    from collections.abc import Iterable

    from _ig_trading.api_requester import APIRequester, AsyncAPIRequester


class AsyncClientSentimentResource(AsyncResource):
    """Client sentiment resource: ``/clientsentiment``."""

    __slots__ = ("related",)

    url: t.Final = "clientsentiment"

    def __init__(self, requester: AsyncAPIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.related: t.Final = AsyncClientSentimentRelatedResource(requester)

    async def get(self, market_id: str, /) -> v1.Sentiment:
        """Returns the client sentiment for the given market.

        ``GET /clientsentiment/{market_id}``

        Args:
            market_id: The market identifier.
        """
        return v1.Sentiment.model_validate(
            await self._requester.get(f"{self.url}/{market_id}")
        )

    async def list(
        self, market_ids: Iterable[str] | None = None, /
    ) -> tuple[v1.Sentiment, ...]:
        """Returns the client sentiment for the given markets.

        ``GET /clientsentiment``

        Args:
            market_ids: The market identifiers to filter by. Defaults to all
                markets.
        """
        return tuple(
            v1.Sentiment.model_validate(sentiment)
            for sentiment in (  # type: ignore[attr-defined]
                await self._requester.get(
                    self.url,
                    params=(
                        {"marketIds": ",".join(market_ids)}
                        if market_ids is not None
                        else None
                    ),
                )
            )["clientSentiments"]
        )


class AsyncClientSentimentRelatedResource(AsyncResource):
    """Client sentiment resource: ``/clientsentiment/related``."""

    __slots__ = ()

    url: t.Final = f"{AsyncClientSentimentResource.url}/related"

    async def list(self, market_id: str, /) -> tuple[v1.Sentiment, ...]:
        """Returns the client sentiment for markets related to the given one.

        ``GET /clientsentiment/related/{market_id}``

        Args:
            market_id: The market identifier.
        """
        return tuple(
            v1.Sentiment.model_validate(sentiment)
            for sentiment in (  # type: ignore[attr-defined]
                await self._requester.get(f"{self.url}/{market_id}")
            )["clientSentiments"]
        )


class ClientSentimentResource(Resource):
    """Client sentiment resource: ``/clientsentiment``."""

    __slots__ = ("related",)

    url: t.Final = "clientsentiment"

    def __init__(self, requester: APIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.related: t.Final = ClientSentimentRelatedResource(requester)

    def get(self, market_id: str, /) -> v1.Sentiment:
        """Returns the client sentiment for the given market.

        ``GET /clientsentiment/{market_id}``

        Args:
            market_id: The market identifier.
        """
        return v1.Sentiment.model_validate(
            self._requester.get(f"{self.url}/{market_id}")
        )

    def list(
        self, market_ids: Iterable[str] | None = None, /
    ) -> tuple[v1.Sentiment, ...]:
        """Returns the client sentiment for the given markets.

        ``GET /clientsentiment``

        Args:
            market_ids: The market identifiers to filter by. Defaults to all
                markets.
        """
        return tuple(
            v1.Sentiment.model_validate(sentiment)
            for sentiment in (  # type: ignore[attr-defined]
                self._requester.get(
                    self.url,
                    params=(
                        {"marketIds": ",".join(market_ids)}
                        if market_ids is not None
                        else None
                    ),
                )
            )["clientSentiments"]
        )


class ClientSentimentRelatedResource(Resource):
    """Client sentiment resource: ``/clientsentiment/related``."""

    __slots__ = ()

    url: t.Final = f"{ClientSentimentResource.url}/related"

    def list(self, market_id: str, /) -> tuple[v1.Sentiment, ...]:
        """Returns the client sentiment for markets related to the given one.

        ``GET /clientsentiment/related/{market_id}``

        Args:
            market_id: The market identifier.
        """
        return tuple(
            v1.Sentiment.model_validate(sentiment)
            for sentiment in (  # type: ignore[attr-defined]
                self._requester.get(f"{self.url}/{market_id}")
            )["clientSentiments"]
        )
