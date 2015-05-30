# Examining Data

用 print打印变量

	print expr
	print /f expr
	
如果不写expr，gdb就打印上次print的变量

`x`命令可以用指定的格式查看内存。

`ptype exp` 查看变量类型信息。

另一种查看变量内容的方法是使用explore命令。It o↵ers an interactive way to start at the highest level
of the data type of an expression. and explore all the way down to leaf scalar values/fields embedded in the higher level data types. 	

	explore arg
		#arg is either an expression (in the source language), 
		or a type visible in the current context of the program being debugged.










	set multiple-symbols mode
	show multiple-symbols
		#When mode is set to ask, the debugger always uses the menu when 
		an ambiguity is detected.

## Program Variables
	
If you wish, you can specify a static variable in a particular function or file by using the colon-colon (::) notation:		




	$1 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	(gdb) p *(cs.arr)@9
	$2 = {0, 1, 2, 3, 4, 5, 6, 7, 8}
	(gdb) p cs.arr
	$3 = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	(gdb) p /x cs.arr
	$4 = {0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9}		



	x addr
	x
	
		n, the repeat count
		f, the display format ((‘x’, ‘d’, ‘u’, ‘o’, ‘t’, ‘a’, ‘c’, ‘f’, ‘s’))
		u, the unit size
			The unit size is any of

 查看3调机器指令
 
	0x10000104a <main()+1178>:	jmpq   0x10000104f <main()+1183>
	0x10000104f <main()+1183>:	mov    -0x214(%rbp),%eax
	0x100001055 <main()+1189>:	add    $0x1,%eax		



		#Compare the data of a loadable section section-name in the executable 
		file of the program being debugged with the same section 
		in the target machine’s memory, and report any mismatches.
		With no arguments, compares all loadable sections. With an argument of -r, 
		compares all loadable read-only sections.

		Note: for remote targets, this command can be accelerated if the target 
		sup- ports computing the CRC checksum of a block of memory 


## Automatic Display				
	
	display expr
	display/fmt expr
	display/fmt addr
	undisplay dnums...
	delete display dnums...
	disable display dnums...
	enable display dnums...
	display				
	info display

## Print Settings

	set print address	
	set print address on
	set print address off
	show print address

## Pretty Printing

gdb provides a mechanism to allow pretty-printing of values using Python code

### Pretty-Printer Introduction

gdb打印一个变量的时候，首先看看有没有pretty-printer，如果有的花就用pretty-printer，否则用普通的print.

`info pretty-printer`可以打印当前已经有的pretty-printers，如果一个pretty-printers可以打印多个类型，那么它的子printer可以打印单独的类型。每个子pretty-printers都有它自己的名字。

格式是：

	printer-name ;subprinter-name.
	
Pretty-printers are installed by registering them with gdb。Typically they are auto- matically loaded and registered when the corresponding debug information is loaded, thus making them available without having to do anything special.

向gdb注册了以后，Pretty-printers就可以自动加载.

There are three places where a pretty-printer can be registered.(没有说那三个地方)


* 第一种是全局的，对所有的inferior都可用
* 第二种是针对某个程序的
* 第三种是objfile，需要加载和卸载。


### Pretty-Printer Example

Here is how a C++ std::string looks without a pretty-printer:

	(gdb) print s
	$1 = {


	$2 = "abcd"

### Pretty-Printer Commands

	info pretty-printer [object-regexp [name-regexp]]
	    #Print the list of installed pretty-printers. 
	    This includes disabled pretty-printers, which are marked as such.

	disable pretty-printer [object-regexp [name-regexp]]
	enable pretty-printer [object-regexp [name-regexp]]

例子：假如我们有三个pretty-printers:一个叫做library1.so 的so里面有foo这个类型的pretty-printers。library2.so里面有bar1，bar2两种类型的pretty-printers

	(gdb) info pretty-printer
		  bar1










would save in $foo the value contained in the object pointed to by object_ptr.




	set $i = 0



		(gdb) print $_exitcode
		$1 = void
		(gdb) print $_isvoid ($_exitcode)
		$2 = 1
		(gdb) run

		Returns one if the length bytes at the addresses given by buf1 and buf2 are equal. 		Otherwise it returns zero.

	$_regex(str, regex)
		#Returns one if the string str matches the regular expression regex. 
		Otherwise it returns zero.			
												







			
	














