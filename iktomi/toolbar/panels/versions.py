from iktomi.toolbar.panels import DebugPanel
import iktomi.toolbar


class Versions(DebugPanel):

    name = 'Version'
    has_content = True

    libraries = ('webob',
                 'sqlalchemy',
                 'jinja2',
                 'simplejson',
                 'html5lib',
                 'dateutil',
                 'iktomi.toolbar',
                 'instesting',
                 'clevercss',
                 'memcache',
                 'testalchemy')

    def __init__(self, *arg, **kwarg):
        super(Versions, self).__init__(*arg, **kwarg)

        self.versions = {}

        for lib in self.libraries:
            try:
                mod = __import__(lib)
                version = getattr(mod, '__version__', None)
                if version:
                    self.versions.update({lib: version})
                del mod
            except ImportError, e:
                print "Can't import `{0}`: {1}".format(lib, e)

    def nav_subtitle(self):
        return iktomi.toolbar.__version__

    def content(self):

        context = self.context.copy()
        context.update({'libraries': self.versions})

        return self.render('panels/versions.html', context)
