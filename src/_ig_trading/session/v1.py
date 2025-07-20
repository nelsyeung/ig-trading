from __future__ import annotations

import datetime as dt

import pydantic
import typing_extensions as t

from _ig_trading.accounts.v1 import AccountType, Balance
from _ig_trading.model import Model

ReroutingEnvironment = t.Literal["DEMO", "LIVE", "TEST", "UAT"]


class Account(Model):
    """Account."""

    #: Account identifier.
    account_id: str
    #: Account name.
    account_name: str
    #: Account type.
    account_type: AccountType
    #: ``True`` if this is the client's preferred account.
    preferred: bool


class AccountSummary(Model):
    """Account summary."""

    #: Account balances.
    account_info: Balance
    #: Account type.
    account_type: AccountType
    #: The client's accounts.
    accounts: tuple[Account, ...]
    #: Client identifier.
    client_id: str
    #: Account currency.
    currency_iso_code: str
    #: Account currency symbol.
    currency_symbol: str
    #: Active account identifier.
    current_account_id: str
    #: ``True`` if the account is enabled for placing trading orders.
    dealing_enabled: bool
    #: ``True`` if the client has active demo accounts.
    has_active_demo_accounts: bool
    #: ``True`` if the client has active live accounts.
    has_active_live_accounts: bool
    #: Lightstreamer endpoint for subscribing to account and price updates.
    lightstreamer_endpoint: str
    #: Rerouting environment.
    rerouting_environment: ReroutingEnvironment | None
    #: Client account timezone offset relative to UTC, expressed in hours.
    timezone_offset: float
    #: ``True`` if the account is allowed to set trailing stops on trades.
    trailing_stops_enabled: bool


class EncryptionKey(Model):
    """Encryption key."""

    #: Encryption key, in Base64 format.
    encryption_key: str
    #: Current timestamp, in milliseconds since epoch.
    time_stamp: int


class OAuthToken(pydantic.BaseModel):
    """OAuth token."""

    model_config = pydantic.ConfigDict(extra="forbid", frozen=True)
    #: Access token.
    access_token: str
    #: Access token expiry, in seconds.
    expires_in: t.Annotated[dt.timedelta, pydantic.BeforeValidator(int)]
    #: Refresh token.
    refresh_token: str
    #: Scope of the access token.
    scope: str
    #: Token type.
    token_type: str


class Session(Model):
    """Session details."""

    #: Active account identifier.
    account_id: str
    #: Client identifier.
    client_id: str
    #: Currency.
    currency: str
    #: Lightstreamer endpoint.
    lightstreamer_endpoint: str
    #: Locale.
    locale: str
    #: Timezone offset relative to UTC, expressed in hours.
    timezone_offset: float


class SwitchAccount(Model):
    """Switched account details."""

    #: ``True`` if the account is enabled for placing trading orders.
    dealing_enabled: bool
    #: ``True`` if the client has active demo accounts.
    has_active_demo_accounts: bool
    #: ``True`` if the client has active live accounts.
    has_active_live_accounts: bool
    #: ``True`` if the account is allowed to set trailing stops on trades.
    trailing_stops_enabled: bool
