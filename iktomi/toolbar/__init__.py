"""
iktomi-debug-toolbar

ported from https://github.com/mgood/flask-debugtoolbar

how to enable::

  IKTOMI_TOOLBAR = True

panels (by default enabled all)::

  IKTOMI_TOOLBAR_PANELS = (
    'iktomi.toolbar.panels.sqla',  # sqlalchemy queries
    'iktomi.toolbar.panels.logger',  # logging messages from view
    'iktomi.toolbar.panels.headers',  # headers of request
    'iktomi.toolbar.panels.request',  # request information
    'iktomi.toolbar.panels.timer',  # time of request
    'iktomi.toolbar.panels.versions'  # versions of few installed libraries
  )
"""
from handler import handler

__all__ = ['handler', '__version__']
__version__ = '0.0.1'
