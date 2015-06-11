__author__ = 'jieliu'


import gdb

class PrintValue (gdb.Command):
    "print value"
    def __init__ (self):
        super (PrintValue, self).__init__ ("printvalue", gdb.COMMAND_SUPPORT, gdb.COMPLETE_NONE, True);

    def invoke(self, arg, from_tty):
        for x in gdb.pretty_printers:
            print x

PrintValue();


