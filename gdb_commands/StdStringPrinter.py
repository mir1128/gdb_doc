__author__ = 'jieliu'

import re
import gdb

class StdStringPrinter(object):
    "Print a std::string"
    def __init__(self, val):
        self.val = val

    def to_string(self):
        return self.val[’_M_dataplus’][’_M_p’];

    def display_hint(self):
        return ’string’


def str_lookup_function(val):
    lookup_tag = val.type.tag
    if lookup_tag == None:
        return None
    regex = re.compile("^std::basic_string<char,.*>$")
    if regex.match(lookup_tag):
        return StdStringPrinter(val)
    return None
