from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

_market_id: t.Final = "EURUSD"


@pytest.fixture
def async_client_sentiment(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncClientSentimentResource:
    return ig.AsyncClientSentimentResource(async_requester)


@pytest.fixture
def client_sentiment(
    requester: ig.APIRequester,
) -> ig.ClientSentimentResource:
    return ig.ClientSentimentResource(requester)


async def test_async_list(
    async_client_sentiment: ig.AsyncClientSentimentResource,
) -> None:
    result: t.Final = await async_client_sentiment.list([_market_id])
    assert result
    assert all(
        isinstance(sentiment, ig.client_sentiment.v1.Sentiment)
        for sentiment in result
    )


async def test_async_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncClientSentimentResource().list()


async def test_async_get(
    async_client_sentiment: ig.AsyncClientSentimentResource,
) -> None:
    sentiment: t.Final = await async_client_sentiment.get(_market_id)
    assert sentiment.market_id == _market_id


@pytest.mark.xfail(
    reason=(
        "GET /clientsentiment/related/{market_id} 404s on this demo "
        "account/API key, unlike /clientsentiment and /clientsentiment/"
        "{market_id} which both work; likely a permission restriction "
        "rather than a wrong path."
    ),
    strict=False,
)
async def test_async_related_list(
    async_client_sentiment: ig.AsyncClientSentimentResource,
) -> None:
    result: t.Final = await async_client_sentiment.related.list(_market_id)
    assert all(
        isinstance(sentiment, ig.client_sentiment.v1.Sentiment)
        for sentiment in result
    )


def test_list(client_sentiment: ig.ClientSentimentResource) -> None:
    result: t.Final = client_sentiment.list([_market_id])
    assert result
    assert all(
        isinstance(sentiment, ig.client_sentiment.v1.Sentiment)
        for sentiment in result
    )


def test_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.ClientSentimentResource().list()


def test_get(client_sentiment: ig.ClientSentimentResource) -> None:
    sentiment: t.Final = client_sentiment.get(_market_id)
    assert sentiment.market_id == _market_id


@pytest.mark.xfail(
    reason=(
        "GET /clientsentiment/related/{market_id} 404s on this demo "
        "account/API key, unlike /clientsentiment and /clientsentiment/"
        "{market_id} which both work; likely a permission restriction "
        "rather than a wrong path."
    ),
    strict=False,
)
def test_related_list(
    client_sentiment: ig.ClientSentimentResource,
) -> None:
    result: t.Final = client_sentiment.related.list(_market_id)
    assert all(
        isinstance(sentiment, ig.client_sentiment.v1.Sentiment)
        for sentiment in result
    )
