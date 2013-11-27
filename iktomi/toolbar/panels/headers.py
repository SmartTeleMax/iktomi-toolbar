from iktomi.toolbar.panels import DebugPanel


class Headers(DebugPanel):

    name = 'Headers'
    has_content = True
    headers = {}

    header_filter = (
        'CONTENT_TYPE',
        'HTTP_ACCEPT',
        'HTTP_ACCEPT_CHARSET',
        'HTTP_ACCEPT_ENCODING',
        'HTTP_ACCEPT_LANGUAGE',
        'HTTP_CACHE_CONTROL',
        'HTTP_CONNECTION',
        'HTTP_HOST',
        'HTTP_KEEP_ALIVE',
        'HTTP_REFERER',
        'HTTP_USER_AGENT',
        'QUERY_STRING',
        'REMOTE_ADDR',
        'REMOTE_HOST',
        'REQUEST_METHOD',
        'SCRIPT_NAME',
        'SERVER_NAME',
        'SERVER_PORT',
        'SERVER_PROTOCOL',
        'SERVER_SOFTWARE',
    )

    def nav_title(self):
        return 'HTTP Headers'

    def title(self):
        return 'HTTP Headers'

    def content(self):
        context = self.context.copy()
        context.update({
            'headers': self.headers
        })

        return self.render('panels/headers.html', context)

    def process_request(self, request):
        self.headers = dict(
            [(k, request.request.environ[k])
             for k in self.header_filter if k in request.request.environ]
        )
