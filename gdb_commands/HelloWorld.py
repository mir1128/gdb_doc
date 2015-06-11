import gdb

class HelloWorld(gdb.Command):
    """Greet the whole world."""
    def __init__ (self):
        super(HelloWorld, self).__init__("hello-world", gdb.COMMAND_USER)

    def invoke (self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len (argv) != 0:
            raise gdb.GdbError ("hello-world takes no arguments")
        print "Hello, World!"

HelloWorld()

