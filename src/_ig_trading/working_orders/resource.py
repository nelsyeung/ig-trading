from __future__ import annotations

import typing_extensions as t

from _ig_trading.resource import AsyncResource, Resource
from _ig_trading.working_orders import v1, v2

if t.TYPE_CHECKING:
    from _ig_trading.api_requester import APIRequester, AsyncAPIRequester
    from _ig_trading.positions.v1 import DealDirection

OrderType = t.Literal["LIMIT", "STOP"]
TimeInForce = t.Literal["GOOD_TILL_CANCELLED", "GOOD_TILL_DATE"]


class AsyncWorkingOrdersResource(AsyncResource):
    """Working orders resource: ``/workingorders``.

    Args:
        requester: A REST API requester. Defaults to creating an
            :class:`AsyncAPIRequester` using ``kwargs``.
    """

    __slots__ = ("otc",)

    url: t.Final = "workingorders"

    def __init__(self, requester: AsyncAPIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.otc: t.Final = AsyncWorkingOrdersOTCResource(requester)

    @t.overload
    async def list(
        self, *, version: t.Literal[1]
    ) -> tuple[v1.WorkingOrder, ...]: ...

    @t.overload
    async def list(
        self, *, version: t.Literal[2] = ...
    ) -> tuple[v2.WorkingOrder, ...]: ...

    async def list(
        self, *, version: t.Literal[1, 2] = 2
    ) -> tuple[v1.WorkingOrder, ...] | tuple[v2.WorkingOrder, ...]:
        """Returns all open working orders for the active account.

        ``GET /workingorders``

        Args:
            version: The API version. Defaults to ``2``.
        """
        return tuple(
            (v1 if version == 1 else v2).WorkingOrder.model_validate(order)
            for order in (  # type: ignore[attr-defined]
                await self._requester.get(self.url, version=version)
            )["workingOrders"]
        )


class AsyncWorkingOrdersOTCResource(AsyncResource):
    """Working orders resource: ``/workingorders/otc``."""

    url: t.Final = f"{AsyncWorkingOrdersResource.url}/otc"

    async def create(
        self,
        *,
        currency_code: str,
        direction: DealDirection,
        epic: str,
        expiry: str,
        guaranteed_stop: bool,
        level: float,
        order_type: OrderType,
        size: float,
        time_in_force: TimeInForce,
        deal_reference: str | None = None,
        force_open: bool | None = None,
        good_till_date: str | None = None,
        limit_distance: float | None = None,
        limit_level: float | None = None,
        stop_distance: float | None = None,
        stop_level: float | None = None,
        version: t.Literal[1, 2] = 2,
    ) -> str:
        """Creates an OTC working order.

        ``POST /workingorders/otc``

        Args:
            currency_code: Currency. Restricted to available instrument
                currencies.
            deal_reference: A user-defined reference identifying the submission
                of the order. Defaults to ``None``.
            direction: Deal direction.
            epic: Instrument epic.
            expiry: Instrument expiry.
            force_open: Whether force open is required. Defaults to
                ``None``.
            good_till_date: Good till date. Accepts either ``yyyy/mm/dd
                hh:mm:ss`` in UTC or a Unix timestamp in milliseconds.
                Defaults to ``None``.
            guaranteed_stop: Whether guaranteed stop is required.
            level: Price at which to execute the trade.
            limit_distance: Limit distance. Defaults to ``None``.
            limit_level: Limit level. Defaults to ``None``.
            order_type: Working order type.
            size: Order size.
            stop_distance: Stop distance. Defaults to ``None``.
            stop_level: Stop level. Defaults to ``None``.
            time_in_force: Describes the type of time in force for a given
                order.
            version: The API version. Defaults to ``2``.
        """
        json: t.Final = {
            "currencyCode": currency_code,
            "dealReference": deal_reference,
            "direction": direction,
            "epic": epic,
            "expiry": expiry,
            "forceOpen": force_open,
            "goodTillDate": good_till_date,
            "guaranteedStop": guaranteed_stop,
            "level": level,
            "limitDistance": limit_distance,
            "limitLevel": limit_level,
            "size": size,
            "stopDistance": stop_distance,
            "stopLevel": stop_level,
            "timeInForce": time_in_force,
            "type": order_type,
        }
        return (  # type: ignore[return-value]
            await self._requester.post(
                self.url,
                json={k: v for k, v in json.items() if v is not None},
                version=version,
            )
        )["dealReference"]

    async def delete(self, deal_id: str, /) -> str:
        """Deletes an OTC working order.

        ``DELETE /workingorders/otc/{deal_id}``

        Args:
            deal_id: Deal identifier.
        """
        return (  # type: ignore[return-value]
            await self._requester.delete(f"{self.url}/{deal_id}", json={})
        )["dealReference"]

    async def update(
        self,
        deal_id: str,
        /,
        *,
        order_type: OrderType,
        time_in_force: TimeInForce,
        good_till_date: str | None = None,
        guaranteed_stop: bool | None = None,
        level: float | None = None,
        limit_distance: float | None = None,
        limit_level: float | None = None,
        stop_distance: float | None = None,
        stop_level: float | None = None,
    ) -> str:
        """Updates an OTC working order.

        ``PUT /workingorders/otc/{deal_id}``

        Args:
            deal_id: Deal identifier.
            good_till_date: Good till date. Accepts either ``yyyy/mm/dd
                hh:mm:ss`` in UTC or a Unix timestamp in milliseconds.
                Defaults to ``None``.
            guaranteed_stop: Whether guaranteed stop is required. Defaults
                to ``None``.
            level: Price at which to execute the trade. Defaults to
                ``None``.
            limit_distance: Limit distance. Defaults to ``None``.
            limit_level: Limit level. Defaults to ``None``.
            order_type: Working order type.
            stop_distance: Stop distance. Defaults to ``None``.
            stop_level: Stop level. Defaults to ``None``.
            time_in_force: Describes the type of time in force for a given
                order.
        """
        json: t.Final = {
            "goodTillDate": good_till_date,
            "guaranteedStop": guaranteed_stop,
            "level": level,
            "limitDistance": limit_distance,
            "limitLevel": limit_level,
            "stopDistance": stop_distance,
            "stopLevel": stop_level,
            "timeInForce": time_in_force,
            "type": order_type,
        }
        return (  # type: ignore[return-value]
            await self._requester.put(
                f"{self.url}/{deal_id}",
                json={k: v for k, v in json.items() if v is not None},
            )
        )["dealReference"]


class WorkingOrdersResource(Resource):
    """Working orders resource: ``/workingorders``.

    Args:
        requester: A REST API requester. Defaults to creating an
            :class:`APIRequester` using ``kwargs``.
    """

    __slots__ = ("otc",)

    url: t.Final = "workingorders"

    def __init__(self, requester: APIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.otc: t.Final = WorkingOrdersOTCResource(requester)

    @t.overload
    def list(
        self, *, version: t.Literal[1]
    ) -> tuple[v1.WorkingOrder, ...]: ...

    @t.overload
    def list(
        self, *, version: t.Literal[2] = ...
    ) -> tuple[v2.WorkingOrder, ...]: ...

    def list(
        self, *, version: t.Literal[1, 2] = 2
    ) -> tuple[v1.WorkingOrder, ...] | tuple[v2.WorkingOrder, ...]:
        """Returns all open working orders for the active account.

        ``GET /workingorders``

        Args:
            version: The API version. Defaults to ``2``.
        """
        return tuple(
            (v1 if version == 1 else v2).WorkingOrder.model_validate(order)
            for order in (  # type: ignore[attr-defined]
                self._requester.get(self.url, version=version)
            )["workingOrders"]
        )


class WorkingOrdersOTCResource(Resource):
    """Working orders resource: ``/workingorders/otc``."""

    url: t.Final = f"{WorkingOrdersResource.url}/otc"

    def create(
        self,
        *,
        currency_code: str,
        direction: DealDirection,
        epic: str,
        expiry: str,
        guaranteed_stop: bool,
        level: float,
        order_type: OrderType,
        size: float,
        time_in_force: TimeInForce,
        deal_reference: str | None = None,
        force_open: bool | None = None,
        good_till_date: str | None = None,
        limit_distance: float | None = None,
        limit_level: float | None = None,
        stop_distance: float | None = None,
        stop_level: float | None = None,
        version: t.Literal[1, 2] = 2,
    ) -> str:
        """Creates an OTC working order.

        ``POST /workingorders/otc``

        Args:
            currency_code: Currency. Restricted to available instrument
                currencies.
            deal_reference: A user-defined reference identifying the submission
                of the order. Defaults to ``None``.
            direction: Deal direction.
            epic: Instrument epic.
            expiry: Instrument expiry.
            force_open: Whether force open is required. Defaults to
                ``None``.
            good_till_date: Good till date. Accepts either ``yyyy/mm/dd
                hh:mm:ss`` in UTC or a Unix timestamp in milliseconds.
                Defaults to ``None``.
            guaranteed_stop: Whether guaranteed stop is required.
            level: Price at which to execute the trade.
            limit_distance: Limit distance. Defaults to ``None``.
            limit_level: Limit level. Defaults to ``None``.
            order_type: Working order type.
            size: Order size.
            stop_distance: Stop distance. Defaults to ``None``.
            stop_level: Stop level. Defaults to ``None``.
            time_in_force: Describes the type of time in force for a given
                order.
            version: The API version. Defaults to ``2``.
        """
        json: t.Final = {
            "currencyCode": currency_code,
            "dealReference": deal_reference,
            "direction": direction,
            "epic": epic,
            "expiry": expiry,
            "forceOpen": force_open,
            "goodTillDate": good_till_date,
            "guaranteedStop": guaranteed_stop,
            "level": level,
            "limitDistance": limit_distance,
            "limitLevel": limit_level,
            "size": size,
            "stopDistance": stop_distance,
            "stopLevel": stop_level,
            "timeInForce": time_in_force,
            "type": order_type,
        }
        return self._requester.post(  # type: ignore[return-value]
            self.url,
            json={k: v for k, v in json.items() if v is not None},
            version=version,
        )["dealReference"]

    def delete(self, deal_id: str, /) -> str:
        """Deletes an OTC working order.

        ``DELETE /workingorders/otc/{deal_id}``

        Args:
            deal_id: Deal identifier.
        """
        return self._requester.delete(  # type: ignore[return-value]
            f"{self.url}/{deal_id}", json={}
        )["dealReference"]

    def update(
        self,
        deal_id: str,
        /,
        *,
        order_type: OrderType,
        time_in_force: TimeInForce,
        good_till_date: str | None = None,
        guaranteed_stop: bool | None = None,
        level: float | None = None,
        limit_distance: float | None = None,
        limit_level: float | None = None,
        stop_distance: float | None = None,
        stop_level: float | None = None,
    ) -> str:
        """Updates an OTC working order.

        ``PUT /workingorders/otc/{deal_id}``

        Args:
            deal_id: Deal identifier.
            good_till_date: Good till date. Accepts either ``yyyy/mm/dd
                hh:mm:ss`` in UTC or a Unix timestamp in milliseconds.
                Defaults to ``None``.
            guaranteed_stop: Whether guaranteed stop is required. Defaults
                to ``None``.
            level: Price at which to execute the trade. Defaults to
                ``None``.
            limit_distance: Limit distance. Defaults to ``None``.
            limit_level: Limit level. Defaults to ``None``.
            order_type: Working order type.
            stop_distance: Stop distance. Defaults to ``None``.
            stop_level: Stop level. Defaults to ``None``.
            time_in_force: Describes the type of time in force for a given
                order.
        """
        json: t.Final = {
            "goodTillDate": good_till_date,
            "guaranteedStop": guaranteed_stop,
            "level": level,
            "limitDistance": limit_distance,
            "limitLevel": limit_level,
            "stopDistance": stop_distance,
            "stopLevel": stop_level,
            "timeInForce": time_in_force,
            "type": order_type,
        }
        return self._requester.put(  # type: ignore[return-value]
            f"{self.url}/{deal_id}",
            json={k: v for k, v in json.items() if v is not None},
        )["dealReference"]
