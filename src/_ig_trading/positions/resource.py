from __future__ import annotations

import typing_extensions as t

from _ig_trading.positions import v1, v2
from _ig_trading.resource import AsyncResource, Resource

if t.TYPE_CHECKING:
    from _ig_trading.api_requester import APIRequester, AsyncAPIRequester

OrderType = t.Literal["LIMIT", "MARKET", "QUOTE"]


class AsyncPositionsResource(AsyncResource):
    """Positions resource: ``/positions``.

    Args:
        requester: A REST API requester. Defaults to creating an
            :class:`AsyncAPIRequester` using ``kwargs``.
    """

    __slots__ = ("otc",)

    url: t.Final = "positions"

    def __init__(self, requester: AsyncAPIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.otc: t.Final = AsyncPositionsOTCResource(requester)

    @t.overload
    async def get(
        self, deal_id: str, /, *, version: t.Literal[1]
    ) -> v1.Position: ...

    @t.overload
    async def get(
        self, deal_id: str, /, *, version: t.Literal[2] = ...
    ) -> v2.Position: ...

    async def get(
        self, deal_id: str, /, *, version: t.Literal[1, 2] = 2
    ) -> v1.Position | v2.Position:
        """Returns an open position for the active account by deal identifier.

        ``GET /positions/{deal_id}``

        Args:
            deal_id: Deal identifier.
            version: The API version. Defaults to ``2``.
        """
        return (v1 if version == 1 else v2).Position.model_validate(
            await self._requester.get(f"{self.url}/{deal_id}", version=version)
        )

    @t.overload
    async def list(
        self, *, version: t.Literal[1]
    ) -> tuple[v1.Position, ...]: ...

    @t.overload
    async def list(
        self, *, version: t.Literal[2] = ...
    ) -> tuple[v2.Position, ...]: ...

    async def list(
        self, *, version: t.Literal[1, 2] = 2
    ) -> tuple[v1.Position, ...] | tuple[v2.Position, ...]:
        """Returns all open positions for the active account.

        ``GET /positions``

        Args:
            version: The API version. Defaults to ``2``.
        """
        return tuple(
            (v1 if version == 1 else v2).Position.model_validate(account)
            for account in (  # type: ignore[attr-defined]
                await self._requester.get(self.url, version=version)
            )["positions"]
        )


class AsyncPositionsOTCResource(AsyncResource):
    """Session resource: ``/positions/otc``."""

    url: t.Final = f"{AsyncPositionsResource.url}/otc"

    async def create(
        self,
        *,
        currency_code: str,
        direction: v1.DealDirection,
        epic: str,
        expiry: str,
        force_open: bool,
        guaranteed_stop: bool,
        order_type: OrderType,
        size: float,
        deal_reference: str | None = None,
        level: float | None = None,
        limit_distance: float | None = None,
        limit_level: float | None = None,
        quote_id: str | None = None,
        stop_distance: float | None = None,
        stop_level: float | None = None,
        trailing_stop: bool | None = None,
        trailing_stop_increment: float | None = None,
        version: t.Literal[1, 2] = 2,
    ) -> str:
        """Creates an OTC position.

        ``POST /positions/otc``

        Args:
            currency_code: Currency.
            deal_reference: A user-defined reference identifying the submission
                of the order. Defaults to ``None``.
            direction: Deal direction.
            epic: Instrument epic identifier.
            expiry: Instrument expiry.
            force_open: Whether force open is required.
            guaranteed_stop: Whether guaranteed stop is required.
            level: Deal level. Defaults to ``None``.
            limit_distance: Limit distance. Defaults to ``None``.
            limit_level: Limit level. Defaults to ``None``.
            order_type: Describes the order level model to be used for a
                position operation.
            quote_id: Lightstreamer price quote identifier. Defaults to
                ``None``.
            size: Deal size.
            stop_distance: Stop distance. Defaults to ``None``.
            stop_level: Stop level. Defaults to ``None``.
            trailing_stop: Whether the stop has to be moved towards the current
                level in case of a favourable trade. Defaults to ``None``.
            trailing_stop_increment: Increment step in pips for the trailing
                stop. Defaults to ``None``.
            version: The API version. Defaults to ``2``.
        """
        return (  # type: ignore[return-value]
            await self._requester.post(
                self.url,
                json={
                    "currencyCode": currency_code,
                    "dealReference": deal_reference,
                    "direction": direction,
                    "epic": epic,
                    "expiry": expiry,
                    "forceOpen": force_open,
                    "guaranteedStop": guaranteed_stop,
                    "level": level,
                    "limitDistance": limit_distance,
                    "limitLevel": limit_level,
                    "orderType": order_type,
                    "quoteId": quote_id,
                    "size": size,
                    "stopDistance": stop_distance,
                    "stopLevel": stop_level,
                    "trailingStop": trailing_stop,
                    "trailingStopIncrement": trailing_stop_increment,
                },
                version=version,
            )
        )["dealReference"]

    async def delete(
        self,
        *,
        direction: v1.DealDirection,
        order_type: OrderType,
        size: float,
        epic: str | None = None,
        expiry: str | None = None,
        time_in_force: t.Literal["EXECUTE_AND_ELIMINATE", "FILL_OR_KILL"]
        | None = None,
        deal_id: str | None = None,
        level: float | None = None,
        quote_id: str | None = None,
    ) -> str:
        """Closes one or more OTC positions.

        ``DELETE /positions/otc``

        Args:
            deal_id: Deal identifier. Defaults to ``None``.
            direction: Deal direction.
            epic: Instrument epic identifier. Defaults to ``None``.
            expiry: Instrument expiry. Defaults to ``None``.
            level: Closing deal level. Defaults to ``None``.
            order_type: Describes the order level model to be used for a
                position operation.
            quote_id: Lightstreamer price quote identifier. Defaults to
                ``None``.
            size: Deal size.
            time_in_force: The time in force determines the order fill
                strategy. Defaults to ``None``.
        """
        return (  # type: ignore[return-value]
            await self._requester.delete(
                self.url,
                json={
                    "dealId": deal_id,
                    "direction": direction,
                    "epic": epic,
                    "expiry": expiry,
                    "level": level,
                    "orderType": order_type,
                    "quoteId": quote_id,
                    "size": size,
                    "timeInForce": time_in_force,
                },
            )
        )["dealReference"]

    async def update(
        self,
        deal_id: str,
        /,
        *,
        guaranteed_stop: bool | None = None,
        limit_level: float | None = None,
        stop_level: float | None = None,
        trailing_stop: bool | None = None,
        trailing_stop_distance: float | None = None,
        trailing_stop_increment: float | None = None,
    ) -> str:
        """Updates an OTC position.

        ``PUT /positions/otc/{deal_id}``

        Args:
            deal_id: Deal identifier.
            guaranteed_stop: Whether a guaranteed stop is required. Defaults
                to ``None``.
            limit_level: Limit level. Defaults to ``None``.
            stop_level: Stop level. Defaults to ``None``.
            trailing_stop: Whether trailing stop is required. Defaults to
                ``None``.
            trailing_stop_distance: Trailing stop distance. Defaults to
                ``None``.
            trailing_stop_increment: Trailing stop step increment. Defaults
                to ``None``.
        """
        return (  # type: ignore[return-value]
            await self._requester.put(
                f"{self.url}/{deal_id}",
                json={
                    "guaranteedStop": guaranteed_stop,
                    "limitLevel": limit_level,
                    "stopLevel": stop_level,
                    "trailingStop": trailing_stop,
                    "trailingStopDistance": trailing_stop_distance,
                    "trailingStopIncrement": trailing_stop_increment,
                },
            )
        )["dealReference"]


class PositionsResource(Resource):
    """Positions resource: ``/positions``.

    Args:
        requester: A REST API requester. Defaults to creating an
            :class:`APIRequester` using ``kwargs``.
    """

    __slots__ = ("otc",)

    url: t.Final = "positions"

    def __init__(self, requester: APIRequester | None = None, /) -> None:
        super().__init__(requester)
        self.otc: t.Final = PositionsOTCResource(requester)

    @t.overload
    def get(
        self, deal_id: str, /, *, version: t.Literal[1]
    ) -> v1.Position: ...

    @t.overload
    def get(
        self, deal_id: str, /, *, version: t.Literal[2] = ...
    ) -> v2.Position: ...

    def get(
        self, deal_id: str, /, *, version: t.Literal[1, 2] = 2
    ) -> v1.Position | v2.Position:
        """Returns an open position for the active account by deal identifier.

        ``GET /positions/{deal_id}``

        Args:
            deal_id: Deal identifier.
            version: The API version. Defaults to ``2``.
        """
        return (v1 if version == 1 else v2).Position.model_validate(
            self._requester.get(f"{self.url}/{deal_id}", version=version)
        )

    @t.overload
    def list(self, *, version: t.Literal[1]) -> tuple[v1.Position, ...]: ...

    @t.overload
    def list(
        self, *, version: t.Literal[2] = ...
    ) -> tuple[v2.Position, ...]: ...

    def list(
        self, *, version: t.Literal[1, 2] = 2
    ) -> tuple[v1.Position, ...] | tuple[v2.Position, ...]:
        """Returns all open positions for the active account.

        ``GET /positions``

        Args:
            version: The API version. Defaults to ``2``.
        """
        return tuple(
            (v1 if version == 1 else v2).Position.model_validate(account)
            for account in (  # type: ignore[attr-defined]
                self._requester.get(self.url, version=version)
            )["positions"]
        )


class PositionsOTCResource(Resource):
    """Session resource: ``/positions/otc``."""

    url: t.Final = f"{PositionsResource.url}/otc"

    def create(
        self,
        *,
        currency_code: str,
        direction: v1.DealDirection,
        epic: str,
        expiry: str,
        force_open: bool,
        guaranteed_stop: bool,
        order_type: OrderType,
        size: float,
        deal_reference: str | None = None,
        level: float | None = None,
        limit_distance: float | None = None,
        limit_level: float | None = None,
        quote_id: str | None = None,
        stop_distance: float | None = None,
        stop_level: float | None = None,
        trailing_stop: bool | None = None,
        trailing_stop_increment: float | None = None,
        version: t.Literal[1, 2] = 2,
    ) -> str:
        """Creates an OTC position.

        ``POST /positions/otc``

        Args:
            currency_code: Currency.
            deal_reference: A user-defined reference identifying the submission
                of the order. Defaults to ``None``.
            direction: Deal direction.
            epic: Instrument epic identifier.
            expiry: Instrument expiry.
            force_open: Whether force open is required.
            guaranteed_stop: Whether guaranteed stop is required.
            level: Deal level. Defaults to ``None``.
            limit_distance: Limit distance. Defaults to ``None``.
            limit_level: Limit level. Defaults to ``None``.
            order_type: Describes the order level model to be used for a
                position operation.
            quote_id: Lightstreamer price quote identifier. Defaults to
                ``None``.
            size: Deal size.
            stop_distance: Stop distance. Defaults to ``None``.
            stop_level: Stop level. Defaults to ``None``.
            trailing_stop: Whether the stop has to be moved towards the current
                level in case of a favourable trade. Defaults to ``None``.
            trailing_stop_increment: Increment step in pips for the trailing
                stop. Defaults to ``None``.
            version: The API version. Defaults to ``2``.
        """
        return self._requester.post(  # type: ignore[return-value]
            self.url,
            json={
                "currencyCode": currency_code,
                "dealReference": deal_reference,
                "direction": direction,
                "epic": epic,
                "expiry": expiry,
                "forceOpen": force_open,
                "guaranteedStop": guaranteed_stop,
                "level": level,
                "limitDistance": limit_distance,
                "limitLevel": limit_level,
                "orderType": order_type,
                "quoteId": quote_id,
                "size": size,
                "stopDistance": stop_distance,
                "stopLevel": stop_level,
                "trailingStop": trailing_stop,
                "trailingStopIncrement": trailing_stop_increment,
            },
            version=version,
        )["dealReference"]

    def delete(
        self,
        *,
        direction: v1.DealDirection,
        order_type: OrderType,
        size: float,
        epic: str | None = None,
        expiry: str | None = None,
        time_in_force: t.Literal["EXECUTE_AND_ELIMINATE", "FILL_OR_KILL"]
        | None = None,
        deal_id: str | None = None,
        level: float | None = None,
        quote_id: str | None = None,
    ) -> str:
        """Closes one or more OTC positions.

        ``DELETE /positions/otc``

        Args:
            deal_id: Deal identifier. Defaults to ``None``.
            direction: Deal direction.
            epic: Instrument epic identifier. Defaults to ``None``.
            expiry: Instrument expiry. Defaults to ``None``.
            level: Closing deal level. Defaults to ``None``.
            order_type: Describes the order level model to be used for a
                position operation.
            quote_id: Lightstreamer price quote identifier. Defaults to
                ``None``.
            size: Deal size.
            time_in_force: The time in force determines the order fill
                strategy. Defaults to ``None``.
        """
        return self._requester.delete(  # type: ignore[return-value]
            self.url,
            json={
                "dealId": deal_id,
                "direction": direction,
                "epic": epic,
                "expiry": expiry,
                "level": level,
                "orderType": order_type,
                "quoteId": quote_id,
                "size": size,
                "timeInForce": time_in_force,
            },
        )["dealReference"]

    def update(
        self,
        deal_id: str,
        /,
        *,
        guaranteed_stop: bool | None = None,
        limit_level: float | None = None,
        stop_level: float | None = None,
        trailing_stop: bool | None = None,
        trailing_stop_distance: float | None = None,
        trailing_stop_increment: float | None = None,
    ) -> str:
        """Updates an OTC position.

        ``PUT /positions/otc/{deal_id}``

        Args:
            deal_id: Deal identifier.
            guaranteed_stop: Whether a guaranteed stop is required. Defaults
                to ``None``.
            limit_level: Limit level. Defaults to ``None``.
            stop_level: Stop level. Defaults to ``None``.
            trailing_stop: Whether trailing stop is required. Defaults to
                ``None``.
            trailing_stop_distance: Trailing stop distance. Defaults to
                ``None``.
            trailing_stop_increment: Trailing stop step increment. Defaults
                to ``None``.
        """
        return self._requester.put(  # type: ignore[return-value]
            f"{self.url}/{deal_id}",
            json={
                "guaranteedStop": guaranteed_stop,
                "limitLevel": limit_level,
                "stopLevel": stop_level,
                "trailingStop": trailing_stop,
                "trailingStopDistance": trailing_stop_distance,
                "trailingStopIncrement": trailing_stop_increment,
            },
        )["dealReference"]
