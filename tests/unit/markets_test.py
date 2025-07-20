from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock


_dealing_rule: t.Final = {"unit": "POINTS", "value": 1.0}
_dealing_rules_v1: t.Final = {
    "controlledRiskSpacing": _dealing_rule,
    "marketOrderPreference": "AVAILABLE_DEFAULT_ON",
    "maxStopOrLimitDistance": _dealing_rule,
    "minControlledRiskStopDistance": _dealing_rule,
    "minDealSize": _dealing_rule,
    "minNormalStopOrLimitDistance": _dealing_rule,
    "minStepDistance": _dealing_rule,
}
_dealing_rules_v4: t.Final = {
    "controlledRiskSpacing": _dealing_rule,
    "maxStopOrLimitDistance": _dealing_rule,
    "minControlledRiskStopDistance": _dealing_rule,
    "minDealSize": _dealing_rule,
    "minNormalStopOrLimitDistance": _dealing_rule,
    "minStepDistance": _dealing_rule,
    "trailingStopsPreference": "AVAILABLE",
}
_instrument_v1: t.Final = {
    "chartCode": "EURUSD",
    "contractSize": "1",
    "controlledRiskAllowed": True,
    "country": None,
    "currencies": [],
    "epic": "CS.D.EURUSD.CFD.IP",
    "expiry": "-",
    "expiryDetails": None,
    "forceOpenAllowed": True,
    "lotSize": 1.0,
    "marginDepositBands": [],
    "marketId": "EURUSD",
    "name": "EUR/USD",
    "newsCode": "EURUSD",
    "onePipMeans": "0.0001",
    "openingHours": None,
    "rolloverDetails": None,
    "slippageFactor": {"unit": "pct", "value": 50.0},
    "specialInfo": [],
    "stopsLimitsAllowed": True,
    "streamingPricesAvailable": True,
    "type": "CURRENCIES",
    "unit": "AMOUNT",
    "valueOfOnePip": "1",
}
_instrument_v4: t.Final[dict[str, object]] = {
    "chartCode": "EURUSD",
    "contractSize": "1",
    "country": None,
    "currencies": [],
    "epic": "CS.D.EURUSD.CFD.IP",
    "expiry": "-",
    "lotSize": 1.0,
    "marketId": "EURUSD",
    "name": "EUR/USD",
    "newsCode": "EURUSD",
    "streamingPricesAvailable": True,
    "limitAllowed": True,
    "stopAllowed": True,
    "type": "CURRENCIES",
    "unit": "AMOUNT",
    "valueOfOnePip": "1",
}
_snapshot_v1: t.Final = {
    "bid": 1.1,
    "binaryOdds": None,
    "controlledRiskExtraSpread": None,
    "decimalPlacesFactor": 4,
    "delayTime": 0,
    "high": 1.2,
    "low": 1.0,
    "marketStatus": "TRADEABLE",
    "netChange": 0.0,
    "offer": 1.1,
    "percentageChange": 0.0,
    "scalingFactor": 1,
    "updateTime": "12:00:00",
}
_snapshot_v4: t.Final[dict[str, object]] = {
    "currencyLadders": None,
    "decimalPlacesFactor": 4,
    "delayTime": 0,
    "high": 1.2,
    "low": 1.0,
    "marketStatus": "TRADEABLE",
    "netChange": 0.0,
    "percentageChange": 0.0,
    "priceLadder": [],
    "scalingFactor": 1,
    "updateTimestampUTC": None,
}
_market_v1: t.Final = {
    "dealingRules": _dealing_rules_v1,
    "instrument": _instrument_v1,
    "snapshot": _snapshot_v1,
}
_market_v4: t.Final = {
    "dealingRules": _dealing_rules_v4,
    "instrument": _instrument_v4,
    "snapshot": _snapshot_v4,
}
_market_overview: t.Final = {
    "bid": 1.1,
    "delayTime": 0,
    "epic": "CS.D.EURUSD.CFD.IP",
    "expiry": "-",
    "high": 1.2,
    "instrumentName": "EUR/USD",
    "instrumentType": "CURRENCIES",
    "low": 1.0,
    "marketStatus": "TRADEABLE",
    "netChange": 0.0,
    "offer": 1.1,
    "percentageChange": 0.0,
    "scalingFactor": 1,
    "streamingPricesAvailable": True,
}


@pytest.fixture
def async_markets(async_requester: mock.AsyncMock) -> ig.AsyncMarketsResource:
    return ig.AsyncMarketsResource(async_requester)


@pytest.fixture
def markets(requester: mock.MagicMock) -> ig.MarketsResource:
    return ig.MarketsResource(requester)


