# Sphinx configuration for the website of the BoSS.
#
# Layout and theme follow the DeepHyper documentation
# (https://deephyper.readthedocs.io): sphinx-book-theme with a persistent left
# sidebar built from the captioned toctrees on the home page. Pages are written
# in Markdown and parsed with MyST.

project = "The BoSS"
author = "The BoSS Development Team"
copyright = "2026, The BoSS Development Team"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",      # NumPy- and Google-style docstrings
    "sphinx.ext.viewcode",      # "[source]" links next to each function
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx.ext.mathjax",
    "sphinx.ext.githubpages",   # writes .nojekyll for GitHub Pages
]

source_suffix = {".md": "markdown"}
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Package documentation ----------------------------------------------------
# The API pages of the "Package documentation" section are generated at build
# time from the docstrings of the boss-bench package (import name boss_bench):
# one page per module, written to docs/api/ (generated, not committed) and
# listed by a glob toctree in index.md, in the order of API_MODULES. The build
# stops with an error if the package cannot be imported.
#
# To build against a local checkout of the package, install it into the build
# environment (pip install -e /path/to/boss-bench), or point to it with
#     BOSS_PACKAGE_SRC=/path/to/boss-bench sphinx-build -b html docs docs/_build/html
import importlib
import os
import pathlib
import sys

PACKAGE = "boss_bench"
API_MODULES = ["data", "confinement", "heat_flux", "trajectory", "design", "plotting"]
if os.environ.get("BOSS_PACKAGE_SRC"):
    sys.path.insert(0, os.environ["BOSS_PACKAGE_SRC"])

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_numpy_docstring = False
napoleon_google_docstring = True


def _write_api_pages():
    try:
        importlib.import_module(PACKAGE)
    except ImportError as e:
        raise RuntimeError(
            f"cannot import {PACKAGE} ({e}), so the package documentation cannot be "
            "built. Install boss-bench into this environment, or set BOSS_PACKAGE_SRC "
            "to a local checkout of it.") from e
    api_dir = pathlib.Path(__file__).parent / "api"
    api_dir.mkdir(exist_ok=True)
    pages = {}
    for number, name in enumerate(API_MODULES):
        module = f"{PACKAGE}.{name}"
        # the number only orders the glob toctree; the page title is the module name
        pages[f"{number}_{name}.md"] = (
            f"# `{module}`\n\n"
            "```{eval-rst}\n"
            f".. automodule:: {module}\n"
            "   :members:\n"
            "```\n")
    for old in api_dir.glob("*.md"):
        if old.name not in pages:
            old.unlink()
    for name, text in pages.items():
        path = api_dir / name
        # rewrite only on a change, so unchanged pages are not rebuilt
        if not path.exists() or path.read_text() != text:
            path.write_text(text)


_write_api_pages()

# -- MyST ---------------------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",     # ::: directives (admonitions, cards, dropdowns)
    "dollarmath",      # $...$ and $$...$$
    "amsmath",
    "attrs_inline",
    "deflist",
    "html_image",
]
myst_heading_anchors = 3   # so links like page.md#section resolve

# -- HTML -----------------------------------------------------------------------
html_theme = "sphinx_book_theme"
html_title = "The BoSS"
html_static_path = ["_static"]
templates_path = ["_templates"]
pygments_style = "sphinx"          # as in the DeepHyper docs
html_css_files = ["custom.css"]
# Stellarator image from the ARTEMISS logo, used until the BoSS has its own.
html_logo = "_static/logo/stellarator.svg"
html_favicon = "_static/logo/stellarator.svg"

html_theme_options = {
    # header
    "use_download_button": False,
    "use_fullscreen_button": True,
    # left sidebar: pages expand into their sections (see _templates/)
    "show_navbar_depth": 1,
    "home_page_in_toc": False,
    # no right-hand sidebar
    "secondary_sidebar_items": [],
}

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True


# -- Left sidebar with expandable page sections ------------------------------
# sphinx-book-theme's sidebar strips in-page section links, so pages could not
# expand into their sections (as on simsopt.readthedocs.io). This builds the
# sidebar from Sphinx's own toctree, which keeps them, and wraps each page's
# sections in the same <details> dropdown markup the theme uses, so the look and
# the expand arrows are unchanged. Used by _templates/sbt-sidebar-nav.html.
def _add_sidebar_nav(app, pagename, templatename, context, doctree):
    from bs4 import BeautifulSoup

    toctree = context.get("toctree")
    if toctree is None:
        return

    def boss_sidebar_nav():
        html = toctree(maxdepth=2, collapse=False, includehidden=True, titles_only=False)
        soup = BeautifulSoup(html, "html.parser")
        for ul in soup.find_all("ul", recursive=False):
            ul["class"] = ["nav", "bd-sidenav"]
        for li in soup.select("li.toctree-l1"):
            classes = li.get("class", [])
            if "current" in classes:
                li["class"] = classes + ["active"]
            sub = li.find("ul", recursive=False)
            if sub is None:
                continue
            li["class"] = li["class"] + ["has-children"]
            details = soup.new_tag("details")
            if "current" in classes:
                details["open"] = "open"
            summary = soup.new_tag("summary")
            toggle = soup.new_tag("span", attrs={"class": "toctree-toggle", "role": "presentation"})
            toggle.append(soup.new_tag("i", attrs={"class": "fa-solid fa-chevron-down"}))
            summary.append(toggle)
            details.append(summary)
            details.append(sub.extract())
            li.append(details)
        return str(soup)

    context["boss_sidebar_nav"] = boss_sidebar_nav


def setup(app):
    app.connect("html-page-context", _add_sidebar_nav)
