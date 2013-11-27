Iktomi Debug-toolbar
===================

This is a port of `flask-debug-toolbar <https://github.com/mgood/flask-debugtoolbar>`_
for Iktomi applications.
If enabled, the toolbar will automatically be injected into Jinja templates.


Usage
-----

You can attach the toolpar to an application by chaining it before one::

  app = iktomi.toolbar.handler() | app

To enable the toolbar, set following variable in your development cfg.py::

  IKTOMI_TOOLBAR = True

Panels (by default enabled all)::

  IKTOMI_TOOLBAR_PANELS = (
    'iktomi.toolbar.panels.sqla',  # sqlalchemy queries
    'iktomi.toolbar.panels.logger',  # logging messages from view
    'iktomi.toolbar.panels.headers',  # headers of request
    'iktomi.toolbar.panels.request',  # request information
    'iktomi.toolbar.panels.timer',  # time of request
    'iktomi.toolbar.panels.versions'  # versions of few installed libraries
  )

