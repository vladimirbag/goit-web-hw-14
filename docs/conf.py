# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath('../'))

# -- Project information -----------------------------------------------------
project = 'contacts'
copyright = '2025, vova27n'
author = 'vova27n'
release = 'super'

# -- General configuration ---------------------------------------------------
extensions = ["sphinx.ext.autodoc"]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']

locale_dirs = []
