# Examining Source Files

## Printing Source Lines
	
	list linenum	list function
	list
	list -

You can change this using set listsize:

	set listsize count
	set listsize unlimited
	show listsize


## Specifying a Location

Here are all the di↵erent ways of specifying a code location that gdb understands:


## Editing Source Files	

	edit location

### Choosing your Editor
	
You can customize gdb to use any editor you want1. By default, it is ‘/bin/ex’, but you can change this by setting the environment variable EDITOR before using gdb. For example, to configure gdb to use the vi editor, you could use these commands with the sh shell:      EDITOR=/usr/bin/vi      export EDITOR      gdb ...or in the csh shell,	setenv EDITOR /usr/bin/vi	gdb ...
## Searching Source Files	
There are two commands for searching through the current source file for a regular expres- sion.
	forward-search regexp
	search regexp
	reverse-search regexp

## Specifying Source Directories


可执行文件一般不记录源文件的路径，只记录源文件的名字。即使记录了，目录也可能会发生变化，gdb有一个源文件目录列表，调试时在这个目录列表中查找源文件。这个叫做source path. 

加入gdb需要访问`/usr/src/foo-1.0/lib/foo.c`这个文件，我们的源码路径为`/mnt/cross`.
首先会按照字面解析这个文件，试图访问：`/mnt/cross/usr/src/foo-1.0/lib/foo.c`，如果失败了，再尝试`/mnt/cross/foo.c`,如果还是失败，就会打印一个error message.
	
不会查找子目录

不会查找可执行文件目录
重新制定源码路径时，gdb会清理已经cache的源文件信息。

When you start gdb, its source path includes only ‘cdir’ and ‘cwd’, in that order. Toadd other directories, use the directory command.The search path is used to find both program source files and gdb script files (read usingthe ‘-command’ option and ‘source’ command).
To define a source path substitu- tion rule, use the `set substitute-path` command
To avoid unexpected substitution results, a rule is applied only if the from part of the directory name ends at a directory separator. For instance, a rule substituting ‘/usr/source’ into ‘/mnt/cross’ will be applied to ‘/usr/source/foo-1.0’ but not to ‘/usr/sourceware/foo-2.0’.And because the substitution is applied only at the beginning of the directory name, this rule will not be applied to ‘/root/usr/source/baz.c’ either.

	directory dirname ... 
	dir dirname ...
	directory
	set directories path-list
	show directories
	set substitute-path from to
		#For example, if the file ‘/foo/bar/baz.c’ was moved to ‘/mnt/cross/baz.c’, 
		then the command
		
		(gdb) set substitute-path /usr/src /mnt/cross

	For instance, if we had entered the following commands:                  (gdb) set substitute-path /usr/src/include /mnt/include                  (gdb) set substitute-path /usr/src /mnt/src	gdb would then rewrite ‘/usr/src/include/defs.h’ into ‘/mnt/include/defs.h’ 	by using the first rule. However, 	it would use the second rule to rewrite ‘/usr/src/lib/foo.c’ into ‘/mnt/src/lib/foo.c’.
	
	unset substitute-path [path]			
	show substitute-path [path]
如果替换的目录已经失效，那么目录可能引起gdb混乱，可以使用下面两条规则解决：
1. Use directory with no argument to reset the source path to its default value.2. Use directory with suitable arguments to reinstall the directories you want in thesource path. You can add all the directories in one command.## Source and Machine Code
可以用`info line`命令将代码行和机器指令对应起来。还可以用`disassemble`显示反汇编.
You can use the command `set disassemble-next-line on` to set whether to disas- semble next source line when execution stops	

	info line linespec

For example, we can use info line to discover the location of the object code for the first line of function m4_changequote:
	(gdb) info line m4_changequote    Line 895 of "builtin.c" starts at pc 0x634c and ends at 0x6350.
还可以反过来，查看某个地址对应的代码行.
	(gdb) info line *0x63ff	Line 926 of "builtin.c" starts at pc 0x63e4 and ends at 0x6404.
	disassemble #显示纯汇编
	disassemble /m  #混合显示，同时显示源码和汇编
	disassemble /r 	#显示二进制指令
		start,end #the addresses from start (inclusive) to end (exclusive)
		start, +length #the addresses from start (inclusive) to start+length (exclusive).
		    	
	


















































		 				