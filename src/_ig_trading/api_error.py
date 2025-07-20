from __future__ import annotations

import abc

import aiohttp
import typing_extensions as t

APIVersion = t.Literal[1, 2, 3]
ClientSession = aiohttp.ClientSession


class APIError(Exception, abc.ABC):
    """API call error.

    Args:
        status: The HTTP status code.
    """

    __slots__ = ("status",)

    def __init__(self, *, status: int) -> None:
        self.status: t.Final = status  #: The HTTP status code.
        super().__init__(f"{status} [{self.error_code}] {self.description}")

    @classmethod
    def from_error_code(
        cls, error_code: str, /, *, status: int
    ) -> APIError | None:
        return next(
            (
                klass(status=status)
                for klass in cls.__subclasses__()
                if not issubclass(klass, UnknownAPIError)
                and klass.error_code == error_code
            ),
            None,
        )

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """The error description."""

    @property
    @abc.abstractmethod
    def error_code(self) -> str:
        """The IG API error code."""


class UnknownAPIError(APIError):
    """An API error that doesn't map to any known IG API error code."""

    def __init__(
        self, *, description: str, error_code: str, status: int
    ) -> None:
        self._description: t.Final = description
        self._error_code: t.Final = error_code
        super().__init__(status=status)

    @t.override
    @property
    def description(self) -> str:
        """The error description."""
        return self._description

    @t.override
    @property
    def error_code(self) -> str:
        """The IG API error code."""
        return self._error_code


class DealExecutionNotFoundError(APIError):
    """Unable to find the deal to execute the requested operation on.

    Maps to the ``error.service.execution.find`` IG API error code. Unlike
    the other error codes here, this one isn't documented by IG; the
    description is inferred from its name and observed behaviour. It has
    been seen shortly after creating a deal, when acting on it again (e.g.
    updating or deleting) immediately afterwards — seemingly a brief
    propagation delay between IG's confirmation and execution services
    rather than the deal genuinely not existing, since retrying shortly
    after succeeds.
    """

    description: t.Final = (
        "Unable to find the deal to execute the requested operation on."
    )
    error_code: t.Final = "error.service.execution.find"


class PositionNotionalDetailsNullError(APIError):
    """Unable to compute a position's notional (market value) details.

    Maps to the
    ``error.service.marketdata.position.notional.details.null.error`` IG API
    error code. Like :class:`.DealExecutionNotFoundError`, this one isn't
    documented by IG; the description is inferred from its name and observed
    behaviour. It has been seen when closing a position immediately after its
    creation was confirmed, seemingly a brief propagation delay before the
    position's market data is fully populated rather than the position
    genuinely being invalid, since retrying shortly after succeeds.
    """

    description: t.Final = (
        "Unable to compute a position's notional (market value) details."
    )
    error_code: t.Final = (
        "error.service.marketdata.position.notional.details.null.error"
    )


class SessionAuthenticationFailureError(APIError):
    """Session authentication failed due to an invalid client security token.

    Maps to the
    ``service.security.authentication.failure-invalid-client-security-token``
    IG API error code. Like :class:`.DealExecutionNotFoundError`, this one
    isn't documented by IG; the description is inferred from its name and
    observed behaviour. It has been seen creating a session (even with no prior
    CST/security token/account ID/bearer token attached to the request) shortly
    after another session was created in quick succession, seemingly a
    transient session-management issue on IG's side rather than the request
    genuinely carrying an invalid token, since retrying shortly after succeeds.
    """

    description: t.Final = (
        "Session authentication failed due to an invalid client security "
        "token."
    )
    error_code: t.Final = (
        "service.security.authentication.failure-invalid-client-security-token"
    )


class DealNotFoundError(APIError):
    """Deal confirmation not found.

    Maps to the ``error.confirms.deal-not-found`` IG API error code.
    """

    description: t.Final = "Deal confirmation not found."
    error_code: t.Final = "error.confirms.deal-not-found"


class EndpointUnavailableForAPIKeyError(APIError):
    """The provided api key was not accepted.

    Maps to the ``endpoint.unavailable.for.api-key`` IG API error code.
    """

    description: t.Final = "The provided api key was not accepted."
    error_code: t.Final = "endpoint.unavailable.for.api-key"


