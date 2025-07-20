# 📈 IG trading

![PyPI Python Version](https://img.shields.io/pypi/pyversions/ig-trading)
[![CI](https://github.com/nelsyeung/ig-trading/actions/workflows/ci.yml/badge.svg)](https://github.com/nelsyeung/ig-trading/actions/workflows/ci.yml)

A fully-typed Python client for [IG](https://www.ig.com/)'s trading REST API,
with both an async and a sync API.

## 🚀 Usage

```python
import asyncio

import ig_trading as ig


async def main() -> None:
    async with ig.AsyncClient() as client:
        # Credentials default to the IG_API_KEY, IG_IDENTIFIER and IG_PASSWORD
        # environment variables if not passed explicitly.
        positions = await client.positions.list()
        for position in positions:
            print(position.position.deal_id, position.market.epic)

        deal_reference = await client.positions.otc.create(
            currency_code="GBP",
            direction="BUY",
            epic="CS.D.EURGBP.CFD.IP",
            expiry="-",
            force_open=True,
            guaranteed_stop=False,
            order_type="MARKET",
            size=1,
        )
        print((await client.confirms.get(deal_reference)).reason)


asyncio.run(main())
```

`ig.Client` is the sync equivalent (built on
[`requests`](https://requests.readthedocs.io/) instead of
[`aiohttp`](https://docs.aiohttp.org/)), with the same API minus `await`:

```python
import ig_trading as ig


def main() -> None:
    with ig.Client() as client:
        positions = client.positions.list()
        for position in positions:
            print(position.position.deal_id, position.market.epic)

        deal_reference = client.positions.otc.create(
            currency_code="GBP",
            direction="BUY",
            epic="CS.D.EURGBP.CFD.IP",
            expiry="-",
            force_open=True,
            guaranteed_stop=False,
            order_type="MARKET",
            size=1,
        )
        print(client.confirms.get(deal_reference).reason)


main()
```

Every `Async`-prefixed class (`AsyncClient`, `AsyncAccountsResource`, ...) has a
sync counterpart with the same name minus the prefix (`Client`,
`AccountsResource`, ...) and an identical API.

Each resource on `client` (`accounts`, `application`, `categories`,
`client_sentiment`, `confirms`, `history`, `markets`, `positions`, `prices`,
`session`, `watchlists`, `working_orders`) can also be used standalone with your
own `aiohttp.ClientSession`/`requests.Session`, e.g. for testing or for
composing your own login flow:

```python
async with ig.AsyncSession() as http_session:
    requester = ig.AsyncAPIRequester(http_session=http_session, key="...")
    session = ig.AsyncSessionResource(requester)
    account = await session.create(identifier="...", password="...")
```

```python
with ig.Session() as http_session:
    requester = ig.APIRequester(http_session=http_session, key="...")
    session = ig.SessionResource(requester)
    account = session.create(identifier="...", password="...")
```

### 🔑 Environment variables

| Variable        | Description |
| --------------- | ----------- |
| `IG_API_KEY`    | API key     |
| `IG_IDENTIFIER` | Username    |
| `IG_PASSWORD`   | Password    |

These can be set directly or via a `.env` file in the working directory.

## 💡 Why

The existing IG API clients on PyPI/GitHub are, for the most part, only
partially typed and expose the API as a flat grab-bag of methods. This project
exists because none of the popular, actively-maintained alternatives (e.g.
[`trading-ig`](https://github.com/ig-python/trading-ig), the most widely used
one) offer all of the following together:

- **Fully typed.** Every request and response is a
  [pydantic](https://docs.pydantic.dev/) model, so responses are validated at
  the boundary and you get real autocomplete/type-checking instead of dicts of
  `Any`.
- **Async and sync.** `AsyncClient` is built on
  [`aiohttp`](https://docs.aiohttp.org/) and `Client` on
  [`requests`](https://requests.readthedocs.io/), each with a background
  task/thread that automatically refreshes the OAuth token before it expires, so
  you don't have to babysit sessions.
- **Clean, resource-oriented usage.** The client is organised as typed
  sub-resources that mirror the shape of the API itself (`client.positions`,
  `client.markets`, `client.working_orders`, ...) rather than one flat object
  with dozens of loosely related methods bolted on.

A couple of other things fell out of that design along the way:

- The library mirrors IG's own API versioning (`v1`, `v2`, `v3`, ...) with a
  matching submodule for each version, so it's clear exactly which version of an
  endpoint/model you're using.
- Errors are typed too: IG's error codes are mapped to specific exception
  classes (e.g. `ExceededAPIKeyAllowanceError`, `OAuthTokenInvalidError`)
  instead of a single generic HTTP error.

## 🛠️ Development

The dev environment is a Docker container with everything needed (`uv`, Python,
Vim, Claude Code) pre-installed. Start it with:

```sh
docker compose run --build --interactive --remove-orphans --rm vim
```

This mounts the repo into the container and drops you into a shell with the
`.venv` already synced (`uv sync` has run as part of the image build).

From there:

```sh
# Run the test suite. Tests hit IG's real demo API (no mocking), so this
# needs IG_API_KEY, IG_IDENTIFIER and IG_PASSWORD set, e.g. via .env.
uv run pytest

# Lint and type-check.
uv run ruff check
uv run mypy .

# Build the docs; output goes to docs/_build/html.
uv run sphinx-build docs public
```

If you don't want to use the container, the same commands work locally as long
as you have `uv` installed — just run `uv sync` first.
