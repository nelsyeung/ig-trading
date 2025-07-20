IG Trading documentation
========================

A fully-typed Python client for `IG <https://www.ig.com/>`_'s trading REST API,
with both an async and a sync API.

.. toctree::
   :hidden:

Usage
-----

:class:`~ig_trading.AsyncClient` is an async context manager: entering it logs
in and starts a background task that keeps the OAuth token refreshed, and
leaving it logs out again.

.. code-block:: python

   import asyncio

   import ig_trading as ig


   async def main() -> None:
       async with ig.AsyncClient() as client:
           # Credentials default to the IG_API_KEY, IG_IDENTIFIER and
           # IG_PASSWORD environment variables if not passed explicitly.
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

Every argument and every field on the returned objects is typed, so
``position.position.deal_id`` and ``position.market.epic`` above are plain
attribute access, not dictionary lookups, and your editor/type checker
knows their types.

:class:`~ig_trading.Client` is the sync equivalent, built on `requests
<https://requests.readthedocs.io/>`_ instead of `aiohttp
<https://docs.aiohttp.org/>`_: it's a regular (non-async) context manager, and
the background OAuth refresh runs on a daemon thread instead of an
:mod:`asyncio` task.

.. code-block:: python

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

Every ``Async``-prefixed class in this documentation
(:class:`~ig_trading.AsyncClient`, :class:`~ig_trading.AsyncAccountsResource`,
...) has a sync counterpart with the same name minus the prefix
(:class:`~ig_trading.Client`, :class:`~ig_trading.AccountsResource`, ...), with
an identical API.

.. _a-resource-oriented-client:

A resource-oriented client
~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`~ig_trading.AsyncClient` doesn't expose the API as one flat list of
methods. Instead it exposes one attribute per resource, and each resource groups
the operations that belong to it, mirroring the shape of `IG's own REST API
<https://labs.ig.com/rest-trading-api-reference.html>`_:

.. list-table::
   :header-rows: 1

   * - Attribute
     - Resource
   * - ``client.accounts``
     - :class:`~ig_trading.AsyncAccountsResource`
   * - ``client.application``
     - :class:`~ig_trading.AsyncApplicationResource`
   * - ``client.categories``
     - :class:`~ig_trading.AsyncCategoriesResource`
   * - ``client.client_sentiment``
     - :class:`~ig_trading.AsyncClientSentimentResource`
   * - ``client.confirms``
     - :class:`~ig_trading.AsyncConfirmsResource`
   * - ``client.history``
     - :class:`~ig_trading.AsyncHistoryResource`
   * - ``client.markets``
     - :class:`~ig_trading.AsyncMarketsResource`
   * - ``client.positions``
     - :class:`~ig_trading.AsyncPositionsResource`
   * - ``client.prices``
     - :class:`~ig_trading.AsyncPricesResource`
   * - ``client.session``
     - :class:`~ig_trading.AsyncSessionResource`
   * - ``client.watchlists``
     - :class:`~ig_trading.AsyncWatchlistsResource`
   * - ``client.working_orders``
     - :class:`~ig_trading.AsyncWorkingOrdersResource`

Where IG's API nests further (e.g. working orders have an "OTC" sub-group), the
client nests too, e.g. ``client.positions.otc.create(...)``.

Each of these resources can also be constructed and used on its own, e.g. to
compose your own login flow, or to call a single endpoint in a script or a test,
without going through :class:`~ig_trading.AsyncClient`:

.. code-block:: python

   async with ig.AsyncSession() as http_session:
       requester = ig.AsyncAPIRequester(http_session=http_session, key="...")
       session = ig.AsyncSessionResource(requester)
       account = await session.create(identifier="...", password="...")

The same applies to the sync resources, using :class:`~ig_trading.Session`
(a plain :class:`requests.Session`) instead:

.. code-block:: python

   with ig.Session() as http_session:
       requester = ig.APIRequester(http_session=http_session, key="...")
       session = ig.SessionResource(requester)
       account = session.create(identifier="...", password="...")