class MalformedDateError(APIError):
    """Invalid date format error.

    Maps to the ``error.malformed.date`` IG API error code.
    """

    description: t.Final = "Invalid date format error."
    error_code: t.Final = "error.malformed.date"


class InvalidDateRangeError(APIError):
    """Invalid date range.

    Maps to the ``error.request.invalid.date-range`` IG API error code.
    """

    description: t.Final = "Invalid date range."
    error_code: t.Final = "error.request.invalid.date-range"


class ExceededAccountAllowanceError(APIError):
    """The account traffic allowance has been exceeded.

    Maps to the ``error.public-api.exceeded-account-allowance`` IG API error
    code.
    """

    description: t.Final = "The account traffic allowance has been exceeded."
    error_code: t.Final = "error.public-api.exceeded-account-allowance"


class ExceededAccountHistoricalDataAllowanceError(APIError):
    """The account historical data traffic allowance has been exceeded.

    Maps to the ``error.public-api.exceeded-account-historical-data-allowance``
    IG API error code.
    """

    description: t.Final = (
        "The account historical data traffic allowance has been exceeded."
    )
    error_code: t.Final = (
        "error.public-api.exceeded-account-historical-data-allowance"
    )


class ExceededAccountTradingAllowanceError(APIError):
    """The account trading traffic allowance has been exceeded.

    Maps to the ``error.public-api.exceeded-account-trading-allowance`` IG API
    error code.
    """

    description: t.Final = (
        "The account trading traffic allowance has been exceeded."
    )
    error_code: t.Final = "error.public-api.exceeded-account-trading-allowance"


class ExceededAPIKeyAllowanceError(APIError):
    """The api key traffic allowance has been exceeded.

    Maps to the ``error.public-api.exceeded-api-key-allowance`` IG API error
    code.
    """

    description: t.Final = "The api key traffic allowance has been exceeded."
    error_code: t.Final = "error.public-api.exceeded-api-key-allowance"


class KYCRequiredError(APIError):
    """The account is not allowed to log into public API.

    Please use the web platform.

    Maps to the ``error.public-api.failure.kyc.required`` IG API error code.
    """

    description: t.Final = (
        "The account is not allowed to log into public API. Please use the "
        "web platform."
    )
    error_code: t.Final = "error.public-api.failure.kyc.required"


class MissingCredentialsError(APIError):
    """The user has not provided all required security credentials.

    Maps to the ``error.public-api.failure.missing.credentials`` IG API error
    code.
    """

    description: t.Final = (
        "The user has not provided all required security credentials."
    )
    error_code: t.Final = "error.public-api.failure.missing.credentials"


class PendingAgreementsRequiredError(APIError):
    """The account is not allowed to log into public API.

    Please use the web platform.

    Maps to the ``error.public-api.failure.pending.agreements.required`` IG
    API error code.
    """

    description: t.Final = (
        "The account is not allowed to log into public API. Please use the "
        "web platform."
    )
    error_code: t.Final = (
        "error.public-api.failure.pending.agreements.required"
    )


class InvalidRequestError(APIError):
    """Invalid request.

    Maps to the ``invalid request`` IG API error code.
    """

    description: t.Final = "Invalid request."
    error_code: t.Final = "invalid request"


class NotNoneConditionalRequestError(APIError):
    """Not null conditional in request.

    Maps to the ``validation.not-null-conditional.request`` IG API error code.
    """

    description: t.Final = "Not null conditional in request."
    error_code: t.Final = "validation.not-null-conditional.request"


class NotNoneConditionalSetValueRequestError(APIError):
    """Not null conditional set value in request.

    Maps to the ``validation.not-null-conditional-set-value.request`` IG API
    error code.
    """

    description: t.Final = "Not null conditional set value in request."
    error_code: t.Final = "validation.not-null-conditional-set-value.request"


class NoneConditionalSetValueRequestError(APIError):
    """Null conditional set value in request.

    Maps to the ``validation.null-conditional-set-value.request`` IG API error
    code.
    """

    description: t.Final = "Null conditional set value in request."
    error_code: t.Final = "validation.null-conditional-set-value.request"


