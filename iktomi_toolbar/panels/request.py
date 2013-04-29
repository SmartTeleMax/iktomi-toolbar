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
                        'get': self.get_GET(),
                        'post': self.get_POST()})

        return self.render('panels/request_vars.html', context)

    def process_request(self, request):
        self.request = request.request

    def decode_args(self, arg):
        name, value = arg

        yield name.decode('utf-8')

        if isinstance(value, (list, tuple)):
            yield [v.decode('utf-8') for v in value]
        else:
            yield value.decode('utf-8')

    def get_GET(self):
        return map(self.decode_args, self.request.str_GET.mixed().items())

    def get_POST(self):
        return map(self.decode_args, self.request.str_POST.mixed().items())
