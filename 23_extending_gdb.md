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

		 				
		



























				
		


				
				