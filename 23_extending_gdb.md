#Extending gdb

gdb提供了几种扩展机制，gdb自动加载扩展文件。使用文件扩展名区分使用的是哪种扩展，如果是不认识的扩展名一律认为是命令文件。

You can control how gdb evaluates these files with the following setting:

	set script-extension off
		#All scripts are always evaluated as gdb Command Files.
	set script-extension soft
		#The debugger determines the scripting language based on filename extension. 
		If this scripting language is supported, gdb evaluates the script using that language.
		Otherwise, it evaluates the file as a gdb Command File.

	set script-extension strict
	show script-extension
		#Display the current value of the script-extension option.
		

## Canned Sequences of Commands

除了断点命令以外，gdb提供了两种批命令执行的方式：用户自定义命令和命令文件。

### User-defined Commands

A user-defined command is a sequence of gdb commands to which you assign a new name as a command. This is done with the define command. User commands may accept up to 10 arguments separated by whitespace. Arguments are accessed within the user command via $arg0...$arg9. A trivial example:

	define adder        print $arg0 + $arg1 + $arg2	end
To execute the command use:
	adder 1 2 3
$argc 表示有几个参数
例子：
	define adder        if $argc == 2          print $arg0 + $arg1        end        if $argc == 3          print $arg0 + $arg1 + $arg2		end 
	end	
	

命令格式：

	define commandname
		#Define a command named commandname. 
		If there is already a command by that name, 
		you are asked to confirm that you want to redefine it.

	document commandname

例子：

    (gdb) define adder
    Type commands for definition of "adder".
    End with a line saying just "end".
    >        print $arg0 + $arg1 + $arg2
    >end
    (gdb) adder 1 2 3
    $1 = 6
    (gdb) document adder
    Type documentation for "adder".
    End with a line saying just "end".
    >this is a test.
    >end
    (gdb) help adder
    this is a test.
    (gdb)

	dont-repeat    
	help user-defined
		#显示所有用户自定义的命令。
	show user
	show user commandname
		#Display the gdb commands used to define commandname (but not its documen- tation). 
		If no commandname is given, display the definitions for all user-defined commands. 
		This does not work for user-defined python commands.

	show max-user-call-depth
	set max-user-call-depth
		#The value of max-user-call-depth controls how many recursion levels are allowed 
		in user-defined commands before gdb suspects an infinite recursion 
		and aborts the command. This does not apply to user-defined python commands.


### User-defined Command Hooks

如果有`hook-foo`，它会在foo之前执行，`hookpost-foo`会在foo之后执行。这两种hook可以同时存在。

hook命令可以调用被它hook的命令，并且不会引起递归。

一个例子，自定义一个`hook-next`命令，这样每次执行next都会执行该命令。

    (gdb) define hook-next
    Type commands for definition of "hook-next".
    End with a line saying just "end".
    >print "hello"
    >end
    (gdb) hook-next
    $1 = "hello"
    (gdb) n
    $2 = "hello"
    begin
    37      struct SimpleStruct ss = { 10, 1.11 };    

you should define a hook for the basic command name, e.g. backtrace rather than bt
You can hook a multi-word command by adding hook- or hookpost- to the last word of the command, e.g. ‘define target hook-remote’ to add a hook to ‘target remote’.    
		 				
### Command Files
命令文件就是一个普通的文本文件，每一行都是gdb命令。还包括注释。命令文件中的空行不会重复上一次执行的命令。
可以用`source`命令执行一个命令文件。Note that the source command is also used to evaluate scripts that are not Command Files.The exact behavior can be configured using the script-extension setting.

	source [-s] [-v] filename
		#Execute the command file filename.
		
命令执行的过程中如果发生错误就会终止当前的命令并返回。
gdb首在当前目录查找命令（脚本）文件，如果指定的文件名中没有路径，那么gdb会在search path下寻找文件。除了"$cdir"，这个目录不在搜索范围之内。

If -s is specified, then gdb searches for filename on the search path even if filename speci- fies a directory. The search is done by appending filename to each element of the search path.
So, for example, if filename is ‘mylib/myscript’ and the search path contains ‘/home/user’ then gdb will look for the script ‘/home/user/mylib/myscript’.The search is also done if filename is an absolute path. For example, if filename is ‘/tmp/myscript’ and the search path contains ‘/home/user’ then gdb will look for the script ‘/home/user/tmp/myscript’.

If -v, for verbose mode, is given then gdb displays each command as it is executed. The option must be given before filename, and is interpreted as part of the filename anywhere else.
-v会显示每条执行的命令。

条件控制关键字：
	
	if	else
	while	loop_break	loop_continue	end

					
### Commands for Controlled Output

During the execution of a command file or a user-defined command, normal gdb output is suppressed;  the only output that appears is what is explicitly printed by the commands in the definition.three commands is useful for generating exactly the output you want.

	echo text

	output expression
	
	output/fmt expression
	
	printf template, expressions...
	
	eval template, expressions...
	
	
### Controlling auto-loading native gdb scripts

