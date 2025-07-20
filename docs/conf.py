"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from __future__ import annotations

import importlib
import importlib.metadata
import inspect
import pathlib
import typing as t

if t.TYPE_CHECKING:
    from collections.abc import Iterator
    from types import ModuleType

_this_path = pathlib.Path(__file__).resolve()


def _compute_external_alias_names(root_name: str, /) -> frozenset[str]:
    """Returns names in ``root_name``'s ``__all__`` for an external class.

    E.g. ``Session = requests.Session``, re-exported so callers can construct
    their own HTTP session. These aren't part of this project's own API, so
    documenting their full member list would render a third-party class's
    internals, including docstrings this project doesn't control and that can
    carry their own Sphinx warnings (as ``requests.Session``'s do).
    """
    root: t.Final = importlib.import_module(root_name)
    return frozenset(
        name
        for name in getattr(root, "__all__", ())
        if inspect.isclass(obj := getattr(root, name, None))
        and not (obj.__module__ or "").startswith(root_name)
    )


def _compute_noindex_pairs(root_name: str, /) -> frozenset[tuple[str, str]]:
    """Returns non-canonical ``(fullname, item)`` pairs under ``root_name``.

    Several ``ig_trading`` submodules re-export models defined (or already
    re-exported) elsewhere, to mirror API versions that share an identical
    schema (e.g. ``ig_trading.prices.v2`` is ``ig_trading.prices.v1`` under
    another name, and ``ig_trading.session.v3.OAuthToken`` is
    ``ig_trading.session.v1.OAuthToken``). Documenting the same object from
    every such page makes Sphinx register it more than once, which it warns
    about.

    Walks the whole public package tree once and returns the ``(fullname,
    item)`` pairs that are *not* the first (canonical) place a given object is
    documented; the autosummary module template renders those with
    ``:noindex:`` so they don't conflict. The result is a plain
    ``frozenset[tuple[str, str]]`` (rather than a function) so it can be passed
    through ``autosummary_context`` and still be pickled when Sphinx caches its
    build environment.
    """
    root: t.Final = importlib.import_module(root_name)
    seen: t.Final[set[str]] = set()
    noindex: t.Final[set[tuple[str, str]]] = set()

    for fullname, module in _walk_modules(root, root_name):
        for name in getattr(module, "__all__", ()):
            obj = getattr(module, name, None)

            if not inspect.isclass(obj):
                continue

            module_name = getattr(obj, "__module__", fullname)
            qualname = getattr(obj, "__qualname__", name)
            key = f"{module_name}.{qualname}"

            if key in seen:
                noindex.add((fullname, name))
            else:
                seen.add(key)

    return frozenset(noindex)


def _walk_modules(
    module: ModuleType, full_name: str, /
) -> Iterator[tuple[str, ModuleType]]:
    yield full_name, module

    for name in getattr(module, "__all__", ()):
        attr = getattr(module, name, None)

        if inspect.ismodule(attr):
            yield from _walk_modules(attr, f"{full_name}.{name}")


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

_metadata = importlib.metadata.metadata("ig-trading")
project = "IG Trading"
copyright = "2026, Nelson Yeung"  # noqa: A001
author = _metadata["Author-email"].split(" <")[0]
release = _metadata["Version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
]

templates_path = ["_templates"]
exclude_patterns = [
    ".DS_Store",
    "Thumbs.db",
    "_build",
    "global.rst",
]

rst_prolog = (_this_path.parent / "global.rst").read_text()

# autodoc settings
autodoc_member_order = "bysource"
autodoc_preserve_defaults = True
autodoc_typehints = "description"

# Several genuinely distinct classes across this project share the same
# short name (e.g. ``markets.v1.DealingRules`` and ``markets.v4.DealingRules``
# are different types for different API versions). ``autodoc_typehints =
# "description"`` cross-links type hints by short name, which is ambiguous
# for these. ``ref.python`` warnings about ambiguous (not missing) targets
# aren't covered by ``nitpick_ignore`` (that only applies in nitpicky mode
# to unresolved references), so suppress the category instead; the type
# hint still renders, just as plain (unlinked) text.
suppress_warnings = ["ref.python"]

# autosummary settings
autosummary_ignore_module_all = False
autosummary_context = {
    "noindex_pairs": _compute_noindex_pairs("ig_trading"),
    "external_alias_names": _compute_external_alias_names("ig_trading"),
}

# Intersphinx settings
intersphinx_mapping: dict[str, tuple[str, tuple[str, str] | str | None]] = {
    "python": ("https://docs.python.org/3", None),
}

# Napoleon settings
napoleon_numpy_docstring = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_css_files = ["custom.css"]
html_static_path = ["_static"]
