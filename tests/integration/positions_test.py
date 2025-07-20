from __future__ import annotations

import contextlib

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

    _DealReference = str


@pytest.fixture
def async_confirms(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncConfirmsResource:
    return ig.AsyncConfirmsResource(async_requester)


@pytest.fixture
def confirms(requester: ig.APIRequester) -> ig.ConfirmsResource:
    return ig.ConfirmsResource(requester)


@pytest.fixture
def async_markets(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncMarketsResource:
    return ig.AsyncMarketsResource(async_requester)


@pytest.fixture
def markets(requester: ig.APIRequester) -> ig.MarketsResource:
    return ig.MarketsResource(requester)


@pytest.fixture
async def async_create_position(
    async_markets: ig.AsyncMarketsResource,
    async_positions: ig.AsyncPositionsResource,
) -> AsyncIterator[_DealReference]:
    epic: t.Final = "CS.D.EURGBP.CFD.IP"
    market: t.Final = await async_markets.get(epic, version=1)

    if market.snapshot.market_status != "TRADEABLE":
        pytest.skip(
            f"{epic} isn't tradeable right now "
            f"(status: {market.snapshot.market_status})"
        )

    order_type: t.Final = "MARKET"
    try:
        deal_reference: t.Final = await async_positions.otc.create(
            currency_code="GBP",
            direction="BUY",
            epic=epic,
            expiry="-",
            force_open=True,
            guaranteed_stop=False,
            order_type=order_type,
            limit_distance=10,
            stop_distance=10,
            size=1,
        )
        yield deal_reference
    finally:
        with contextlib.suppress(AssertionError):
            position: t.Final = await _get_position_from_deal_reference(
                async_positions, deal_reference
            )
            await async_positions.otc.delete(
                deal_id=position.deal_id,
                direction=position.direction,
                order_type=order_type,
                size=position.size,
            )


@pytest.fixture
def async_positions(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncPositionsResource:
    return ig.AsyncPositionsResource(async_requester)


@pytest.fixture
def positions(requester: ig.APIRequester) -> ig.PositionsResource:
    return ig.PositionsResource(requester)


@pytest.fixture
def create_position(
    markets: ig.MarketsResource,
    positions: ig.PositionsResource,
) -> Iterator[_DealReference]:
    epic: t.Final = "CS.D.EURGBP.CFD.IP"
    market: t.Final = markets.get(epic, version=1)

    if market.snapshot.market_status != "TRADEABLE":
        pytest.skip(
            f"{epic} isn't tradeable right now "
            f"(status: {market.snapshot.market_status})"
        )

    order_type: t.Final = "MARKET"
    try:
        deal_reference: t.Final = positions.otc.create(
            currency_code="GBP",
            direction="BUY",
            epic=epic,
            expiry="-",
            force_open=True,
            guaranteed_stop=False,
            order_type=order_type,
            limit_distance=10,
            stop_distance=10,
            size=1,
        )
        yield deal_reference
    finally:
        with contextlib.suppress(AssertionError):
            position: t.Final = _get_sync_position_from_deal_reference(
                positions, deal_reference
            )
            positions.otc.delete(
                deal_id=position.deal_id,
                direction=position.direction,
                order_type=order_type,
                size=position.size,
            )


async def test_async_get(
    async_create_position: _DealReference,
    async_positions: ig.AsyncPositionsResource,
) -> None:
    position: t.Final = await _get_position_from_deal_reference(
        async_positions, async_create_position
    )
    assert await async_positions.get(position.deal_id)


async def test_async_otc_create(
    async_confirms: ig.AsyncConfirmsResource,
    async_create_position: _DealReference,
    async_positions: ig.AsyncPositionsResource,
) -> None:
    assert (
        await async_confirms.get(async_create_position)
    ).reason == "SUCCESS"
    assert await async_positions.list()


async def test_async_otc_update(
    async_confirms: ig.AsyncConfirmsResource,
    async_create_position: _DealReference,
    async_positions: ig.AsyncPositionsResource,
) -> None:
    position: t.Final = await _get_position_from_deal_reference(
        async_positions, async_create_position
    )
    deal_reference: t.Final = await async_positions.otc.update(
        position.deal_id,
        limit_level=position.limit_level,
        stop_level=position.stop_level,
    )
    assert (await async_confirms.get(deal_reference)).reason == "SUCCESS"


async def test_async_otc_delete(
    async_confirms: ig.AsyncConfirmsResource,
    async_create_position: _DealReference,
    async_positions: ig.AsyncPositionsResource,
) -> None:
    position: t.Final = await _get_position_from_deal_reference(
        async_positions, async_create_position
    )
    assert position.deal_id
    deal_reference: t.Final = await async_positions.otc.delete(
        deal_id=position.deal_id,
        direction=position.direction,
        order_type="MARKET",
        size=position.size,
    )
    assert (await async_confirms.get(deal_reference)).reason == "SUCCESS"


def test_get(
    create_position: _DealReference, positions: ig.PositionsResource
) -> None:
    position: t.Final = _get_sync_position_from_deal_reference(
        positions, create_position
    )
    assert positions.get(position.deal_id)


def test_otc_create(
    confirms: ig.ConfirmsResource,
    create_position: _DealReference,
    positions: ig.PositionsResource,
) -> None:
    assert confirms.get(create_position).reason == "SUCCESS"
    assert positions.list()


def test_otc_update(
    confirms: ig.ConfirmsResource,
    create_position: _DealReference,
    positions: ig.PositionsResource,
) -> None:
    position: t.Final = _get_sync_position_from_deal_reference(
        positions, create_position
    )
    deal_reference: t.Final = positions.otc.update(
        position.deal_id,
        limit_level=position.limit_level,
        stop_level=position.stop_level,
    )
    assert confirms.get(deal_reference).reason == "SUCCESS"


def test_otc_delete(
    confirms: ig.ConfirmsResource,
    create_position: _DealReference,
    positions: ig.PositionsResource,
) -> None:
    position: t.Final = _get_sync_position_from_deal_reference(
        positions, create_position
    )
    assert position.deal_id
    deal_reference: t.Final = positions.otc.delete(
        deal_id=position.deal_id,
        direction=position.direction,
        order_type="MARKET",
        size=position.size,
    )
    assert confirms.get(deal_reference).reason == "SUCCESS"


async def _get_position_from_deal_reference(
    positions: ig.AsyncPositionsResource, deal_reference: _DealReference, /
) -> ig.positions.v2.PositionData:
    position: t.Final = next(
        (
            position.position
            for position in await positions.list()
            if position.position.deal_reference == deal_reference
        ),
        None,
    )
    assert position is not None, (
        f"Position with deal reference {deal_reference} not found"
    )
    return position


def _get_sync_position_from_deal_reference(
    positions: ig.PositionsResource, deal_reference: _DealReference, /
) -> ig.positions.v2.PositionData:
    position: t.Final = next(
        (
            position.position
            for position in positions.list()
            if position.position.deal_reference == deal_reference
        ),
        None,
    )
    assert position is not None, (
        f"Position with deal reference {deal_reference} not found"
    )
    return position
