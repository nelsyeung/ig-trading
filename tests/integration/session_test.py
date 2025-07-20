from __future__ import annotations

import pytest
import typing_extensions as t

import ig_trading as ig


@pytest.fixture
def async_session(
    async_requester: ig.AsyncAPIRequester,
) -> ig.AsyncSessionResource:
    return ig.AsyncSessionResource(async_requester)


@pytest.fixture
def session(requester: ig.APIRequester) -> ig.SessionResource:
    return ig.SessionResource(requester)


@pytest.fixture
def isolated_async_session() -> ig.AsyncSessionResource:
    # `create()` clears whatever identity (account ID, bearer token, CST,
    # security token) its requester already holds before logging in, since IG
    # rejects a login that carries a stale one. Tests that call `create()`
    # therefore need their own requester rather than the shared, already
    # logged-in `async_requester`/`async_session`, or they'd log the rest of
    # the suite out.
    return ig.AsyncSessionResource(ig.AsyncAPIRequester())


@pytest.fixture
def isolated_session() -> ig.SessionResource:
    # See `isolated_async_session` above.
    return ig.SessionResource(ig.APIRequester())


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.session.v1.AccountSummary),
        (2, ig.session.v2.AccountSummary),
        (3, ig.session.v3.AccountSummary),
    ],
    ids=("v1", "v2", "v3"),
)
async def test_async_create(
    isolated_async_session: ig.AsyncSessionResource,
    expected: type,
    version: t.Literal[1, 2, 3],
) -> None:
    assert isinstance(
        await isolated_async_session.create(version=version), expected
    )


async def test_async_create_with_wrong_account(
    isolated_async_session: ig.AsyncSessionResource,
) -> None:
    with pytest.raises(ig.InvalidDetailsError):
        await isolated_async_session.create(identifier="foo")


async def test_async_create_with_wrong_password(
    isolated_async_session: ig.AsyncSessionResource,
) -> None:
    with pytest.raises(ig.InvalidDetailsError):
        await isolated_async_session.create(password="foo")


async def test_async_delete(async_session: ig.AsyncSessionResource) -> None:
    await async_session.delete()
    await async_session.get()


async def test_async_delete_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        await ig.AsyncSessionResource().delete()


async def test_async_get(async_session: ig.AsyncSessionResource) -> None:
    assert isinstance(await async_session.get(), ig.session.v1.Session)


async def test_async_update_to_wrong_account(
    async_session: ig.AsyncSessionResource,
) -> None:
    with pytest.raises(ig.AccountAccessDeniedError):
        await async_session.update("foo", default_account=False)


async def test_async_wrong_api_key() -> None:
    with pytest.raises(ig.APIKeyInvalidError):
        await ig.AsyncSessionResource(ig.AsyncAPIRequester(key="foo")).create()


async def test_async_encryption_key_get(
    async_session: ig.AsyncSessionResource,
) -> None:
    assert isinstance(
        await async_session.encryption_key.get(),
        ig.session.v1.EncryptionKey,
    )


async def test_async_refresh_token_create(
    isolated_async_session: ig.AsyncSessionResource,
) -> None:
    account: t.Final = await isolated_async_session.create()
    assert isinstance(
        await isolated_async_session.refresh_token.create(
            account.oauth_token.refresh_token
        ),
        ig.session.v1.OAuthToken,
    )


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        (1, ig.session.v1.AccountSummary),
        (2, ig.session.v2.AccountSummary),
        (3, ig.session.v3.AccountSummary),
    ],
    ids=("v1", "v2", "v3"),
)
def test_create(
    expected: type,
    isolated_session: ig.SessionResource,
    version: t.Literal[1, 2, 3],
) -> None:
    assert isinstance(isolated_session.create(version=version), expected)


def test_create_with_wrong_account(
    isolated_session: ig.SessionResource,
) -> None:
    with pytest.raises(ig.InvalidDetailsError):
        isolated_session.create(identifier="foo")


def test_create_with_wrong_password(
    isolated_session: ig.SessionResource,
) -> None:
    with pytest.raises(ig.InvalidDetailsError):
        isolated_session.create(password="foo")


def test_delete(session: ig.SessionResource) -> None:
    session.delete()
    session.get()


def test_delete_given_not_logged_in() -> None:
    with pytest.raises(ig.ClientTokenMissingError):
        ig.SessionResource().delete()


def test_get(session: ig.SessionResource) -> None:
    assert isinstance(session.get(), ig.session.v1.Session)


def test_update_to_wrong_account(session: ig.SessionResource) -> None:
    with pytest.raises(ig.AccountAccessDeniedError):
        session.update("foo", default_account=False)


def test_wrong_api_key() -> None:
    with pytest.raises(ig.APIKeyInvalidError):
        ig.SessionResource(ig.APIRequester(key="foo")).create()


def test_encryption_key_get(session: ig.SessionResource) -> None:
    assert isinstance(
        session.encryption_key.get(),
        ig.session.v1.EncryptionKey,
    )


def test_refresh_token_create(isolated_session: ig.SessionResource) -> None:
    account: t.Final = isolated_session.create()
    assert isinstance(
        isolated_session.refresh_token.create(
            account.oauth_token.refresh_token
        ),
        ig.session.v1.OAuthToken,
    )
