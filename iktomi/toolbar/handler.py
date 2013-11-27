# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
import traceback

from iktomi.web.core import WebHandler

from jinja2 import Environment, FileSystemLoader

from .utils import replace_insensitive

__all__ = ['handler']


LIB_PATH = os.path.dirname(__file__)
TEMPLATES_PATH = os.path.join(LIB_PATH, 'templates')
STATIC_PATH = os.path.join(LIB_PATH, 'static')


def read_js():
    JS_FILES = ('jquery.js',
                'jquery.tablesorter.js',
                'toolbar.js')

    for file in JS_FILES:
        with open(os.path.join(STATIC_PATH, 'js', file), 'r') as js:
            yield js.read().decode('utf-8')


class DebugToolbar(object):

    DEFAULT_PANELS = (
        'iktomi.toolbar.panels.sqla',  # sqlalchemy queries
        # XXX this panel breaks exception logging
        #'iktomi.toolbar.panels.logger',  # logging messages from view
        'iktomi.toolbar.panels.headers',  # headers of request
        'iktomi.toolbar.panels.request',  # request information
        'iktomi.toolbar.panels.timer',  # time of request
        'iktomi.toolbar.panels.versions'  # versions of few installed libraries
    )

    panel_classes = []

    def __init__(self, cfg):
        self.enable = getattr(cfg, 'IKTOMI_TOOLBAR', False)
        if self.enable:
            self.panels = getattr(cfg, 'IKTOMI_TOOLBAR_PANELS', self.DEFAULT_PANELS)
            self.jinja_env = Environment(loader=FileSystemLoader(
                TEMPLATES_PATH
            ))
            self.js = "\n/*===*/\n".join(read_js())
            self.load_panels()

    def load_panels(self):
        for panel_path in self.panels:
            dot = panel_path.rindex('.')
            panel_classname = panel_path[dot + 1:]

            try:
                mod = __import__(panel_path, {}, {}, [''])
            except ImportError:
                print traceback.print_exc()
                continue
            panel_class = getattr(mod, panel_classname.capitalize())(
                jinja_env=self.jinja_env
            )
            self.panel_classes.append(panel_class)

    def render_panel(self, env):

        self.process_response(env)

        return self.jinja_env.get_template('base.html').render({
            'raw_js': self.js,
            'panels': self.panel_classes,
        })

    def process_response(self, response):
        for panel in self.panel_classes:
            panel.process_response(response)


class handler(DebugToolbar, WebHandler):

    def process_request(self, request):
        for panel in self.panel_classes:
            panel.process_request(request)

    def toolbar(self, env, data):
        """This method should be overridden in subclasses."""
        if not self.enable:
            return self.next_handler(env, data)
        self.process_request(env)
        resp = self.next_handler(env, data)
        if resp.content_type == 'text/html':
            resp.body = replace_insensitive(
                resp.body.decode('utf-8'), '</body>',
                self.render_panel(env) + '</body>'
            ).encode('utf-8')
        return resp


    __call__ = toolbar  # For nice traceback
