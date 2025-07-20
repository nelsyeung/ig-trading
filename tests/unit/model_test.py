from __future__ import annotations

import datetime as dt

import pydantic
import pytest
import typing_extensions as t

from _ig_trading.model import DateTime, Model


class _Example(Model):
    when: DateTime


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (
            "2024:01:02-03:04:05",
            dt.datetime(2024, 1, 2, 3, 4, 5, tzinfo=dt.timezone.utc),
        ),
        (
            "2024/01/02 03:04:05",
            dt.datetime(2024, 1, 2, 3, 4, 5, tzinfo=dt.timezone.utc),
        ),
        (
            "2024/01/02 03:04:05:678",
            dt.datetime(
                2024, 1, 2, 3, 4, 5, 678000, tzinfo=dt.timezone.utc
            ),
        ),
        (
            "2024-01-02T03:04:05",
            dt.datetime(2024, 1, 2, 3, 4, 5, tzinfo=dt.timezone.utc),
        ),
        (
            "2024-01-02T03:04:05.678",
            dt.datetime(
                2024, 1, 2, 3, 4, 5, 678000, tzinfo=dt.timezone.utc
            ),
        ),
    ],
)
def test_datetime_given_known_formats(raw: str, expected: dt.datetime) -> None:
    assert _Example.model_validate({"when": raw}).when == expected


def test_datetime_given_already_a_datetime() -> None:
    when: t.Final = dt.datetime(2024, 1, 2, tzinfo=dt.timezone.utc)
    assert _Example.model_validate({"when": when}).when == when


def test_datetime_given_unknown_format() -> None:
    with pytest.raises(pydantic.ValidationError):
        _Example.model_validate({"when": "not a date"})


def test_model_forbids_extra_fields() -> None:
    with pytest.raises(pydantic.ValidationError):
        _Example.model_validate(
            {"when": "2024-01-02T03:04:05", "extra": "field"}
        )


def test_model_is_frozen() -> None:
    example: t.Final = _Example.model_validate({"when": "2024-01-02T03:04:05"})

    with pytest.raises(pydantic.ValidationError):
        example.when = dt.datetime.now(dt.timezone.utc)


def test_model_uses_camel_case_aliases() -> None:
    class _CamelExample(Model):
        some_field: str

    assert _CamelExample.model_validate({"someField": "value"}).some_field == (
        "value"
    )
