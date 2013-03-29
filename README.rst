Iktomi Debug-toolbar
===================

This is a port of `flask-debug-toolbar <https://github.com/mgood/flask-debugtoolbar>`_
for Flask applications.
If enabled, the toolbar will automatically be injected into Jinja templates.


Usage
-----

You can attach the toolpar to an application by chaining it before one::

  app = iktomi_toolbar.handler() | app

To enable the toolbar, set following variable in your development cfg.py::

  IKTOMI_TOOLBAR = True

Panels (by default enabled all)::

  IKTOMI_TOOLBAR_PANELS = (
    'iktomi_toolbar.panels.sqla',  # sqlalchemy queries
    'iktomi_toolbar.panels.logger',  # logging messages from view
    'iktomi_toolbar.panels.headers',  # headers of request
    'iktomi_toolbar.panels.request',  # request information
    'iktomi_toolbar.panels.timer',  # time of request
    'iktomi_toolbar.panels.versions'  # versions of few installed libraries
  )

