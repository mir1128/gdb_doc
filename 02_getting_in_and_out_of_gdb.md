# getting in and out of gdb

##gdb启动相关

* 如何启动？ 直接调试一个程序

		gdb program

* 调试core文件

		gdb program core

* attach 到一个进程

		gdb program 1234

* 用args指定运行参数. 调试gcc，并且gcc的参数是后面的那些

		gdb --args gcc -O2 -c foo.c

* --silent 不打印那些警告信息

		gdb --silent
		
gdb启动的时候会把第一个参数作为符号文件（可执行文件，因为可执行文件里可能有符号）。等同于使用-se 参数。把第二个参数作为进程id而attach上去，或者作为core文件。 如果第二个参数是一个十进制数字，会首先尝试作为进程attach上去，如果失败则作为core文件解析。如果想直接作为core文件解析，可以这样：

	gdb some_execute ./12345
	

gdb启动时的一些选项:

**启动时选择文件**

	-command file
	-x file #Execute commands from file file. The contents of this file is evaluated exactly
			 as the source command would.		
		
	-eval-command command			 	
	-ex command #Execute a single gdb command. 这个命令可能会重复使用多次（需要再查一下这个命令）
	
	
	-init-command file
	-ix file  #Execute commands from file file before loading the inferior 
			 (but after loading gdbinit files).
			 
	
	-init-eval-command command				 
	-iex command #Execute a single gdb command before loading the inferior 
					(but after loading gdbinit files)
	
	-directory directory 
	-d directory	#Add directory to the path to search for source and script files.

	-r
	-readnow 立刻读取全部符号表，默认是只在需要的时候才读取。这样启动的时候虽然慢，但是调试起来快。
	
	
**启动时选择模式**
	
You can run gdb in various alternative modes—for example, in batch mode or quiet mode.

	-nx
	-n	Do not execute commands found in any initialization file. 
		There are three init files, loaded in the following order:
		
		1. system.gdbinit 它的位置由 "-with-system-gdbinit"这个配置项设置. gdb启动首先读取这个文件。
		在处理options之前处理这个文件
		2. ~/.gdbinit 这个文件紧随system.gdbinit
		3. ./.gdbinit 这个文件在选项处理完以后才被处理，但是如果有-x指定的命令文件，
		那么-x指定的命令文件最后处理
		
	-batch 批处理执行-x指定的命令文件. (查一下批处理执行的用途)
		   Batch mode may be useful for running gdb as a filter, 
		   for example to download and run a program on another computer; 
		   in order to make this more useful, the message:
		   	
		   		"Program exited normally."

	-cd directory 
	    Run gdb using directory as its working directory, instead of the current direc- tory.
	    
	-data-directory directory 
	-D directory	    
		Run gdb using directory as its data directory. 
		The data directory is where gdb searches for its auxiliary files

	--args 给被调试的可执行文件指定参数
	
	-baud bps 
	-b bps 远程调试时指定波特率。 （这个对于visual gdb是否有用？）
	
	-l timeout 远程调试时指定超时时间。
	
	-tty device
	-t device #Run using device for your program’s standard input and output.

	-tui #Activate the Text User Interface when starting. 
		 The Text User Interface man- ages several text windows on the terminal, 
		 showing source, assembly, regis- ters and gdb command outputs 

	-interpreter interp # Use the interpreter interp 
		for interface with the controlling program or device. 
		This option is meant to be set by programs 
		which communicate with gdb using it as a back end.(这个还不知道是干嘛的，下来查一下)

	-write #Open the executable and core files for both reading and writing. 
	       This is equiv- alent to the ‘set write on’ command inside gdb
	       (写一个core文件或者可执行文件有什么意义？)	-statistics #This option causes gdb to print statistics about time and memory usage 
	       after it completes each command and returns to the prompt.
	
	-configuration 	       		



**gdb的启动过程**

1. Sets up the command interpreter as specified by the command line
2. Reads the system-wide init file。 and executes all the commands in that file.
3. Reads the init file (if any) in your home directory1 and executes all the commands in that file.
4. Executes commands and command files specified by the ‘-iex’ and ‘-ix’ options in their specified order. 
5. Processes command line options and operands.
6. Readsandexecutesthecommandsfrominitfile(ifany)inthecurrentworkingdirectory
7. If the command line specified a program to debug, or a process to attach to, or a core file, gdb loads any auto-loaded scripts provided for the program or for its loaded shared libraries.
8. Executes commands and command files specified by the ‘-ex’ and ‘-x’ options in their specified order.
9. Reads the command history recorded in the history file. 




##gdb退出
	
	quit [expression]
	q

	An interrupt 不会导致gdb退出，但是会终止当前正在运行的gdb命令回到命令输入界面

	用detach可以结束attach


## Shell Commands	


调试时如果想执行shell命令，不需要退出gdb.

	!command-string #!和命令之间没有空格.
					如果设置了环境变量SHELL，那么会调用SHELL指定的shell，否则用默认的


## Logging Output	

	set logging on #打开日志
	set logging off #关闭日志
	set logging file file # 指定日志文件名，默认gdb.txt
	set logging overwrite [on|off] # 是否overwrite
	set logging redirect [on|off] #
	show logging #显示日志设置




























		
				
			   		

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	




