# gdb Files

gdb needs to know the file name of the program to be debugged, both in order to read its symbol table and in order to start your program.To debug a core dump of a previous run, you must also tell gdb the name of the core dump file.

## Commands to Specify Files
You may want to specify executable and core dump file names. The usual way to do this is at start-up time, using the arguments to gdb’s start-up commands

Occasionally it is necessary to change to a di↵erent file during a gdb session. Or you may run gdb and forget to specify a file you want to use. Or you are debugging a remote target via gdbserver.In these situations the gdb commands to specify new files are useful.

	file filename
		Use filename as the program to be debugged.
		You can load unlinked object ‘.o’ files into gdb using the file command. 
		You will not be able to “run” an object file, 
		but you can disassemble functions and inspect variables. 
		Also, if the underlying BFD functionality supports it, 
		you could use gdb -write to patch object files using this technique. 

	file
		file with no argument makes gdb discard any information it has on 
		both executable file and the symbol table.

	exec-file [ filename ]
		Specify that the program to be run (but not the symbol table) is found in file- name. 
		gdb searches the environment variable PATH if necessary to locate your program. 
		Omitting filename means to discard information on the executable file.
		
	symbol-file [ filename ]
		Read symbol table information from file filename. PATH is searched when nec- essary. 
		Use the file command to get both symbol table and program to run from the same file.
		symbol-file with no argument clears out gdb information on your program’s symbol table.
		The symbol-file command causes gdb to forget the contents of some break- points 
		and auto-display expressions.			
		This is because they may contain pointers to the internal data recording symbols 
		and data types, which are part of the old symbol table data being discarded inside gdb.
		
	symbol-file [ -readnow ] filename
	core-file [filename]
	core
	remove-symbol-file filename
	remove-symbol-file -a address
	add-symbol-file-from-memory address


## Debugging Information in Separate Files

## Debugging information in a special section## Index Files Speed Up gdb
## Errors Reading Symbol Files
## GDB Data Files
gdb will sometimes read an auxiliary data file. These files are kept in a directory known as the data directory.
You can set the data directory’s name, and view the name gdb is currently using.
	
	set data-directory directory
	show data-directory
	
















































































			
					
