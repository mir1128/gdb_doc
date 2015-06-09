# Altering Execution

当程序中有bug，你可以在gdb中修改变量的值，让程序继续运行并观察后面的程序是否正确。

你可以修改变量，内存,给程序发送信号，在一个新的地址上再次运行，或者从一个函数中提前返回。

## Assignment to Variables

给一个变量赋值可以用print，也可以用set

	print x=4
	set x = 4
	(gdb) set var width=47
	
Because the set command has many subcommands that can conflict with the names of program variables, it is a good idea to use the set variable command instead of just set.

For example, if your program has a variable g, you run into problems if you try to set a new value with just ‘set g=4’, because gdb has the command `set gnutarget`, abbreviated set g:


## Continuing at a Di↵erent Address

Ordinarily, when you continue your program, you do so at the place where it stopped, with the continue command. You can instead continue at an address of your own choosing, with the following commands:

	jump linespec
	j linespec
	jump location
	j location

### Giving your Program a Signal

	queue-signal signal
	signal signal	
	
### Returning from a Function
	return
	return expression
		

## Calling Program Functions

	print expr
	call expr
		Evaluate the expression expr without displaying void returned values.
		
## Patching Programs

If you’d like to be able to patch the binary, you can specify that explicitly with the set write command.For example, you might want to turn on internal debugging flags, or even to make emergency repairs.

	set write on
	set write off

	show write
		#Display whether executable files and core files are 
		opened for writing as well as reading	

## Compiling and injecting code in gdb
gdb supports on-demand compilation and code injection into programs running under gdb.
GCC 5.0 or higher built with ‘libcc1.so’ must be installed for this functionality to be enabled. This functionality is implemented with the following commands.

	compile code source-code
	compile code -raw -- source-code
	
		
这个特性在gdb7.7.1中不支持

	(gdb) compile code
	Undefined command: "compile".  Try "help".

命令未定义	

























			

	
