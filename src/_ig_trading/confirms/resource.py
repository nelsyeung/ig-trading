from __future__ import annotations

import typing_extensions as t

from _ig_trading.confirms.v1 import DealConfirmation
from _ig_trading.resource import AsyncResource, Resource


class AsyncConfirmsResource(AsyncResource):
    """Deal confirmation resource: ``/confirms``.

    Args:
        requester: A REST API requester. Defaults to creating an
            :class:`AsyncAPIRequester` using ``kwargs``.
    """

    __slots__ = ()

    url: t.Final = "confirms"

    async def get(self, deal_reference: str, /) -> DealConfirmation:
        """Returns a deal confirmation for the given deal reference.

        Please note, this should only be used if the deal confirmation isn't
        received via the streaming API.

        ``GET /confirms/{deal_reference}``
        """
        return DealConfirmation.model_validate(
            await self._requester.get(f"{self.url}/{deal_reference}")
        )


class ConfirmsResource(Resource):
    """Deal confirmation resource: ``/confirms``.

    Args:
        requester: A REST API requester. Defaults to creating an
            :class:`APIRequester` using ``kwargs``.
    """

    __slots__ = ()

    url: t.Final = "confirms"

    def get(self, deal_reference: str, /) -> DealConfirmation:
        """Returns a deal confirmation for the given deal reference.

        Please note, this should only be used if the deal confirmation isn't
        received via the streaming API.

        ``GET /confirms/{deal_reference}``
        """
        return DealConfirmation.model_validate(
            self._requester.get(f"{self.url}/{deal_reference}")
        )
