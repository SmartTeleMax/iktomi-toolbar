import time
import traceback
from functools import partial

from iktomi.toolbar.panels import DebugPanel
from iktomi.toolbar.utils import Storage

from sqlalchemy import event
from sqlalchemy.engine import Engine

try:
    import sqlparse
except ImportError:
    format_sql = lambda x: x
    sql_action = lambda x: x.split('`', 1)[0]
else:
    format_sql = partial(sqlparse.format,
                         reindent=True,
                         keyword_case='upper')
    sql_action = lambda x: sqlparse.parse(x)[0].get_type()


log = Storage()

def short_traceback(stack):
    tb = []
    for frame in stack:
        fl, line, module, code = frame
        if '/wsgiref/' in fl:
            tb = []
        if '/iktomi/web/filters.py' in fl:
            tb = []
        if '/iktomi/' in fl or '/sqlalchemy/' in fl:
            pass
        else:
            tb.append(frame)

    formatted = traceback.format_list(tb)
    return ''.join(formatted).decode('utf-8')


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    context._query_start_time = time.time()
    log.new({'query': statement,
             'params': parameters,
             'action': sql_action(statement),
             'sql': format_sql(statement),
             'context': context,
             'traceback': short_traceback(traceback.extract_stack()),
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

    def nav_subtitle(self):
        return 'TOTAL: %0.2fms' % (self.total_time * 1000)

    def __init__(self, *args, **kwargs):
        super(Sqla, self).__init__(*args, **kwargs)
        self.queries = []

    def content(self):
        context = self.context.copy()
        context.update({'queries': self.queries})
        return self.render('panels/sqlalchemy.html', context)

    def process_request(self, env):
        self.old_queries = list(log.get_and_clear())
    #    for engine in set(env.db._Session__binds.values()):
    #        env.db.execute('RESET QUERY CACHE;', bind=engine)

    def process_response(self, env):
        self.count = log.glob
        self.queries = list(log.get_and_clear())
        self.total_time = sum(x['time'] for x in self.queries)