async def test_async_get_given_v1(
    async_markets: ig.AsyncMarketsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _market_v1

    result: t.Final = await async_markets.get("CS.D.EURUSD.CFD.IP", version=1)

    async_requester.get.assert_awaited_once_with(
        "markets/CS.D.EURUSD.CFD.IP", version=1
    )
    assert isinstance(result, ig.markets.v1.Market)


async def test_async_get_given_v4_default(
    async_markets: ig.AsyncMarketsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = _market_v4

    result: t.Final = await async_markets.get("CS.D.EURUSD.CFD.IP")

    async_requester.get.assert_awaited_once_with(
        "markets/CS.D.EURUSD.CFD.IP", version=4
    )
    assert isinstance(result, ig.markets.v4.Market)


async def test_async_list_given_epics(
    async_markets: ig.AsyncMarketsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"marketDetails": [_market_v1]}

    result: t.Final = await async_markets.list(["CS.D.EURUSD.CFD.IP"])

    async_requester.get.assert_awaited_once_with(
        "markets",
        params={"epics": "CS.D.EURUSD.CFD.IP", "filter": "ALL"},
        version=2,
    )
    assert len(result) == 1
    assert isinstance(result[0], ig.markets.v1.Market)


async def test_async_list_given_search_term(
    async_markets: ig.AsyncMarketsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"markets": [_market_overview]}

    result: t.Final = await async_markets.list(search_term="EUR")

    async_requester.get.assert_awaited_once_with(
        "markets",
        params={"searchTerm": "EUR", "pageNumber": 1, "pageSize": 50},
        version=2,
    )
    assert result == (
        ig.markets.v1.MarketOverview.model_validate(_market_overview),
    )


async def test_async_list_given_search_term_v1_no_pagination(
    async_markets: ig.AsyncMarketsResource, async_requester: mock.AsyncMock
) -> None:
    async_requester.get.return_value = {"markets": [_market_overview]}

    await async_markets.list(search_term="EUR", version=1)

    async_requester.get.assert_awaited_once_with(
        "markets", params={"searchTerm": "EUR"}, version=1
    )


async def test_async_list_given_neither_epics_nor_search_term(
    async_markets: ig.AsyncMarketsResource,
) -> None:
    with pytest.raises(ValueError, match="Exactly one of"):
        await async_markets.list()  # type: ignore[call-overload]


async def test_async_list_given_both_epics_and_search_term(
    async_markets: ig.AsyncMarketsResource,
) -> None:
    with pytest.raises(ValueError, match="Exactly one of"):
        await async_markets.list(  # type: ignore[call-overload]
            ["CS.D.EURUSD.CFD.IP"], search_term="EUR"
        )


def test_get_given_v1(
    markets: ig.MarketsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _market_v1

    result: t.Final = markets.get("CS.D.EURUSD.CFD.IP", version=1)

    requester.get.assert_called_once_with(
        "markets/CS.D.EURUSD.CFD.IP", version=1
    )
    assert isinstance(result, ig.markets.v1.Market)


def test_get_given_v4_default(
    markets: ig.MarketsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = _market_v4

    result: t.Final = markets.get("CS.D.EURUSD.CFD.IP")

    requester.get.assert_called_once_with(
        "markets/CS.D.EURUSD.CFD.IP", version=4
    )
    assert isinstance(result, ig.markets.v4.Market)


def test_list_given_epics(
    markets: ig.MarketsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"marketDetails": [_market_v1]}

    result: t.Final = markets.list(["CS.D.EURUSD.CFD.IP"])

    requester.get.assert_called_once_with(
        "markets",
        params={"epics": "CS.D.EURUSD.CFD.IP", "filter": "ALL"},
        version=2,
    )
    assert len(result) == 1
    assert isinstance(result[0], ig.markets.v1.Market)


def test_list_given_search_term(
    markets: ig.MarketsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"markets": [_market_overview]}

    result: t.Final = markets.list(search_term="EUR")

    requester.get.assert_called_once_with(
        "markets",
        params={"searchTerm": "EUR", "pageNumber": 1, "pageSize": 50},
        version=2,
    )
    assert result == (
        ig.markets.v1.MarketOverview.model_validate(_market_overview),
    )


def test_list_given_search_term_v1_no_pagination(
    markets: ig.MarketsResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {"markets": [_market_overview]}

    markets.list(search_term="EUR", version=1)

    requester.get.assert_called_once_with(
        "markets", params={"searchTerm": "EUR"}, version=1
    )


def test_list_given_neither_epics_nor_search_term(
    markets: ig.MarketsResource,
) -> None:
    with pytest.raises(ValueError, match="Exactly one of"):
        markets.list()  # type: ignore[call-overload]


def test_list_given_both_epics_and_search_term(
    markets: ig.MarketsResource,
) -> None:
    with pytest.raises(ValueError, match="Exactly one of"):
        markets.list(  # type: ignore[call-overload]
            ["CS.D.EURUSD.CFD.IP"], search_term="EUR"
        )