Auto-loading can be enabled or disabled, and the list of auto-loaded scripts can be printed.

	set auto-load gdb-scripts [on|off]
	show auto-load gdb-scripts
	info auto-load gdb-scripts [regexp]



## Extending gdb using Python

Python scripts used by gdb should be installed in ‘data-directory/python’, where data-directory is the data directory as determined at gdb startup.(什么是gdb的data files)
This directory, known as the python directory, is automatically added to the Python Search Path in order to allow the Python interpreter to locate all scripts installed at this location.

Additionally, gdb commands and convenience functions which are written in Python and are located in the ‘data-directory/python/gdb/command’ or ‘data- directory/python/gdb/function’ directories are automatically imported when gdb starts.

### Python Commands

gdb provides two commands for accessing the Python interpreter, and one related setting:

	python-interactive [command]
	pi [command]
		#Without an argument, the python-interactive command can be used 
		to start an interactive Python prompt. 
		To return to gdb, type the EOF character (e.g., Ctrl-D on an empty prompt).

	python [command]
	py [command]
		#The python command can be used to evaluate Python code.

	set python print-stack
	source ‘script-name’
	python execfile ("script-name")
	

### Python API

`python help (gdb)`可以看一下python里面的gdb模块有哪些类和函数。

`python help(gdb.inforier)`
#### Basic Python
GDB为python解释器自动import了一个gdb模块
	gdb.post_event (event)
		#给gdb内部的事件队列push一个可调用对象。这个可调用对象会在后面某个时间点调用。
		事件会按照它们被post的先后顺序调用。
		
(GDB的事件队列是怎样的机制？)			

	gdb.write()
		#打印，默认是gdb.STDOUT此外还有gdb.STDERR,gdb.STDLOG
		

	gdb.solib_name (address)
		查看某个地址所在的so或者lib


#### Exception Handling

python代码本身没有处理的异常会打印在gdb的命令行中


#### Values From Inferior

从Inferior里面获取的程序信息都可以用gdb.Value这种类型保存

Inferior 的 values可以使用python的directory语法访问.比如：if some_val is a gdb.Value instance holding a structure, you can access its foo element with:

	bar = some_val[’foo’]

Structure elements can also be accessed by using gdb.Field objects as subscripts 


	Value.dynamic_type
		#The dynamic type of this gdb.Value.
		#This uses C++ run-time type information (RTTI) to determine the dynamic 
		type of the value.
		Note that this feature will only work when debugging a C++ program 
		that includes RTTI for the object in question. 
		Otherwise, it will just return the static type of the value as in ptype foo

	Value.__init__ (val)
		Many Python values can be converted directly to a gdb.
		Value via this object initial- izer. Specifically:

	Value.dereference ()
		For pointer data types, this method returns a new gdb.
		Value object whose contents is the object pointed to by the pointer. 
		For example, if foo is a C pointer to an int, declared in your C program as
			int *foo;
		then you can use the corresponding gdb.Value to access what foo points to like this:
			bar = foo.dereference ()


#### Types In Python

gdb represents types from the inferior using the class gdb.Type.
The following type-related functions are available in the gdb module:

	gdb.lookup_type (name [, block])


#### Pretty Printing API

pretty printer就是一个对象，hold了一个value，并且实现了一组接口，这组接口是：

	pretty_printer.children (self)
		gdb调用这个返回pretty_print里面hold的值，它的返回值必须遵从python的iterator 协议. 
		每个iterator返回的item必须是一个元组，这个元组hold了两个值。第一个是name，第二个是value.
		The value can be any Python object which is convertible to a gdb value.
		这个方法是可选的，如果没实现这个方法，gdb就会认为这个Value没有成员变量
		
	pretty_printer.display_hint (self)
		This method is optional. If it does exist, this method must return a string.
		Some display hints are predefined by gdb:
		‘array’:

	pretty_printer.to_string (self)
		gdb will call this method to display the string representation 
		of the value passed to the object’s constructor.

	gdb.default_visualizer (value)
		This function takes a gdb.Value object as an argument.
		 If a pretty-printer for this value exists, then it is returned. 
		 If no such printer exists, then this returns None.

#### Selecting Pretty-Printers

gdb.pretty_printers是一个python list对象，里面包含了所有全局的pretty-printers.

Each function on these lists is passed a single gdb.Value argument and should return a pretty-printer object conforming to the interface definition above (see Section 23.2.2.5 [Pretty Printing API], page 332). If a function cannot create a pretty-printer for the value, it should return None.		 						
				#### Writing a Pretty-Printer
一个pretty-printer包含了两部分：一个lookup函数，还有printer
一个打印std::string的例子.
printer实现：
	class StdStringPrinter(object):
    	"Print a std::string"
	    def __init__(self, val):
    	    self.val = val

	    def to_string(self):
    	    return self.val[’_M_dataplus’][’_M_p’]

	    def display_hint(self):
    	    return ’string’

lookup函数实现：

	def str_lookup_function(val):
    	lookup_tag = val.type.tag
	    if lookup_tag == None:
    	    return None
	    regex = re.compile("^std::basic_string<char,.*>$")
    	if regex.match(lookup_tag):
        	return StdStringPrinter(val)
	    return None	    	    


