from __future__ import annotations

import typing as t

from _ig_trading.model import Model

CreateStatus = t.Literal["SUCCESS", "SUCCESS_NOT_ALL_INSTRUMENTS_ADDED"]
DeleteStatus = t.Literal["SUCCESS"]
UpdateStatus = t.Literal["SUCCESS"]


class Watchlist(Model):
    """Watchlist."""

    #: ``True`` if this watchlist doesn't belong to the user, but is a system
    #: predefined one.
    default_system_watchlist: bool
    #: ``True`` if this watchlist can be deleted by the user.
    deleteable: bool
    #: ``True`` if this watchlist can be altered by the user.
    editable: bool
    #: Watchlist identifier.
    id: str
    #: Watchlist name.
    name: str


class Watchlists(Model):
    """Watchlists."""

    #: Watchlists.
    watchlists: tuple[Watchlist, ...]


class CreateResult(Model):
    """Result of creating a watchlist."""

    #: Status of the request.
    status: CreateStatus
    #: Identifier of the watchlist just created, if successful.
    watchlist_id: str
