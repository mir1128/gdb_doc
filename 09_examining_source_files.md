# Examining Source Files

## Printing Source Lines
	
	list linenum
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
	
You can customize gdb to use any editor you want1. By default, it is ‘/bin/ex’, but you can change this by setting the environment variable EDITOR before using gdb. For example, to configure gdb to use the vi editor, you could use these commands with the sh shell:



	search regexp
	reverse-search regexp

## Specifying Source Directories


可执行文件一般不记录源文件的路径，只记录源文件的名字。即使记录了，目录也可能会发生变化，gdb有一个源文件目录列表，调试时在这个目录列表中查找源文件。这个叫做source path. 

加入gdb需要访问`/usr/src/foo-1.0/lib/foo.c`这个文件，我们的源码路径为`/mnt/cross`.
首先会按照字面解析这个文件，试图访问：`/mnt/cross/usr/src/foo-1.0/lib/foo.c`，如果失败了，再尝试`/mnt/cross/foo.c`,如果还是失败，就会打印一个error message.
	
不会查找子目录

不会查找可执行文件目录


When you start gdb, its source path includes only ‘cdir’ and ‘cwd’, in that order. To



	directory dirname ... 
	dir dirname ...
	directory
	set directories path-list
	show directories
	set substitute-path from to
		#For example, if the file ‘/foo/bar/baz.c’ was moved to ‘/mnt/cross/baz.c’, 
		then the command
		
		(gdb) set substitute-path /usr/src /mnt/cross

	For instance, if we had entered the following commands:








	info line linespec

For example, we can use info line to discover the location of the object code for the first line of function m4_changequote:









	


















































	