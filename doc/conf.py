# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime as _datetime
from importlib.metadata import version as _get_version


project = "pyrsistent-as-rpds-py"
project_import_name = "rpds"
project_dist_name = "pyrsistent-as-rpds-py"
author = "Eduard Christian Dumitrescu'"
copyright = "2025, " + author


try:
    version = _get_version(project_dist_name)
except Exception:
    version = "UNKNOWN"
release = version + "~" + _datetime.date.today().strftime("%Y-%m-%d")

language = "en"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    # "sphinx.ext.imgmath",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]

source_suffix = ".rst"
master_doc = "index"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

todo_include_todos = True
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "classic"
html_static_path = ["_static"]
htmlhelp_basename = project_dist_name + "doc"
