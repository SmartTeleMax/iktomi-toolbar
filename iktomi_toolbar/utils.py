import os.path
import sys


def format_fname(value):
    # If the value is not an absolute path, the it is a builtin or
    # a relative file (thus a project file).
    if not os.path.isabs(value):
        if value.startswith(('{', '<')):
            return value
        if value.startswith('.' + os.path.sep):
            return value
        return '.' + os.path.sep + value

    # If the file is absolute and within the project root handle it as
    # a project file

    # Loop through sys.path to find the longest match and return
    # the relative path from there.
    prefix = None
    prefix_len = 0
    for path in sys.path:
        new_prefix = os.path.commonprefix([path, value])
        if len(new_prefix) > prefix_len:
            prefix = new_prefix
            prefix_len = len(prefix)

    if not prefix.endswith(os.path.sep):
        prefix_len -= 1
    path = value[prefix_len:]
    return '<%s>' % path


def replace_insensitive(string, target, replacement):
    """Similar to string.replace() but is case insensitive
    Code borrowed from:
    http://forums.devshed.com/python-programming-11/
    case-insensitive-string-replace-490921.html
    """
    no_case = string.lower()
    index = no_case.rfind(target.lower())
    if index >= 0:
        return string[:index] + replacement + string[index + len(target):]
    else:  # no results so return the original string
        return string


class Storage(object):

    def __init__(self):
        self.glob = 0
        self.current = 0
        self.queries = {}

    def new(self, di):
        self.glob += 1
        self.current = self.glob
        self.queries[self.current] = di

    def update(self, di):
        self.queries[self.current].update(di)

    def get_and_clear(self):
        for query in self.queries.itervalues():
            yield query

        self.glob = 0
        self.current = 0
        self.queries = {}

    def delete(self, item):
        del self.queries[item]
