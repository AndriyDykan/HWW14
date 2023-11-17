import sys
import os

sys.path.append(os.path.abspath(r'C:\Users\Miran\Desktop\HW14'))
project = 'HW14'
copyright = '2023, andriy'
author = 'Andriy'

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'nature'
html_static_path = ['_static']


