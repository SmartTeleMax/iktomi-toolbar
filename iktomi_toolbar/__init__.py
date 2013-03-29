"""
iktomi-debug-toolbar

ported from https://github.com/mgood/flask-debugtoolbar

how to enable::

  IKTOMI_TOOLBAR = True

panels (by default enabled all)::

  IKTOMI_TOOLBAR_PANELS = (
    'iktomi_toolbar.panels.sqla',  # sqlalchemy queries
    'iktomi_toolbar.panels.logger',  # logging messages from view
    'iktomi_toolbar.panels.headers',  # headers of request
    'iktomi_toolbar.panels.request',  # request information
    'iktomi_toolbar.panels.timer',  # time of request
    'iktomi_toolbar.panels.versions'  # versions of few installed libraries
  )
"""
from handler import handler

__all__ = ['handler', '__version__']
__version__ = '0.0.1'
