import gdb

class BackTracePrinter(gdb.Command):
    "print backtrace "
    def __init__(self):
        super(BackTracePrinter, self).__init__("pretty-backtrace", gdb.COMMAND_USER)

    def invoke (self, args, from_tty):
        argv = gdb.string_to_argv(args)
        newestFrame = gdb.newest_frame()
        print "the newest frame is : " + newestFrame.name()

        architecture = newestFrame.architecture()
        print "this architecture is : " + architecture.name()

        for inc in architecture.disassemble(int(argv[0], 16), int(argv[1], 16)):
            print inc['asm']


BackTracePrinter()
