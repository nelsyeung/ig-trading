from __future__ import annotations

from _ig_trading.model import Model
from _ig_trading.session.v1 import OAuthToken


class AccountSummary(Model):
    """Account summary."""

    #: Active account identifier.
    account_id: str
    #: Client identifier.
    client_id: str
    #: Lightstreamer endpoint for subscribing to account and price updates.
    lightstreamer_endpoint: str
    #: OAuth token.
    oauth_token: OAuthToken
    #: Timezone offset of the active account relative to UTC, expressed in
    #: hours.
    timezone_offset: float
