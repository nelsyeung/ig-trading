from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock

_sentiment: t.Final = {
    "longPositionPercentage": 60.0,
    "marketId": "EURUSD",
    "shortPositionPercentage": 40.0,
}


@pytest.fixture
def async_client_sentiment(
    async_requester: mock.AsyncMock,
) -> ig.AsyncClientSentimentResource:
    return ig.AsyncClientSentimentResource(async_requester)


@pytest.fixture
def client_sentiment(
    requester: mock.MagicMock,
) -> ig.ClientSentimentResource:
    return ig.ClientSentimentResource(requester)


async def test_async_get(
    async_client_sentiment: ig.AsyncClientSentimentResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = _sentiment

    result: t.Final = await async_client_sentiment.get("EURUSD")

    async_requester.get.assert_awaited_once_with("clientsentiment/EURUSD")
    assert result == ig.client_sentiment.v1.Sentiment.model_validate(
        _sentiment
    )


async def test_async_list_given_no_market_ids(
    async_client_sentiment: ig.AsyncClientSentimentResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {"clientSentiments": [_sentiment]}

    result: t.Final = await async_client_sentiment.list()

    async_requester.get.assert_awaited_once_with(
        "clientsentiment", params=None
    )
    assert result == (
        ig.client_sentiment.v1.Sentiment.model_validate(_sentiment),
    )


async def test_async_list_given_market_ids(
    async_client_sentiment: ig.AsyncClientSentimentResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {"clientSentiments": [_sentiment]}

    await async_client_sentiment.list(["EURUSD", "GBPUSD"])

    async_requester.get.assert_awaited_once_with(
        "clientsentiment", params={"marketIds": "EURUSD,GBPUSD"}
    )


async def test_async_related_list(
    async_client_sentiment: ig.AsyncClientSentimentResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {"clientSentiments": [_sentiment]}

    result: t.Final = await async_client_sentiment.related.list("EURUSD")

    async_requester.get.assert_awaited_once_with(
        "clientsentiment/related/EURUSD"
    )
    assert result == (
        ig.client_sentiment.v1.Sentiment.model_validate(_sentiment),
    )


def test_get(
    client_sentiment: ig.ClientSentimentResource,
    requester: mock.MagicMock,
) -> None:
    requester.get.return_value = _sentiment

    result: t.Final = client_sentiment.get("EURUSD")

    requester.get.assert_called_once_with("clientsentiment/EURUSD")
    assert result == ig.client_sentiment.v1.Sentiment.model_validate(
        _sentiment
    )


def test_list_given_no_market_ids(
    client_sentiment: ig.ClientSentimentResource,
    requester: mock.MagicMock,
) -> None:
    requester.get.return_value = {"clientSentiments": [_sentiment]}

    result: t.Final = client_sentiment.list()

    requester.get.assert_called_once_with("clientsentiment", params=None)
    assert result == (
        ig.client_sentiment.v1.Sentiment.model_validate(_sentiment),
    )


def test_list_given_market_ids(
    client_sentiment: ig.ClientSentimentResource,
    requester: mock.MagicMock,
) -> None:
    requester.get.return_value = {"clientSentiments": [_sentiment]}

    client_sentiment.list(["EURUSD", "GBPUSD"])

    requester.get.assert_called_once_with(
        "clientsentiment", params={"marketIds": "EURUSD,GBPUSD"}
    )


def test_related_list(
    client_sentiment: ig.ClientSentimentResource,
    requester: mock.MagicMock,
) -> None:
    requester.get.return_value = {"clientSentiments": [_sentiment]}

    result: t.Final = client_sentiment.related.list("EURUSD")

    requester.get.assert_called_once_with("clientsentiment/related/EURUSD")
    assert result == (
        ig.client_sentiment.v1.Sentiment.model_validate(_sentiment),
    )
