from datetime import datetime
import logging

try:
    import threading
except ImportError:
    threading = None

from iktomi.toolbar.panels import DebugPanel
from iktomi.toolbar.utils import format_fname, Storage


class ThreadTrackingHandler(logging.Handler):
    def __init__(self):
        if threading is None:
            raise NotImplementedError("threading module is not available, \
                the logging panel cannot be used without it")
        logging.Handler.__init__(self)
        self.records = Storage()

    def emit(self, record, thread=None):
        self.records.new({'entry': record})

    def get_records(self, thread=None):
        return self.records.get_and_clear()


handler = None
_init_lock = threading.Lock()


def _init_once():
    global handler
    if handler is not None:
        return
    with _init_lock:
        if handler is not None:
            return
        handler = ThreadTrackingHandler()
        logging.root.addHandler(handler)

_init_once()


class Logger(DebugPanel):

    name = 'Logging'
    has_content = True

    def content(self):
        records = []
        for message in self.messages:
            record = message['entry']
            records.append({
                'message': record.getMessage().decode('utf-8'),
                'time': datetime.fromtimestamp(record.created),
                'level': record.levelname,
                'file': format_fname(record.pathname),
                'file_long': record.pathname,
                'line': record.lineno
            })

        context = self.context.copy()
        context.update({'records': records})

        return self.render('panels/logger.html', context)

    def get_and_delete(self):
        if handler:
            records = handler.get_records()
            return records
        return []

    def process_response(self, request):
        self.messages = self.get_and_delete()
