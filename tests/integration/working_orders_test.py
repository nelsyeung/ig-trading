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
def async_working_orders(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncWorkingOrdersResource:
    return ig.AsyncWorkingOrdersResource(async_requester)


@pytest.fixture
def working_orders(requester: ig.APIRequester) -> ig.WorkingOrdersResource:
    return ig.WorkingOrdersResource(requester)


@pytest.fixture
async def async_create_working_order(
    async_confirms: ig.AsyncConfirmsResource,
    async_working_orders: ig.AsyncWorkingOrdersResource,
) -> AsyncIterator[_DealReference]:
    deal_reference: t.Final = await async_working_orders.otc.create(
        currency_code="GBP",
        direction="BUY",
        epic="CS.D.EURGBP.CFD.IP",
        expiry="-",
        guaranteed_stop=False,
        level=0.0001,
        order_type="LIMIT",
        size=1,
        time_in_force="GOOD_TILL_CANCELLED",
    )
    try:
        yield deal_reference
    finally:
        with contextlib.suppress(ig.APIError):
            deal_id: t.Final = (
                await async_confirms.get(deal_reference)
            ).deal_id
            await async_working_orders.otc.delete(deal_id)


@pytest.fixture
def create_working_order(
    confirms: ig.ConfirmsResource,
    working_orders: ig.WorkingOrdersResource,
) -> Iterator[_DealReference]:
    deal_reference: t.Final = working_orders.otc.create(
        currency_code="GBP",
        direction="BUY",
        epic="CS.D.EURGBP.CFD.IP",
        expiry="-",
        guaranteed_stop=False,
        level=0.0001,
        order_type="LIMIT",
        size=1,
        time_in_force="GOOD_TILL_CANCELLED",
    )
    try:
        yield deal_reference
    finally:
        with contextlib.suppress(ig.APIError):
            deal_id: t.Final = confirms.get(deal_reference).deal_id
            working_orders.otc.delete(deal_id)


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.working_orders.v1.WorkingOrder),
        (2, ig.working_orders.v2.WorkingOrder),
    ],
    ids=("v1", "v2"),
)
async def test_async_list(
    async_create_working_order: _DealReference,
    async_working_orders: ig.AsyncWorkingOrdersResource,
    expected: type,
    version: t.Literal[1, 2],
) -> None:
    assert async_create_working_order
    result: t.Final = await async_working_orders.list(version=version)
    assert result
    assert all(isinstance(order, expected) for order in result)


async def test_async_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncWorkingOrdersResource().list()


async def test_async_otc_create(
    async_confirms: ig.AsyncConfirmsResource,
    async_create_working_order: _DealReference,
    async_working_orders: ig.AsyncWorkingOrdersResource,
) -> None:
    assert (
        await async_confirms.get(async_create_working_order)
    ).reason == "SUCCESS"
    assert await async_working_orders.list()


async def test_async_otc_delete(
    async_confirms: ig.AsyncConfirmsResource,
    async_create_working_order: _DealReference,
    async_working_orders: ig.AsyncWorkingOrdersResource,
) -> None:
    deal_id: t.Final = (
        await async_confirms.get(async_create_working_order)
    ).deal_id
    deal_reference: t.Final = await async_working_orders.otc.delete(deal_id)
    assert (await async_confirms.get(deal_reference)).reason == "SUCCESS"


async def test_async_otc_update(
    async_confirms: ig.AsyncConfirmsResource,
    async_create_working_order: _DealReference,
    async_working_orders: ig.AsyncWorkingOrdersResource,
) -> None:
    deal_id: t.Final = (
        await async_confirms.get(async_create_working_order)
    ).deal_id
    deal_reference: t.Final = await async_working_orders.otc.update(
        deal_id,
        level=0.0002,
        order_type="LIMIT",
        time_in_force="GOOD_TILL_CANCELLED",
    )
    assert (await async_confirms.get(deal_reference)).reason == "SUCCESS"


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.working_orders.v1.WorkingOrder),
        (2, ig.working_orders.v2.WorkingOrder),
    ],
    ids=("v1", "v2"),
)
def test_list(
    create_working_order: _DealReference,
    expected: type,
    version: t.Literal[1, 2],
    working_orders: ig.WorkingOrdersResource,
) -> None:
    assert create_working_order
    result: t.Final = working_orders.list(version=version)
    assert result
    assert all(isinstance(order, expected) for order in result)


def test_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.WorkingOrdersResource().list()


def test_otc_create(
    confirms: ig.ConfirmsResource,
    create_working_order: _DealReference,
    working_orders: ig.WorkingOrdersResource,
) -> None:
    assert confirms.get(create_working_order).reason == "SUCCESS"
    assert working_orders.list()


def test_otc_delete(
    confirms: ig.ConfirmsResource,
    create_working_order: _DealReference,
    working_orders: ig.WorkingOrdersResource,
) -> None:
    deal_id: t.Final = confirms.get(create_working_order).deal_id
    deal_reference: t.Final = working_orders.otc.delete(deal_id)
    assert confirms.get(deal_reference).reason == "SUCCESS"


def test_otc_update(
    confirms: ig.ConfirmsResource,
    create_working_order: _DealReference,
    working_orders: ig.WorkingOrdersResource,
) -> None:
    deal_id: t.Final = confirms.get(create_working_order).deal_id
    deal_reference: t.Final = working_orders.otc.update(
        deal_id,
        level=0.0002,
        order_type="LIMIT",
        time_in_force="GOOD_TILL_CANCELLED",
    )
    assert confirms.get(deal_reference).reason == "SUCCESS"
