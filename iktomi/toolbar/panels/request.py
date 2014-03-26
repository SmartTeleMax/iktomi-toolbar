from iktomi.toolbar.panels import DebugPanel


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

    def force_unicode(self, val):
        if not isinstance(val, unicode):
            return val.decode('utf-8')
        return val

    def decode_args(self, arg):
        name, value = arg

        yield self.force_unicode(name)

        if isinstance(value, (list, tuple)):
            yield [self.force_unicode(v) for v in value]
        else:
            yield self.force_unicode(value)

    def get_GET(self):
        return map(self.decode_args, self.request.GET.mixed().items())

    def get_POST(self):
        return map(self.decode_args, self.request.POST.mixed().items())
