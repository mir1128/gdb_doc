from __future__ import with_statement
import gdb

class SaveBreakpointsCommand(gdb.Command):
    """Save the current breakpoints to a file.
    This command takes a single argument, a file name.
    The breakpoints can be restored using the 'source' command."""

    def __init__(self):
        super(SaveBreakpointsCommand, self).__init__("save breakpoints", gdb.COMMAND_SUPPORT, gdb.COMPLETE_FILENAME)


    def invoke(self, arg, from_tty):
        with open (arg, 'w') as f:
            for bp in gdb.breakpoints():
                print >> f, "break", bp.location,
                if bp.thread is not None:
                    print >> f, " thread", bp.thread,
                if bp.condition is not None:
                    print >> f, " if", bp.condition,
                print >> f
                if not bp.enabled:
                    print >> f, "disable $bpnum"
                # Note: we don't save the ignore count; there doesn't
                # seem to be much point.
                commands = bp.commands
                if commands is not None:
                    print >> f, "commands"
                    # Note that COMMANDS has a trailing newline.
                    print >> f, commands,
                    print >> f, "end"
                print >> f

SaveBreakpointsCommand()