import gdb

class DisplayType(gdb.Command):
    def __init__(self):
        super(DisplayType, self).__init__("display-value", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        tp = gdb.lookup_type(argv[0], gdb.newest_frame().block())

        for item in tp.items():
            print item


DisplayType()
