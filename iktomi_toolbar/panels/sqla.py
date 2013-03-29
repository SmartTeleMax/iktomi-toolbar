import time
from functools import partial

from iktomi_toolbar.panels import DebugPanel
from iktomi_toolbar.utils import Storage

from sqlalchemy import event
from sqlalchemy.engine import Engine

try:
    import sqlparse
except ImportError:
    format_sql = lambda x: x
else:
    format_sql = partial(sqlparse.format,
                         reindent=True,
                         keyword_case='upper')


log = Storage()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    context._query_start_time = time.time()
    log.new({'query': statement,
             'params': parameters,
             'action': statement.split('`', 1)[0],
             'sql': format_sql(statement),
             'context': context,
             'time': context._query_start_time})


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    total = time.time() - context._query_start_time
    log.update({'time': total})


class Sqla(DebugPanel):

    name = 'SQLAlchemy'
    has_content = True

    def title(self):
        return 'SQLAlchemy (%s)' % self.count
    nav_title = title

    def __init__(self, *args, **kwargs):
        super(Sqla, self).__init__(*args, **kwargs)
        self.queries = {}

    def content(self):

        context = self.context.copy()
        context.update({'queries': self.queries})

        return self.render('panels/sqlalchemy.html', context)

    def process_response(self, request):
        self.count = log.glob
        self.queries = log.get_and_clear()
