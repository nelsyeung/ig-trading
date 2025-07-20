from __future__ import annotations

import typing_extensions as t

import ig_trading as ig


def test_from_error_code_given_known_code() -> None:
    status: t.Final = 404
    error: t.Final = ig.APIError.from_error_code(
        "error.confirms.deal-not-found", status=status
    )
    assert isinstance(error, ig.DealNotFoundError)
    assert error.status == status
    assert error.error_code == "error.confirms.deal-not-found"
    assert error.description == "Deal confirmation not found."


def test_from_error_code_given_unknown_code() -> None:
    assert ig.APIError.from_error_code("some.unknown.code", status=500) is None


def test_str_includes_status_error_code_and_description() -> None:
    assert str(ig.OAuthTokenInvalidError(status=401)) == (
        "401 [error.security.oauth-token-invalid] Invalid OAuth access token."
    )


def test_unknown_api_error() -> None:
    status: t.Final = 500
    e: t.Final = ig.UnknownAPIError(
        description="Something went wrong.",
        error_code="_unknown",
        status=status,
    )
    assert e.description == "Something went wrong."
    assert e.error_code == "_unknown"
    assert e.status == status