The example lookup function extracts the value’s type, and attempts to match it to a type that it can pretty-print. f it is a type the printer can pretty-print, it will return a printer object. If not, it returns None.


#### Type Printing API
gdb提供了一种显示type信息的方式。这对于显示type信息非常有用。

A type printer is just a Python object conforming to a certain protocol.A simple base class implementing the protocol is provided; 

	instantiate (self):
		This is called by gdb at the start of type-printing. 

	recognize (self, type):
		if type is not recognized, return None.
		Otherwise, return a string which is to be printed as the name of type. 
		The type argument will be an instance of gdb.Type

#### Filtering Frames

Frame filters are Python objects that manipulate the visibility of a frame or frames when a backtrace is printed by gdb.				


#### Decorating Frames


#### Writing a Frame Filter


#### Xmethods In Python

Xmethods are additional methods or replacements for existing methods of a C++ class.
This feature is useful for those cases where a method defined in C++ source code could be inlined or optimized out by the compiler, making it unavailable to gdb.
For such cases, one can define an xmethod to serve as a replacement for the method defined in the C++ source code.
gdb will then invoke the xmethod, instead of the C++ method, to evaluate expressions.
One can also use xmethods when debugging with core files. 
Moreover, when debugging live programs, invoking an xmethod need not involve running the inferior (which can potentially perturb its state)
Hence, even if the C++ method is available, it is better to use its replacement xmethod if one is defined.


#### Xmethod API


#### Writing an Xmethod


#### Inferiors In Python

#### Events In Python
gdb provides a general event facility so that Python code can be notified of various state changes, particularly changes that occur in the inferior.



#### Threads In Python
Python scripts can access information about, and manipulate inferior threads controlled by gdb, via objects of the gdb.InferiorThread class.


#### Commands In Python

#### Parameters In Python
You can implement new gdb parameters using Python.
Parameters are exposed to the user via the set and show commands.

here are many parameters that already exist and can be set in gdb.
Two examples are: set follow fork and set charset. 
Setting these parameters influences certain behavior in gdb. 
Similarly, you can define parameters that can be used to influence behavior in custom Python scripts and commands.

#### Writing new convenience functions
You can implement new convenience functions  in Python.

#### Program Spaces In Python

A program space, or progspace, represents a symbolic view of an address space.
It consists of all of the objfiles of the program.

#### Objfiles In Python

#### Accessing inferior stack frames from Python.

#### Accessing blocks from Python.In gdb, symbols are stored in blocks. A block corresponds roughly to a scope in the source code. Blocks are organized hierarchically, and are represented individually in Python as a gdb.Block.Blocks rely on debugging information being available.
#### Python representation of Symbols.
gdb represents every variable, function and type as an entry in a symbol table.
Similarly, Python represents these symbols in gdb with the gdb.Symbol object.
#### Symbol table representation in Python.
#### Manipulating line tables using Python
#### Manipulating breakpoints using Python
#### Finish Breakpoints
### Python Auto-loading
When a new object file is read(for example, due to the file command, or because the inferior has loaded a shared library)gdb will look for Python support scripts in several ways: ‘objfile-gdb.py’ and .debug_gdb_scripts section.
The auto-loading feature is useful for supplying application-specific debugging commands and scripts
Auto-loading can be enabled or disabled, and the list of auto-loaded scripts can be printed.
When reading an auto-loaded file, gdb sets the current objfile. This is available via the gdb.current_objfile function.
This can be useful for registering objfile-specific pretty-printers and frame-filters.
### Python modules
gdb comes with several modules to assist writing Python code.
#### gdb.printing
#### gdb.types
#### gdb.prompt


## Extending gdb using Guile

## Auto-loading extensions
gdb provides two mechanisms for automatically loading extensions when a new object file is read (for example, due to the file command, or because the inferior has loaded a shared library): ‘objfile-gdb.ext’ and the .debug_gdb_scripts section of modern file formats like ELF.

The auto-loading feature is useful for supplying application-specific debugging commands and features.

Auto-loading can be enabled or disabled, and the list of auto-loaded scripts can be printed. 

### The ‘objfile-gdb.ext’ file
When a new object file is read, gdb looks for a file named ‘objfile-gdb.ext’ 
where objfile is the object file’s name and where ext is the file extension for the extension language:

		‘objfile-gdb.gdb’:
		GDB’s own command language
	‘objfile-gdb.py’:
		Python
		‘objfile-gdb.scm’						Guile
If this file exists and is readable, gdb will evaluate it as a script in the specified extension language.
If this file does not exist, then gdb will look for script-name file in all of the directories as specified below.		


### The .debug_gdb_scripts section

### Which flavor to choose?

## Multiple Extension LanguagesThe Guile and Python extension languages do not share any state, and generally do not interfere with each other. There are some things to be aware of, however.
### Python comes first
## Creating new spellings of existing commands








	
		    	
						

				
				
		



























































	
		
			
			

						





















				
		


				
				
				