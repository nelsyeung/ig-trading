from __future__ import annotations

import typing_extensions as t

from _ig_trading.model import Model

AccountType = t.Literal["CFD", "PHYSICAL", "SPREADBET"]
Status = t.Literal["DISABLED", "ENABLED", "SUSPENDED_FROM_DEALING"]
UpdatePreferencesStatus = t.Literal["SUCCESS"]


class Balance(Model):
    """Account balance."""

    #: Amount available for trading.
    available: float
    #: Balance of funds in the account.
    balance: float
    #: Minimum deposit amount required for margins.
    deposit: float
    #: Profit and loss amount.
    profit_loss: float


class Account(Model):
    """Account."""

    #: Account alias.
    account_alias: str | None
    #: Account identifier.
    account_id: str
    #: Account name.
    account_name: str
    #: Account type.
    account_type: AccountType
    #: Account balances.
    balance: Balance
    #: ``True`` if the account can be transferred from.
    can_transfer_from: bool
    #: ``True`` if the account can be transferred to.
    can_transfer_to: bool
    #: Account currency.
    currency: str
    #: ``True`` if this is the default login account.
    preferred: bool
    #: Account status.
    status: Status


class Preferences(Model):
    """Account preferences."""

    #: ``True`` if the user wants to be allowed to define trailing stop rules
    #: for their trade operations.
    trailing_stops_enabled: bool
