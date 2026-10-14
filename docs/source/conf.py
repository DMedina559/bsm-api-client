"""Build the SDK developer documentation without connecting to BSM."""

from importlib.metadata import version as package_version

project = "BSM API Client"
author = "DMedina559"
release = package_version("bsm-api-client")
extensions = ["sphinx.ext.autodoc", "myst_parser"]
html_theme = "sphinx_rtd_theme"
myst_heading_anchors = 3
autodoc_member_order = "bysource"
autodoc_typehints = "signature"
exclude_patterns = ["_build"]
