from __future__ import annotations

from unittest import mock

import pytest

from _ig_trading import env


@pytest.fixture(autouse=True)
def _no_dotenv_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        env.dotenv, "dotenv_values", mock.Mock(return_value={})
    )


def test_get_api_key_given_environment_variable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(env.API_KEY, "from-environ")
    assert env.get_api_key() == "from-environ"


def test_get_identifier_given_dotenv_file(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(env.IDENTIFIER, raising=False)
    monkeypatch.setattr(
        env.dotenv,
        "dotenv_values",
        mock.Mock(return_value={env.IDENTIFIER: "from-dotenv"}),
    )
    assert env.get_identifier() == "from-dotenv"


def test_get_password_given_environment_variable_takes_precedence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(env.PASSWORD, "from-environ")
    monkeypatch.setattr(
        env.dotenv,
        "dotenv_values",
        mock.Mock(return_value={env.PASSWORD: "from-dotenv"}),
    )
    assert env.get_password() == "from-environ"


def test_get_password_given_neither_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(env.PASSWORD, raising=False)
    with pytest.raises(KeyError):
        env.get_password()
