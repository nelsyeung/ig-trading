from __future__ import annotations

import contextlib
import datetime as dt
import typing as t

import pydantic
import pydantic.alias_generators


class Model(pydantic.BaseModel):
    """Base class for all request and response models."""

    model_config = pydantic.ConfigDict(
        alias_generator=pydantic.alias_generators.to_camel,
        extra="forbid",
        frozen=True,
    )


def _to_datetime(v: object, /) -> object:
    if not isinstance(v, str):
        return v

    formats: t.Final = (
        "%Y:%m:%d-%H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S:%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    )
    for fmt in formats:
        with contextlib.suppress(ValueError):
            return dt.datetime.strptime(v, fmt).astimezone(dt.timezone.utc)

    err: t.Final = f"time data '{v}' does not match format {formats}"
    raise ValueError(err)


DateTime = t.Annotated[dt.datetime, pydantic.BeforeValidator(_to_datetime)]
