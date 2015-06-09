# gdb Text User Interface
The gdb Text User Interface (TUI) is a terminal interface which uses the curses library to show the source file, the assembly output, the program registers and gdb commands in separate text windows. The TUI mode is supported only on platforms where a suitable version of the curses library is available.

The TUI mode is enabled by default when you invoke gdb as ‘gdb -tui’. You can also switch in and out of TUI mode while gdb runs by using various TUI commands and key bindings, such as C-x C-a. 

## TUI Overview
