from __future__ import annotations

import typing_extensions as t

from _ig_trading.categories import v1
from _ig_trading.resource import AsyncResource, Resource


class AsyncCategoriesResource(AsyncResource):
    """Categories resource: ``/categories``."""

    __slots__ = ()

    url: t.Final = "categories"

    async def get(self, category_id: str, /) -> v1.Instruments:
        """Returns all instruments for the given category.

        ``GET /categories/{category_id}/instruments``

        Args:
            category_id: The category identifier.
        """
        return v1.Instruments.model_validate(
            await self._requester.get(f"{self.url}/{category_id}/instruments")
        )

    async def list(self) -> tuple[v1.Category, ...]:
        """Returns all categories of instruments enabled for the account.

        ``GET /categories``
        """
        return tuple(
            v1.Category.model_validate(category)
            for category in (  # type: ignore[attr-defined]
                await self._requester.get(self.url)
            )["categories"]
        )


class CategoriesResource(Resource):
    """Categories resource: ``/categories``."""

    __slots__ = ()

    url: t.Final = "categories"

    def get(self, category_id: str, /) -> v1.Instruments:
        """Returns all instruments for the given category.

        ``GET /categories/{category_id}/instruments``

        Args:
            category_id: The category identifier.
        """
        return v1.Instruments.model_validate(
            self._requester.get(f"{self.url}/{category_id}/instruments")
        )

    def list(self) -> tuple[v1.Category, ...]:
        """Returns all categories of instruments enabled for the account.

        ``GET /categories``
        """
        return tuple(
            v1.Category.model_validate(category)
            for category in (  # type: ignore[attr-defined]
                self._requester.get(self.url)
            )["categories"]
        )
