from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig


async def test_async_client() -> None:
    async with ig.AsyncSession() as http_session:
        client: t.Final = ig.AsyncClient(http_session=http_session)
        async with client:
            assert isinstance(
                await client.session.get(), ig.session.v1.Session
            )
        with pytest.raises(ig.ClientTokenMissingError):
            assert await client.session.get()


def test_client() -> None:
    with ig.Session() as http_session:
        client: t.Final = ig.Client(http_session=http_session)
        with client:
            assert isinstance(client.session.get(), ig.session.v1.Session)
        with pytest.raises(ig.ClientTokenMissingError):
            assert client.session.get()