class NoCompatiblePositionFoundError(APIError):
    """Unable to aggregate close positions - no compatible position found.

    Maps to the ``unable to aggregate close positions - no compatible position
    found`` IG API error code.
    """

    description: t.Final = (
        "Unable to aggregate close positions - no compatible position found."
    )
    error_code: t.Final = (
        "unable to aggregate close positions - no compatible position found"
    )


class PreferredAccountDisabledError(APIError):
    """The user's preferred account is disabled.

    Maps to the ``error.public-api.failure.preferred.account.disabled`` IG API
    error code.
    """

    description: t.Final = "The user's preferred account is disabled."
    error_code: t.Final = "error.public-api.failure.preferred.account.disabled"


class PreferredAccountNotSetError(APIError):
    """The user has not set a preferred account.

    Maps to the ``error.public-api.failure.preferred.account.not.set`` IG API
    error code.
    """

    description: t.Final = "The user has not set a preferred account."
    error_code: t.Final = "error.public-api.failure.preferred.account.not.set"


class StockbrokingNotSupportedError(APIError):
    """Stockbroking not supported for Public API users.

    Maps to the ``error.public-api.failure.stockbroking-not-supported`` IG API
    error code.
    """

    description: t.Final = "Stockbroking not supported for Public API users."
    error_code: t.Final = "error.public-api.failure.stockbroking-not-supported"


class AccountNotYetActivatedError(APIError):
    """The account has not been activated yet.

    Maps to the ``error.security.account-not-yet-activated`` IG API error code.
    """

    description: t.Final = "The account has not been activated yet."
    error_code: t.Final = "error.security.account-not-yet-activated"


class AccountSuspendedError(APIError):
    """The account has been suspended.

    Maps to the ``error.security.account-suspended`` IG API error code.
    """

    description: t.Final = "The account has been suspended."
    error_code: t.Final = "error.security.account-suspended"


class AccountTokenInvalidError(APIError):
    """The provided account token is not valid.

    The service requires an account token and the one provided was not valid.

    Maps to the ``error.security.account-token-invalid`` IG API error code.
    """

    description: t.Final = (
        "The service requires an account token and the one provided was not "
        "valid."
    )
    error_code: t.Final = "error.security.account-token-invalid"


class AccountTokenMissingError(APIError):
    """The service requires an account token and it was not provided.

    Maps to the ``error.security.account-token-missing`` IG API error code.
    """

    description: t.Final = (
        "The service requires an account token and it was not provided."
    )
    error_code: t.Final = "error.security.account-token-missing"


class APIKeyDisabledError(APIError):
    """The provided api key is not currently enabled.

    The provided api key was not accepted because it is not currently enabled.

    Maps to the ``error.security.api-key-disabled`` IG API error code.
    """

    description: t.Final = (
        "The provided api key was not accepted because it is not currently "
        "enabled."
    )
    error_code: t.Final = "error.security.api-key-disabled"


class APIKeyInvalidError(APIError):
    """The provided api key was not accepted.

    Maps to the ``error.security.api-key-invalid`` IG API error code.
    """

    description: t.Final = "The provided api key was not accepted."
    error_code: t.Final = "error.security.api-key-invalid"


class APIKeyMissingError(APIError):
    """The api key was not provided.

    Maps to the ``error.security.api-key-missing`` IG API error code.
    """

    description: t.Final = "The api key was not provided."
    error_code: t.Final = "error.security.api-key-missing"


class APIKeyRestrictedError(APIError):
    """The provided api key was not valid for the requesting account.

    Maps to the ``error.security.api-key-restricted`` IG API error code.
    """

    description: t.Final = (
        "The provided api key was not valid for the requesting account."
    )
    error_code: t.Final = "error.security.api-key-restricted"


class APIKeyRevokedError(APIError):
    """The provided api key was not accepted because it has been revoked.

    Maps to the ``error.security.api-key-revoked`` IG API error code.
    """

    description: t.Final = (
        "The provided api key was not accepted because it has been revoked."
    )
    error_code: t.Final = "error.security.api-key-revoked"


