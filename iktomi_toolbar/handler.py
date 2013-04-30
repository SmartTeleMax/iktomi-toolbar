# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
import traceback

import cfg
import environment

from iktomi.web.core import WebHandler
from iktomi.web import Response

from jinja2 import Environment, FileSystemLoader

from utils import replace_insensitive

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
        'iktomi_toolbar.panels.sqla',  # sqlalchemy queries
        'iktomi_toolbar.panels.logger',  # logging messages from view
        'iktomi_toolbar.panels.headers',  # headers of request
        'iktomi_toolbar.panels.request',  # request information
        'iktomi_toolbar.panels.timer',  # time of request
        'iktomi_toolbar.panels.versions'  # versions of few installed libraries
    )

    panel_classes = []
    enable = getattr(cfg, 'IKTOMI_TOOLBAR', False)

    def __init__(self):
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


class Tmpl(environment.BoundTemplate):

    def render_to_response(self, template_name, __data,
                           content_type="text/html"):
        response_html = self.template.render(template_name,
                                             **self._vars(__data))

        response_html = replace_insensitive(
            response_html, '</body>',
            self.toolbar.render_panel(self) + '</body>'
        )
        return Response(response_html, content_type=content_type)


class handler(DebugToolbar, WebHandler):

    def process_request(self, request):
        for panel in self.panel_classes:
            panel.process_request(request)

    def toolbar(self, env, data):
        """This method should be overridden in subclasses."""
        try:
            if self.enable:
                self.process_request(env)
                debug_template = Tmpl(env, environment.template_loader)
                debug_template.toolbar = self
                debug_template.process_response = self.process_response
                env.template = debug_template
                env.render_to_response = debug_template.render_to_response
            return self.next_handler(env, data)
        except Exception as e:
            print(traceback.print_exc())
            raise e

    __call__ = toolbar  # For nice traceback
