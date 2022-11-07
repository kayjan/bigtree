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
]
autodoc_default_options = {"autosummary": True}

templates_path = ["_templates"]
exclude_patterns = []

language = "Python"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pyramid"
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"
html_logo = "_static/favicon.ico"


def setup(app):
    app.add_css_file("custom.css")
