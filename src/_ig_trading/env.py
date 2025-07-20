from __future__ import annotations

import os

import dotenv
import typing_extensions as t

API_KEY: t.Final = "IG_API_KEY"
IDENTIFIER: t.Final = "IG_IDENTIFIER"
PASSWORD: t.Final = "IG_PASSWORD"  # noqa: S105


def get_api_key() -> str:
    """The API key, from ``IG_API_KEY`` or a ``.env`` file."""
    return _get_value(API_KEY)


def get_identifier() -> str:
    """The identifier, from ``IG_IDENTIFIER`` or a ``.env`` file."""
    return _get_value(IDENTIFIER)


def get_password() -> str:
    """The password, from ``IG_PASSWORD`` or a ``.env`` file."""
    return _get_value(PASSWORD)


def _get_value(key: str, /) -> str:
    if v := os.environ.get(key):
        return v
    if v := dotenv.dotenv_values().get(key):
        return v
    raise KeyError(key)
