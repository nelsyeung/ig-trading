from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig

if t.TYPE_CHECKING:
    from unittest import mock


@pytest.fixture
def async_categories(
    async_requester: mock.AsyncMock,
) -> ig.AsyncCategoriesResource:
    return ig.AsyncCategoriesResource(async_requester)


@pytest.fixture
def categories(requester: mock.MagicMock) -> ig.CategoriesResource:
    return ig.CategoriesResource(requester)


async def test_async_get(
    async_categories: ig.AsyncCategoriesResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {
        "instruments": [
            {"epic": "CS.D.EURUSD.CFD.IP", "instrumentName": "EUR/USD"}
        ],
        "metadata": {
            "pageNumber": 1,
            "pageSize": 500,
            "totalPages": 1,
            "totalResults": 1,
        },
    }

    result: t.Final = await async_categories.get("CURRENCIES")

    async_requester.get.assert_awaited_once_with(
        "categories/CURRENCIES/instruments"
    )
    assert isinstance(result, ig.categories.v1.Instruments)
    assert result.instruments[0].epic == "CS.D.EURUSD.CFD.IP"


async def test_async_list(
    async_categories: ig.AsyncCategoriesResource,
    async_requester: mock.AsyncMock,
) -> None:
    async_requester.get.return_value = {
        "categories": [
            {"code": "CURRENCIES", "nonTradeable": False},
            {"code": "CRYPTOCURRENCY", "nonTradeable": True},
        ]
    }

    result: t.Final = await async_categories.list()

    async_requester.get.assert_awaited_once_with("categories")
    assert result == (
        ig.categories.v1.Category.model_validate(
            {"code": "CURRENCIES", "nonTradeable": False}
        ),
        ig.categories.v1.Category.model_validate(
            {"code": "CRYPTOCURRENCY", "nonTradeable": True}
        ),
    )


def test_get(
    categories: ig.CategoriesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {
        "instruments": [
            {"epic": "CS.D.EURUSD.CFD.IP", "instrumentName": "EUR/USD"}
        ],
        "metadata": {
            "pageNumber": 1,
            "pageSize": 500,
            "totalPages": 1,
            "totalResults": 1,
        },
    }

    result: t.Final = categories.get("CURRENCIES")

    requester.get.assert_called_once_with("categories/CURRENCIES/instruments")
    assert isinstance(result, ig.categories.v1.Instruments)
    assert result.instruments[0].epic == "CS.D.EURUSD.CFD.IP"


def test_list(
    categories: ig.CategoriesResource, requester: mock.MagicMock
) -> None:
    requester.get.return_value = {
        "categories": [
            {"code": "CURRENCIES", "nonTradeable": False},
            {"code": "CRYPTOCURRENCY", "nonTradeable": True},
        ]
    }

    result: t.Final = categories.list()

    requester.get.assert_called_once_with("categories")
    assert result == (
        ig.categories.v1.Category.model_validate(
            {"code": "CURRENCIES", "nonTradeable": False}
        ),
        ig.categories.v1.Category.model_validate(
            {"code": "CRYPTOCURRENCY", "nonTradeable": True}
        ),
    )
