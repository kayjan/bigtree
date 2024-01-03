import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../.."))
import bigtree

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "bigtree"
copyright = "2022, Kay Jan WONG"
author = "Kay Jan WONG"
release = bigtree.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "autodocsumm",
    "myst_parser",
    "sphinxemoji.sphinxemoji",
    "sphinx.ext.mathjax",
    "sphinx.ext.doctest",
]
autodoc_default_options = {"autosummary": True}
sphinxemoji_style = "twemoji"
myst_enable_extensions = [
    "attrs_block",
]
base_dir = os.path.dirname(os.path.dirname(os.getcwd()))
assets_dir = os.path.join(base_dir, "assets", "docstr")
doctest_global_setup = f"""
import os
if not os.path.exists(r"{assets_dir}"):
    os.mkdir(r"{assets_dir}")
"""

templates_path = ["_templates"]
exclude_patterns = []

language = "Python"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "karma_sphinx_theme"
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
html_logo = "_static/favicon.ico"


def setup(app):
    app.add_css_file("custom.css")