class ClientSuspendedError(APIError):
    """The client has been suspended from using the platform.

    Maps to the ``error.security.client-suspended`` IG API error code.
    """

    description: t.Final = (
        "The client has been suspended from using the platform."
    )
    error_code: t.Final = "error.security.client-suspended"


class ClientTokenInvalidError(APIError):
    """The service requires a client token and the one provided was not valid.

    Maps to the ``error.security.client-token-invalid`` IG API error code.
    """

    description: t.Final = (
        "The service requires a client token and the one provided was not "
        "valid."
    )
    error_code: t.Final = "error.security.client-token-invalid"


class ClientTokenMissingError(APIError):
    """The service requires a client token and it was not provided.

    Maps to the ``error.security.client-token-missing`` IG API error code.
    """

    description: t.Final = (
        "The service requires a client token and it was not provided."
    )
    error_code: t.Final = "error.security.client-token-missing"


class GenericError(APIError):
    """An unexpected server-side error occurred; please contact support.

    An unexpected error has been encountered on the server side, cannot
    proceed. Please contact the support.

    Maps to the ``error.security.generic`` IG API error code.
    """

    description: t.Final = (
        "An unexpected error has been encountered on the server side, cannot "
        "proceed. Please contact the support."
    )
    error_code: t.Final = "error.security.generic"


class GetSessionTimeoutError(APIError):
    """Request timed out while retrieving session details.

    Maps to the ``error.security.get.session.timeout`` IG API error code.
    """

    description: t.Final = (
        "Request timed out while retrieving session details."
    )
    error_code: t.Final = "error.security.get.session.timeout"


class InvalidDetailsError(APIError):
    """The provided credentials are not valid.

    The credentials used to authenticate the users are not valid, login is
    rejected.

    Maps to the ``error.security.invalid-details`` IG API error code.
    """

    description = (
        "The credentials used to authenticate the users are not valid, login "
        "is rejected."
    )
    error_code: t.Final = "error.security.invalid-details"


class InvalidWebsiteError(APIError):
    """This site is not accessible via the API services.

    Maps to the ``error.security.invalid-website`` IG API error code.
    """

    description: t.Final = "This site is not accessible via the API services."
    error_code: t.Final = "error.security.invalid-website"


class OAuthTokenInvalidError(APIError):
    """Invalid OAuth access token.

    Maps to the ``error.security.oauth-token-invalid`` IG API error code.
    """

    description: t.Final = "Invalid OAuth access token."
    error_code: t.Final = "error.security.oauth-token-invalid"


class AccountIDMustBeDifferentError(APIError):
    """A switch to the current account was attempted.

    Maps to the ``error.switch.accountId-must-be-different`` IG API error code.
    """

    description: t.Final = "A switch to the current account was attempted."
    error_code: t.Final = "error.switch.accountId-must-be-different"


class AccountAccessDeniedError(APIError):
    """The account has been denied login privileges.

    Maps to the ``error.client.account.switch.account-access-denied`` IG API
    error code.
    """

    description: t.Final = "The account has been denied login privileges."
    error_code: t.Final = "error.client.account.switch.account-access-denied"


class InvalidAccountIDError(APIError):
    """A switch to an invalid account id was attempted.

    Maps to the ``error.switch.invalid-accountId`` IG API error code.
    """

    description: t.Final = "A switch to an invalid account id was attempted."
    error_code: t.Final = "error.switch.invalid-accountId"


class InvalidApplicationError(APIError):
    """The provided user agent string is not valid.

    Maps to the ``error.security.invalid-application`` IG API error code.
    """

    description: t.Final = "The provided user agent string is not valid."
    error_code: t.Final = "error.security.invalid-application"


class InvalidInputError(APIError):
    """A generic input data error has occurred.

    Maps to the ``invalid.input`` IG API error code.
    """

    description: t.Final = "A generic input data error has occurred."
    error_code: t.Final = "invalid.input"


class InvalidCurrencyCodeError(APIError):
    """Invalid currency code.

    Maps to the ``validation.pattern.invalid.request.currencyCode`` IG API
    error code.
    """

    description: t.Final = "Invalid currency code."
    error_code: t.Final = "validation.pattern.invalid.request.currencyCode"


