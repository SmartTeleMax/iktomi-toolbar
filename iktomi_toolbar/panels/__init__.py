

class DebugPanel(object):
    """
    Base class for debug panels.
    """
    has_content = False

    context = {}

    # Panel methods
    def __init__(self, jinja_env, context={}):
        self.context.update(context)
        self.jinja_env = jinja_env

        # If the client enabled the panel
        self.is_active = False

    def render(self, template_name, context):
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)

    def dom_id(self):
        return 'insDebug%sPanel' % (self.name.replace(' ', ''))

    def nav_title(self):
        """Title showing in toolbar"""
        return self.name

    def nav_subtitle(self):
        """Subtitle showing until title in toolbar"""
        return ''

    def title(self):
        """Title showing in panel"""
        return self.name

    def url(self):
        return ''

    def content(self):
        raise NotImplementedError

    # Standard middleware methods
    def process_request(self, request):
        pass

    def process_response(self, request):
        pass
