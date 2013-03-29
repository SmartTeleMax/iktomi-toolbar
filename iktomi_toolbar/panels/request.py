from iktomi_toolbar.panels import DebugPanel


class Request(DebugPanel):

    name = 'Request'
    has_content = True

    def nav_title(self):
        return 'Request Vars'

    def content(self):
        context = self.context.copy()
        context.update({'cookies': tuple((k, self.request.cookies.get(k))
                                          for k in self.request.cookies),
                        'get': tuple(self.get_GET()),
                        'post': self.get_POST()})

        return self.render('panels/request_vars.html', context)

    def process_request(self, request):
        self.request = request.request

    def get_GET(self):
        for arg in self.request.environ['QUERY_STRING'].split('&'):
            if arg:
                yield arg.split('=')

    def get_POST(self):
        return None
