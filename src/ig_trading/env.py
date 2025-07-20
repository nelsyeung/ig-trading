"""Environment variables.

Attributes:
    API_KEY (typing.Final[typing.Literal["IG_API_KEY"]]): API key environment
        variable name.
    IDENTIFIER (typing.Final[typing.Literal["IG_IDENTIFIER"]]): Identifier
        environment variable name.
    PASSWORD (typing.Final[typing.Literal["IG_PASSWORD"]]): Password
        environment variable name.
"""

from _ig_trading.env import (
    API_KEY,
    IDENTIFIER,
    PASSWORD,
    get_api_key,
    get_identifier,
    get_password,
)

__all__ = (
    "API_KEY",
    "IDENTIFIER",
    "PASSWORD",
    "get_api_key",
    "get_identifier",
    "get_password",
)
