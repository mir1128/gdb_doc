import gdb

class DisplayValue(gdb.Command):
    def __init__(self):
        super(DisplayValue, self).__init__("display-value", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        argvs = gdb.string_to_argv(args)
        for argv in argvs:
            myval = gdb.parse_and_eval(argv)
            print myval.address

DisplayValue()