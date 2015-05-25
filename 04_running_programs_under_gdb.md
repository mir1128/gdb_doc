# Running Programs Under Gdb

## 编译调试信息

增加调试信息使用-g 参数，这些调试信息被放到.o文件中。

调试信息包括变量和函数类型， 以及可执行文件中的地址和行号之间的对应关系。

gdb可以handle宏相关的信息.但是大多数编译器如果只是指定了-g选项是不会包含调试信息的。如果使用DWARF调试格式，并且指定了-g3编译选项，就可以查看宏相关的信息了。
（查一下DWARF是什么）

查一下gcc对于调试支持的选项
See Section “Options for Debugging Your Program or GCC” in Using the gnu Compiler Collection (GCC), for more information on gcc options affecting debug information.## Starting your Program
执行完run以后，gdb新建一个子进程，并且让那个进程运行你的程序。
影响子进程的四个方面：
1. The arguments.2. The environment.
3. The working directory.
4. The standard input and output.

（查一下exec-wrapper是否可以调试.so文件）

## Your Program’s Arguments

	set args #Specify the arguments to be used the next time your program is run. 			 If set args has no arguments, run executes your program with no arguments.
	show args #Show the arguments to give your program when it is started.
	
## Your Program’s Environment

## Your Program’s Working Directory

## Your Program’s Input and Output
	info terminal	#Displays information recorded by gdb about 					the terminal modes your program is using.
	run > outfile 可以将调试信息输出到outfile里
	tty 命令可以做为指定输出目标的命令。
	tty /dev/ttyb 将输出重定向/dev/ttyb’上					

## Debugging an Already-running Process

	attach process-id # This command attaches to a running process—one 
					 that was started outside gdb.
					 info files可以查看当前被调试文件的信息

	detach #detach When you have finished debugging the attached process, 
			you can use the detach command to release it from gdb control. 
			detach后的进行仍然会继续运行。

如果运行gdb以后，并且attach一个进程，然后这时退出gdb,那么将自动detach这个进程。但是如果执行了run命令，就kill了那个进程。

## Killing the Child Process

## Debugging Multiple Inferiors and Programs

在一个gdb session 里面调试多个进程，甚至调试多个进程里的不同线程。

inferior概念：

inferior表示了一个进程的状态信息，一般一个inferior对应一个进程，但即使没有进程inferior也可以存在。它可以在进程创建之前就存在，进程结束之后还可以保存着。通常每个inferior都有它自己的地址空间，每个inferior可以有多个进程在运行。用info inferiors命令可以查看当前session的inferior信息。



	(gdb) info inferiors
	Num  Description       Executable
	* 1    process 9285      /Users/jieliu/Documents/gdb/example/main	
	*表示当前正在运行的inferior
	
	inferior infno #让infno成为正在运行的inferior
	
用add-inferior和clone-inferior可以让多个可执行文件加入到当前的gdb session中。To remove inferiors from the debugging session use the remove-inferiors command.


	add-inferior [ -copies n ] [ -exec executable ]
	n 表示创建n份拷贝，如果不指定，默认是1，exec也可以不指定，那么就新建一个空的inferior，以后可以使用file再给它指定可执行文件。
	
	clone-inferior [ -copies n ] [ infno ]
	This is a conve- nient command when you want to run another instance of the inferior you are debugging.
	
		detach inferior infno
	kill inferiors infno
To be notified when inferiors are started or exit under gdb’s control use:
	set print inferior-events	set print inferior-events on	set print inferior-events off


## Debugging Programs with Multiple Threads

关于线程，gdb提供以下支持：

* automatic notification of new threads
* ‘**thread threadno**’, a command to switch among threads
* ‘info threads’, a command to inquire about existing threads
* ‘thread apply [threadno] [all] args’, a command to apply a command to a list of threads
* thread-specific breakpoints
* ‘set print thread-events’, which controls printing of messages on thread start andexit.
* ‘setlibthread-db-search-pathpath’,whichletstheuserspecifywhichlibthread_db to use if the default choice isn’t compatible with the program.

有新现成启停的时候，gdb会得到通知。

	thread threadno

这个命令可以切换线程.

gdb内建变量“$_thread”包含了当前线程号。这个变量在设置条件断点，命令脚本时比较有用。（怎么有用了？）

	thread apply [threadno | all] command
	
可以指定一个范围的线程号 thread apply 2-4 command

	thread name [name]

	thread find [regexp]
	
	(gdb) thread find 26688	Thread 4 has target id ’Thread 0x41e02940 (LWP 26688)’ (gdb) info thread 4    	Id   Target Id         Frame        4    Thread 0x41e02940 (LWP 26688) 0x00000031ca6cd372 in select ()		

	set print thread-events	set print thread-events on 	set print thread-events off	show print thread-events
	set libthread-db-search-path [path]


## Debugging Forks

如果是fork了一个进程，那么子进程会畅通无阻的运行，如果设置了一个断点，子进程运行到这个断点的时候会收到一个SIGTRAP信号，这个信号会导致子进程退出。测试程序：

	#include <sys/types.h>
	#include <unistd.h>
	#include <stdio.h>
	#include <sys/wait.h>

	static void sig_trap(int)
	{
		printf("\nreceive a signal interupt.\n");
	}



	int main(int argc, char *argv[])
	{
		pid_t pid;
		pid = fork();
		if (pid > 0)
		{
			execlp("ls", "ls", "-al", NULL);
		}
		else if (pid == 0)
		{
			signal(SIGTRAP, sig_trap);
			printf("this is the child process\n");
			_exit(0);
		}

		int status;
		if (waitpid(pid, &status, 0) < 0 ){
			printf("waitpid error.");
		}

		return 0;
	}

在子进程中打断点以后，子进程会异常退出。

如果想调试子进程，那么可以在fork之后加上sleep，然后ps 出子进程id,再attach上去.

如果想调试子进程，而不是父进程，可以用：

	set follow-fork-mode child/parent
	
	show follow-fork-mode
	
On Linux, if you want to debug both the parent and child processes, use the command 

	set detach-on-fork.	

	set detach-on-fork mode	
	
	show detach-on-fork
	

## Setting a Bookmark to Return to Later

有一些操作系统支持进程状态快照，这个叫做checkpoint.

	checkpoint 
		#Save a snapshot of the debugged program’s current execution state. 
		The checkpoint command takes no arguments, 
		but each checkpoint is assigned a small integer id, similar to a breakpoint id.

	info checkpoints
	restart checkpoint-id
	delete checkpoint checkpoint-id
	
回到先前的checkpoint以后，整个系统的状态都会被恢复，包括文件指针。对于已经写到文件中的内容不会恢复，但是文件指针会恢复到先前的位置，这样刚写入的内容就可以被覆盖了。对于读文件，文件指针会恢复到checkpoint的位置。

已经发送给打印机的是收不回来的。

回退回去以后进程的process id 就不同了。如果保存了process id 那么可能会受到影响。

### A Non-obvious Benefit of Using Checkpoints

(什么是address space randomization)			



	
					
	
	



















































































									 
			 