class InvalidDirectionError(APIError):
    """Invalid direction.

    Maps to the ``invalid.request.direction`` IG API error code.
    """

    description: t.Final = "Invalid direction."
    error_code: t.Final = "invalid.request.direction"


class InvalidExpiryError(APIError):
    """Invalid expiry.

    Maps to the ``validation.pattern.invalid.request.expiry`` IG API error
    code.
    """

    description: t.Final = "Invalid expiry."
    error_code: t.Final = "validation.pattern.invalid.request.expiry"


class InvalidLevelError(APIError):
    """Invalid level.

    Maps to the ``invalid.request.level`` IG API error code.
    """

    description: t.Final = "Invalid level."
    error_code: t.Final = "invalid.request.level"


class InvalidInstrumentError(APIError):
    """Invalid instrument/epic.

    Maps to the ``error.service.create.otc.position.instrument.invalid`` IG API
    error code.
    """

    description: t.Final = "Invalid instrument/epic."
    error_code: t.Final = (
        "error.service.create.otc.position.instrument.invalid"
    )


class InvalidOrderTypeError(APIError):
    """Invalid order type.

    Maps to the ``invalid.request.orderType`` IG API error code.
    """

    description: t.Final = "Invalid order type."
    error_code: t.Final = "invalid.request.orderType"


class InvalidSizeError(APIError):
    """Invalid size.

    Maps to the ``invalid.request.size`` IG API error code.
    """

    description: t.Final = "Invalid size."
    error_code: t.Final = "invalid.request.size"


class MutualExclusiveValueError(APIError):
    """Mutually exclusive value in request.

    Maps to the ``validation.mutual-exclusive-value.request`` IG API error
    code.
    """

    description: t.Final = "Mutually exclusive value in request."
    error_code: t.Final = "validation.mutual-exclusive-value.request"


class ExpiryNoneNotAllowedError(APIError):
    """Expiry must not be None.

    Maps to the ``validation.null-not-allowed.request.expiry`` IG API error
    code.
    """

    description: t.Final = "Expiry must not be None."
    error_code: t.Final = "validation.null-not-allowed.request.expiry"


class TargetValueConditionalSetValueError(APIError):
    """Target value conditional set value in request.

    Maps to the ``validation.target-value-conditional-set-value.request`` IG
    API error code.
    """

    description: t.Final = "Target value conditional set value in request."
    error_code: t.Final = (
        "validation.target-value-conditional-set-value.request"
    )


class OneSelectionRequiredRequestError(APIError):
    """One selection required in request.

    Maps to the ``validation.one-selection-required.request`` IG API error
    code.
    """

    description: t.Final = "One selection required in request."
    error_code: t.Final = "validation.one-selection-required.request"


class RequestNoneNotAllowedError(APIError):
    """Request must not be None.

    Maps to the ``validation.null-not-allowed.request`` IG API error code.
    """

    description: t.Final = "Request must not be None."
    error_code: t.Final = "validation.null-not-allowed.request"


class ForceOpenNoneNotAllowedError(APIError):
    """Force open must not be None.

    Maps to the ``validation.null-not-allowed.request.forceOpen`` IG API error
    code.
    """

    description: t.Final = "Force open must not be None."
    error_code: t.Final = "validation.null-not-allowed.request.forceOpen"


class GuaranteedStopNoneNotAllowedError(APIError):
    """Guaranteed stop must not be None.

    Maps to the ``validation.null-not-allowed.request.guaranteedStop`` IG API
    error code.
    """

    description: t.Final = "Guaranteed stop must not be None."
    error_code: t.Final = "validation.null-not-allowed.request.guaranteedStop"


class UnauthorisedAccessToEquityDataError(APIError):
    """Unauthorised access to equity data.

    Maps to the ``unauthorised.access.to.equity.exception`` IG API error code.
    """

    description: t.Final = "Unauthorised access to equity data."
    error_code: t.Final = "unauthorised.access.to.equity.exception"


class PriceHistoryIOError(APIError):
    """Price history IO error.

    Maps to the ``error.price-history.io-error`` IG API error code.
    """

    description: t.Final = "Price history IO error."
    error_code: t.Final = "error.price-history.io-error"
