# Examining the Symbol Table

	info address symbol
		Describe where the data for symbol is stored. 
		For a register variable, this says which register it is kept in.

	info symbol addr
		(gdb) info symbol 0x54320
		_initialize_vx + 396 in section .text

	demangle [-l language] [--] name
	
	ptype[/flags] [arg]

一个使用ptype的例子:

	typedef double real_t;    struct complex { real_t real; double imag; };    typedef struct complex complex_t;    complex_t var;    real_t *real_pointer_var;

`whatis`和`ptype`的区别:    	(gdb) whatis var
	type = complex_t
	(gdb) ptype var
	type = struct complex {
	real_t real;
	    double imag;
	}
	(gdb) whatis complex_t
	type = struct complex
	(gdb) whatis struct complex
	type = struct complex
	(gdb) ptype struct complex
	type = struct complex {
	real_t real;
	    double imag;
	}
	(gdb) whatis real_pointer_var
	type = real_t *
	(gdb) ptype real_pointer_var
	type = double *	info types regexp 	info types			
		# Print a brief description of all types whose names match the regular expression regexp

	info type-printers
		#info type-printers displays all the available type printers.
		
	info scope location

一个例子：

		(gdb) info scope command line handler
		Scope for command_line_handler:
		Symbol rl is an argument at stack/frame offset 8, length 4.
		Symbol linebuffer is in static storage at address 0x150a18, length 4. Symbol linelength is in static storage at address 0x150a1c, length 4. Symbol p 		is a local variable in register $esi, length 4.
		Symbol p1 is a local variable in register $ebx, length 4.
		Symbol nline is a local variable in register $edx, length 4.
		Symbol repeat is a local variable at frame offset -8, length 4.
		

	info source	
			
	info sources
		Print the names of all source files in your program 
		for which there is debugging information, 
		organized into two lists: files whose symbols have already been read, 
		and files whose symbols will be read when needed.

	info functions
		#Print the names and data types of all defined functions.

	info functions regexp
	info variables
	info variables regexp
	info classes
	info classes regexp
	
	set print symbol-loading
		The set print symbol-loading command allows you to control the printing
		of messages when gdb loads symbol information.
		
						

























					