.. _api-versioning:

API versioning
~~~~~~~~~~~~~~~

IG versions individual endpoints independently (e.g. markets go up to ``v4``
while sessions only go up to ``v3``). ``ig_trading`` mirrors that directly: each
resource module has a submodule per API version it supports
(``ig_trading.positions.v2``, ``ig_trading.session.v1``,
``ig_trading.session.v3``, ...), each with its own request/response models.
Where two versions share an identical schema, the newer submodule simply
re-exports the older one, so you can always import the version you mean and know
exactly which shape of data you're getting.

Environment variables
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - Variable
     - Description
   * - ``IG_API_KEY``
     - API key
   * - ``IG_IDENTIFIER``
     - Username
   * - ``IG_PASSWORD``
     - Password

These can be set directly in the environment or via a ``.env`` file in the
working directory, and are picked up automatically by
:class:`~ig_trading.AsyncClient` (or :class:`~ig_trading.Client`) when
``api_key``, ``username`` or ``password`` aren't passed explicitly.

.. _error-handling:

Error handling
~~~~~~~~~~~~~~~

Errors IG's API returns are mapped to specific exception classes rather than
raised as a single generic HTTP error, so you can catch exactly the failure you
expect. Every one of them subclasses :class:`~ig_trading.APIError`:

.. code-block:: python

   try:
       await client.positions.otc.create(...)
   except ig.ExceededAccountTradingAllowanceError:
       ...
   except ig.APIError:
       # Catch-all for any other API error.
       ...

See the :ref:`API reference <api-reference>` below for the full list of
exception types.

Why this exists
----------------

The existing IG API clients on PyPI/GitHub are, for the most part, only
partially typed and expose the API as a flat grab-bag of methods. This project
exists because none of the popular, actively-maintained alternatives (e.g.
`trading-ig <https://github.com/ig-python/trading-ig>`_, the most widely used
one) offer all of the following together:

- **Fully typed.** Every request and response is a `pydantic
  <https://docs.pydantic.dev/>`_ model, so responses are validated at the
  boundary and you get real autocomplete and type-checking instead of
  dictionaries of ``Any``.
- **Async and sync.** :class:`~ig_trading.AsyncClient` is built on `aiohttp
  <https://docs.aiohttp.org/>`_ and :class:`~ig_trading.Client` on `requests
  <https://requests.readthedocs.io/>`_, each with a background task/thread that
  automatically refreshes the OAuth token before it expires, so you don't have
  to babysit sessions yourself.
- **Clean, resource-oriented usage.** The client is organised as typed
  sub-resources that mirror the shape of the API itself, as described in
  :ref:`a-resource-oriented-client` above, rather than one flat object with
  dozens of loosely related methods bolted on.

A couple of other things fell out of that design along the way:

- The library mirrors IG's own :ref:`api-versioning` with a matching submodule
  for each version, so it's always clear exactly which version of an
  endpoint/model you're using.
- :ref:`error-handling` is typed too: IG's error codes are mapped to specific
  exception classes rather than a single generic HTTP error.

Development
-----------

The dev environment is a Docker container with everything needed
(``uv``, Python, Vim, Claude Code) pre-installed. Start it with:

.. code-block:: shell

   docker compose run --build --interactive --remove-orphans --rm vim

This mounts the repository into the container and drops you into a shell
with the ``.venv`` already synced (``uv sync`` has run as part of the
image build).

From there:

.. code-block:: shell

   # Run the test suite. Tests hit IG's real demo API (no mocking), so this
   # needs IG_API_KEY, IG_IDENTIFIER and IG_PASSWORD set, e.g. via .env.
   uv run pytest

   # Lint and type-check.
   uv run ruff check
   uv run mypy .

   # Build these docs; output goes to public.
   uv run sphinx-build docs public

If you don't want to use the container, the same commands work locally as long
as you have ``uv`` installed — just run ``uv sync`` first.

.. _api-reference:

API reference
--------------

.. autosummary::
   :recursive:
   :toctree: _autosummary

   ig_trading
