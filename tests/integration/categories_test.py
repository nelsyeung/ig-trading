from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig


@pytest.fixture
def async_categories(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncCategoriesResource:
    return ig.AsyncCategoriesResource(async_requester)


@pytest.fixture
def categories(requester: ig.APIRequester) -> ig.CategoriesResource:
    return ig.CategoriesResource(requester)


async def test_async_list(
    async_categories: ig.AsyncCategoriesResource,
) -> None:
    result: t.Final = await async_categories.list()
    assert result
    assert all(
        isinstance(category, ig.categories.v1.Category) for category in result
    )


async def test_async_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncCategoriesResource().list()


async def test_async_get(async_categories: ig.AsyncCategoriesResource) -> None:
    category: t.Final = (await async_categories.list())[0]
    instruments: t.Final = await async_categories.get(category.code)
    assert isinstance(instruments, ig.categories.v1.Instruments)


async def test_async_get_given_instruments_missing_market_data(
    async_categories: ig.AsyncCategoriesResource,
) -> None:
    # Some instruments (e.g. certain cryptocurrencies) have no
    # pricing/trading permission on this account, so IG omits their market
    # data fields (bid, high, low, etc.) entirely rather than sending null.
    instruments: t.Final = await async_categories.get("CRYPTOCURRENCY")
    assert instruments.instruments
    assert all(
        isinstance(instrument, ig.categories.v1.Instrument)
        for instrument in instruments.instruments
    )


def test_list(categories: ig.CategoriesResource) -> None:
    result: t.Final = categories.list()
    assert result
    assert all(
        isinstance(category, ig.categories.v1.Category) for category in result
    )


def test_list_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.CategoriesResource().list()


def test_get(categories: ig.CategoriesResource) -> None:
    category: t.Final = categories.list()[0]
    instruments: t.Final = categories.get(category.code)
    assert isinstance(instruments, ig.categories.v1.Instruments)


def test_get_given_instruments_missing_market_data(
    categories: ig.CategoriesResource,
) -> None:
    # Some instruments (e.g. certain cryptocurrencies) have no
    # pricing/trading permission on this account, so IG omits their market
    # data fields (bid, high, low, etc.) entirely rather than sending null.
    instruments: t.Final = categories.get("CRYPTOCURRENCY")
    assert instruments.instruments
    assert all(
        isinstance(instrument, ig.categories.v1.Instrument)
        for instrument in instruments.instruments
    )
