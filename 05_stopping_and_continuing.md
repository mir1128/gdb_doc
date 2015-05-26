# Stopping and Continuing

	info program
	# Display information about the status of your program: whether it is running or not, what process it is, and why it stopped.
	

## Breakpoints, Watchpoints, and Catchpoints

1. breakpoints	

通常意义上的断点。可以给断点加上条件变成条件断点。可以用文件行号，函数名，或者地址做断点参数。一些系统可以给动态链接库设置断点。

2. watchpoint

watchpoint也叫数据断点，它可以是一个表达式，当这个表达式的值发生变化的时候就会断住。可以让变量在断住的时候自动显示。

3. catchpoint 

异常或者事件断点。可以在发生c++异常，或者动态库加载事件时候断住。阻止程序收到信号，可以用signal命令。

每个断点都有一个从1开始的编号，可以用一个短点号的范围，如:5-7

### Setting Breakpoints

	break location
	
	break ... if cond
	
	tbreak args   #只断住一次，当执行过1次以后这个断点就会自动被删除。args同break一样。
		hbreak args #硬件断点，需要硬件支持（有什么用？）The main purpose of this is EPROM/ROM code debugging, so you can set a breakpoint at an instruction without changing the instruction.
	thbreak args #Set a hardware-assisted breakpoint enabled only for one stop.
	rbreak regex #Set breakpoints on all functions matching the regular expression regex.	The syntax of the regular expression is the standard one used with tools like ‘grep’. 
	rbreak file:regex
	info breakpoints [n...]
 	info break [n...] 会显示一个断点被断住的次数。这个特点配合ignore命令特别有用。可以先设置一个很大的ignore数字，然后info break查看断点被hit了多少次，然后再次执行，ignore次数比最多调用次数少一次。这样就可以看到最后一次该断点断住的时候发生了什么。
	
一个位置可以有多个断点，一个断点可以对应多个位置，原因是：

1. Multiple functions in the program may have the same name.
2. For a C++ constructor, the gcc compiler generates several instances of the functionbody, used in different cases.
3. ForaC++templatefunction,agivenlineinthefunctioncancorrespondtoanynumber of instantiations.
4. Foraninlinedfunction,agivensourcelinecancorrespondtoseveralplaceswherethat function is inlined.

调试动态链接库是很常见的事情，为了支持调试动态链接库，gdb在动态链接库加载或者卸载的时候会update断点信息。通常你在程序启动的时候设置断点信息，这时动态库还没有加载，动态库里的符号还不可用,此时设置断点，gdb会寻味是否设置pending breakpoint.

gdb normally implements breakpoints by replacing the program code at the breakpoint address with a special instruction, which, when executed, given control to the debugger.
gdb实现断点的原理是在断点的地方设置一条特殊的指令，当执行到这里的时候，把控制权交给调试器。默认的，当程序继续运行时就把它改成特殊指令，当程序停止时就改回成正常指令。This behaviour guards against leaving breakpoints inserted in the target should gdb abrubptly disconnect.However, with slow remote targets, inserting and removing breakpoint can reduce the performance. This behavior can be controlled with the following commands::

	set breakpoint always-inserted off
		所有断点都是在程序恢复执行的时候才插入进去。当程序停止时所有断点都被移除了。这是默认的行为。
		
	set breakpoint always-inserted on
		断点一直都在程序里，如果用户新加一个断点，或者更改一个已经存在的断点，目标文件中的指令立即被更新。
		
		set breakpoint condition-evaluation host	
	set breakpoint condition-evaluation target
	set breakpoint condition-evaluation auto
	
### Setting Watchpoints
可以给一个未初始化的变量设置数据断点。例如，你可以给在global_ptr初始化之前给*global_ptr设置断点。当它被初始化的时候gdb就会停住。
	watch [-l|-location] expr [thread threadnum] [mask maskvalue]
		#The simplest (and the most popular) use of this command 
		is to watch the value of a single variable:
		(gdb) watch foo
		如果给后面再加上一个线程号，那么只有当这个线程改变该变量时才会断住，其他线程修改这个变量的时候不会断住。
		这种方只有硬件断点才支持。
		A masked watchpoint specifies a mask in addition to an address to watch.
		The mask specifies that some bits of an address
		 (the bits which are reset in the mask) should be ignored 
		 when matching the address accessed by the inferior against the watchpoint ad- dress.
		 	(gdb) watch foo mask 0xffff00ff            (gdb) watch *0xdeadbeef mask 0xffffff00
	rwatch [-l|-location] expr [thread threadnum] [mask maskvalue]
		Set a watchpoint that will break when the value of expr is read by the program.
	
	awatch [-l|-location] expr [thread threadnum] [mask maskvalue]
		Set a watchpoint that will break when expr is either read from 
		or written into by the program.		
	info watchpoints
		This command prints a list of watchpoints, using the same format as info break
		
	如果想watch一个地址，需要解引用，以为地址只是一个常数。
		(gdb) watch 0x600850      		Cannot watch constant value 0x600850.      	(gdb) watch *(int *) 0x600850      		Watchpoint 1: *(int *) 6293584		

	GDB首先尝试设置硬件断点，硬件断点执行快。而且当变化发生的时候立刻断住。如果不能设置硬件断点才尝试软件断点，软件断点执行较慢，而且是在执行下一条指令之前才断住,此时数值已经变化了。(一个是在数值变化前，一个是数值变化后。)
	
可以用set can-use-hw- watchpoints 0 命令只使用软件断点。

	set can-use-hw-watchpoints
		Set whether or not to use hardware watchpoints.	show can-use-hw-watchpoints		Show the current mode of using hardware watchpoints.
如果是远程调试，可以限制硬件断点的数目。

一个设置硬件断点的例子:

	Breakpoint 1, main (argc=1, argv=0x7fff5fbff5e8) at test_fork.cpp:16
	16		pid = fork();
	(gdb) watch pid
	Hardware watchpoint 2: pid
	(gdb) c
	Continuing.
	this is the child process
	Hardware watchpoint 2: pid

	Old value = 0
	New value = 12923
	main (argc=1, argv=0x7fff5fbff5e8) at test_fork.cpp:17
	17		if (pid > 0)awatch和rwatch只支持硬件断点，因为只访问不修改只能通过检查指令来获悉。目前gdb还不能做到。

一些系统上watchpoint的局限:
如果被watch的变量地址跨度大，可能watch不了。Sometimes, gdb cannot set a hardware watchpoint because the data type of the watched expression is wider than what a hardware watchpoint on the target machine can handle. For example, some systems can only watch regions that are up to 4 bytes wide; on such sys- tems you cannot set hardware watchpoints for an expression that yields a double-precision floating-point number (which is typically 8 bytes wide). As a work-around, it might be pos- sible to break the large region into a series of smaller ones and watch them with separate watchpoints.		
如果硬件断点设置的太多，可能不支持。
If you set too many hardware watchpoints, gdb might be unable to insert all of them when you resume the execution of your program. Since the precise number of active watch- points is unknown until such time as the program is about to be resumed, gdb might not be able to warn you about this when you set the watchpoints, and the warning will be printed only when the program is resumed:	**Hardware watchpoint num: Could not insert watchpoint**

watch一个比较复杂的表达式有时候也是不行的，因为变量太多耗尽了硬件断点的指标。
Watching complex expressions that reference many variables can also exhaust the re- sources available for hardware-assisted watchpoints. That’s because gdb needs to watch every variable in the expression with separately allocated resources.

在多线程环境中，硬件断点观察所有线程。
In multi-threaded programs, watchpoints will detect changes to the watched expression from every thread.


### Setting Catchpoints

	catch event
		Stop when event occurs. The event can be any of the following:
			throw [regexp]
			rethrow [regexp]
			catch [regexp]
		
			exception unhandled
			exec # 系统调用exec
			syscall 系统调用
			syscall [name | number] 
			fork
			vfork
			load [regexp] 
			unload [regexp]  #加载或者卸载动态链接库。
			signal [signal... | ‘all’] 
				#One reason that catch signal can be more useful than handle 
				is that you can attach commands and conditions to the catchpoint.
			tcatch event #只断住1次
							
			
catchpoint断住的时候， $_exception变量可用。里面保存了跑出的异常变量。
这个有一些限制。(用的时候回来查有哪些限制。)

关于syscall:

A call to or return from a system call, a.k.a. syscall. A syscall is a mechanism for application programs to request a service from the operating system (OS) or one of the OS system services. gdb can catch some or all of the syscalls issued by the debuggee, and show the related information for each syscall. If no argument is specified, calls to and returns from all system calls will be caught.

syscall 都有哪些？ 

name can be any system call name that is valid for the underlying OS. Just what syscalls are valid depends on the OS. On GNU and Unix systems, you can find the full list of valid syscall names on ‘/usr/include/asm/unistd.h’.

	(gdb) catch syscall [tab]
	Display all 297 possibilities? (y or n)
	_sysctl                 eventfd                 getitimer               lgetxattr               	munlock                 restart_syscall         setitimer               timer_create


				
一个syscall 例子：

	(gdb) c
	Continuing.

	Catchpoint 3 (call to syscall access), 0x00007ffff7df3537 in access () at ../sysdeps/unix/	syscall-template.S:81
	81	../sysdeps/unix/syscall-template.S: No such file or directory.

有哪些syscall？
通常会保存在一个xml文件里，如果没有xml文件，会是这样的：
      (gdb) catch syscall      warning: Could not open "syscalls/i386-linux.xml"      warning: Could not load the syscall XML file ’syscalls/i386-linux.xml’.      GDB will not be able to display syscall names.      Catchpoint 1 (syscall)      (gdb)	



### Deleting Breakpoints

	clear
	clear location
	clear function
	clear filename:function	clear linenum	clear filename:linenum
	delete [breakpoints] [range...]
	

### Disabling Breakpoints

	disable [breakpoints] [range...]
	enable [breakpoints] [range...]
	enable [breakpoints] once range...
	enable [breakpoints] count count range...
	enable [breakpoints] delete range...
	
### Break Conditions
		
条件断点还可以提供副作用，甚至可以调用你程序里的函数。这个可能会很有用，例如调用日志函数记录信息,或者调用自定义函数格式化某个数据结构。这个效果完全可预测，除非同一个位置还有其他的断点（如果这样的话，其他的断点有可能会先断住，然后就不检查这个条件断点了). 如果只是为了这个副作用，断点命令一般比条件断点更好用。

对于远程调试：

Breakpoint conditions can also be evaluated on the target’s side if the target supports it. Instead of evaluating the conditions locally, gdb encodes the expression into an agent expression (see Appendix F [Agent Expressions], page 659) suitable for execution on the target, independently of gdb. Global variables become raw memory locations, locals become stack accesses, and so forth.

普通断点和数据断点都支持条件设置，但是catch断点不支持。对于catch断点如果想设置条件，就需要使用condition命令.

	condition bnum expression
	#bnum 表示断点号。
	
	condition bnum
	# Remove the condition from breakpoint number bnum. 
	It becomes an ordinary unconditional breakpoint.
	
一种特别有用的场景就是在制定次数时才断住。由于这种场景太有用了，所以单独提供了一个命令来支持他。就是使用ignore指定忽略次数。每个断点都有一个ignore次数，大多数时候它的值都是0，因此没有什么作用，但如果是一个整数，每次就会减1，减少到0 的时候就会断住了。
	
	ignore bnum count
	
如果条件和ignore同时使用，那么会忽略condition。忽略次数够了以后才检查condition.
ignore count对于普通断点，数据断点，异常断点都有效。

### Breakpoint Command Lists

可以给断点设置一系列的命令，当它断住的时候就会执行这些命令。

	commands [range...]
		... command-list ...
	end
	
	如果想取消这些命令：
	
	commands [range...]
	end
	
The commands echo, output, and printf allow you to print precisely controlled output.
and are often useful in silent breakpoints.
For example, here is how you could use breakpoint commands to print the value of x at entry to foo whenever x is positive.

	break foo if x>0      commands      silent      printf "x is %d\n",x      cont	end

另外一种使用场景：

One application for breakpoint commands is to compensate for one bug so you can test for another. Put a breakpoint just after the erroneous line of code, give it a condition to detect the case in which something erroneous has been done, and give it commands to assign correct values to any variables that need them. End with the continue command so that your program does not stop, and start with the silent command so that no output is produced. Here is an 
	
	example:      break 403      commands      silent      set x = y + 4      cont	end	
### Dynamic Printf
动态打印命令dprintf可以在断点处打印数据内容，效果类似printf.
最简单的形式是打印到标准输出，但是你可以设置 **dprintf-style**变量用不同的方式来处理输出。例如你可以调用你自己实现的printf函数。这样就可以重定向输出位置了。
if you are doing remote debugging with a stub or agent, you can also ask to have the printf handled by the remote agent. In addition to ensuring that the output goes to the remote program’s device along with any other output the program might produce, you can also ask that the dprintf remain active even after disconnecting from the remote target. 
	dprintf location,template,expression[,expression...]
	set dprintf-style style
		#Set the dprintf output to be handled in one of several di↵erent 
		styles enumerated below. 
		A change of style a↵ects all existing dynamic printfs immediately. 
		(If you need individual control over the print commands, 
		simply define normal breakpoints with explicitly-supplied command lists.)
		
		gdb
		call
		agent #Have the remote debugging agent (such as gdbserver) handle the output itself. 
			  This style is only available for agents that support 
			  running commands on the target
			  
		set dprintf-function function
			#Set the function to call if the dprintf style is call.
			By default its value is printf. You may set it to any expression. 
			that gdb can evaluate to a function, as per the call command.
			
		set dprintf-channel channel

	set disconnected-dprintf on
	set disconnected-dprintf off
	show disconnected-dprintf off

一个使用dprintf的例子：

As an example, if you wanted dprintf output to go to a logfile that is a standard I/O stream assigned to the variable mylog, you could do the following:	
	(gdb) set dprintf-style call    (gdb) set dprintf-function fprintf	(gdb) set dprintf-channel mylog	(gdb) dprintf 25,"at line 25, glob=%d\n",glob	Dprintf 1 at 0x123456: file main.c, line 25.	(gdb) info break    	1       dprintf        keep y   0x00123456 in main at main.c:25        	call (void) fprintf (mylog,"at line 25, glob=%d\n",glob)            continue           	(gdb)					
### How to save breakpoints to a file
		save breakpoints [filename]           	
		# To read the saved breakpoint definitions, use the source command

就是把断点相关的命令保存到一个文本文件里，可以手动编辑里面的命令。

### Static Probe Points			

SDT stands for Statically Defined Tracing,

（这一节缺乏背景知识，相关资料

http://sourceware. org/systemtap/wiki/UserSpaceProbeImplementation 介绍了SDT实现原理

### Cannot insert breakpoints

数据断点太多了，disable或者delete掉一些。

### Breakpoint address adjusted...

断点打在了变量定义的地方，那个地方不产生指令，所以会将断点调整到离可执行代码最近的地方。

## Continuing and Stepping

如果是被信号导致程序停止，可以使用`handle`或者是`signal 0`恢复运行，或者可以单步调试handler

	continue [ignore-count]
	c [ignore-count]
	fg [ignore-count]
	
To resume execution at a di↵erent place, you can use return to go back to the calling function;or jump to go to an arbitrary location in your program.

	step
	step count
	next [count]

	set step-mode
	set step-mode on
	show step-mode
	
	finish
		#Continue running until just after function in the selected stack frame returns.
	until
	u 
		#Continue running until a source line past the current line, 
		in the current stack frame, is reached.
	
	until location
	u location
	
	advance location
		#Continue running the program up to the given location
	stepi
	stepi arg
	si 
		#An argument is a repeat count, as in step.

	nexti
	nexti arg
	ni
		#Execute one machine instruction, but if it is a function call, 
		proceed until thefunction returns.		

	set range-stepping
	show range-stepping

## Skipping Over Functions and Files

对于不感兴趣的函数或者是文件，可以用skip命令跳过他们。

例如：
	
	101	int func() 
	102	{	103    	foo(boring());	104    	bar(boring());	105	}假如想要调试func, foo和bar，但是不想调试boring,如果在103行step就会进入boring, 但如果用next,就会跳过foo和boring.
一种解决办法就是进入boring,然后finish. 但如果boring调用地方太多，这就显得很low.
比较好的办法是 `skip boring`， 这样以后再step就不会进入boring了.

也可以让gdb忽略一整个文件。例如`skip file boring.c`

	skip [linespec]
	skip function [linespec]
	skip file [filename]
	info skip [range]
	skip delete [range]
	skip enable [range]
	skip disable [range]

## Signals

GDB能检测到信号发生，你可以告诉gdb当信号发生的时候采取何种措施。
对于非出错信号，gdb直接忽略，如果是出错信号，gdb会立刻暂停程序。可以使用handle改变这些设置。

	info signals
	info handle
		# 查看各种信号的处理机制。
	info signals sig
	catch signal [signal... | ‘all’]
		#Set a catchpoint for the indicated signals.
	handle signal [keywords...]
		#keywords可以是：
		nostop
			#gdb should not stop your program when this signal happens. 
			It may still print a message telling you that the signal has come in.
		stop
			#gdb should stop your program when this signal happens. 
			This implies the print keyword as well
		print
			#gdb should print a message when this signal happens.
		noprint												#gdb should not mention the occurrence of the signal at all. 
			#This implies the nostop keyword as well.
		pass
		noignore
		nopass
		ignore

## Stopping and Starting Multi-thread Programs
	
有两种模式控制多线程程序的运行。默认使用all-stop模式,当一个线程遇到断点挺住了，其他线程也会停住。
一些targets还支持non-stop模式，在调试一个线程的时候，其他现成仍然继续运行。

### All-Stop Mode

在这种模式下，当断住的时候，所有线程都停止运行，这时可以切换线程。但是一旦恢复运行，所有线程都会开始运行。当单步执行的时候，实际上其他线程也是在运行的。GDB不能锁住其他线程让它们不运行，因为线程调度是由操作系统完成的。其他线程在当前线程运行一条语句这段时间里可能已经运行了多条语句。甚至，其他线程可能会断在一条语句中间。

当你执行了一次step以后，很可能发现程序断在了另一个线程，这是因为另一个线程比当前被调试的线程先遇到了断点，信号，或者异常。当GDB断住以后，它会自动切换到遭遇断点，信号或者异常的线程。如果发生了这种切换，gdb会提示你`Switching to Thread n`

有一些系统，你可以修改gdb的默认行为，可以锁住系统的线程调度,只允许被调试的线程运行。

	set scheduler-locking mode
		#If it is off, then there is no locking and any thread may run at any time.
		#If on, then only the current thread may run when the inferior is resumed. 
		The step mode optimizes for single-stepping; 
		it prevents other threads from preempting the current thread 
		while you are stepping, so that the focus of debugging does not change unexpectedly.
		Other threads only rarely (or never) get a chance to run when you step.
		They are more likely to run when you ‘next’ over a function call, 
		and they are completely free to run when you use commands like ‘continue’, 
		‘until’, or ‘finish’. 				
		However, unless another thread hits a breakpoint during its timeslice, 
		gdb does not change the current thread away from the thread that you are debugging.
		
	show scheduler-locking

一般当执行了continue,next或者step, GDB只允许当前inferior里面的线程继续运行。可以通过

	set schedule-multiple
改变行为。
	
	show schedule-multiple

### Non-Stop Mode

一些调试目标支持non-stop模式，在这种模式下，只有被调试线程的执行会被断住，其他线程不受影响，一直运行。这种模式对被调试进程的干扰最小。对于一些需要实时响应外部事件的程序，这种模式是非常合适的。

在non-stop模式下，只有一个线程断住的时候才会上报调试事件，跟all-stop模式不一样，其他线程根本不会停住。所以continue也只会影响当前线程，而不会影响其他线程。这让你可以随意控制线程的运行。例如：单步调试一个线程，让其他线程随意运行，单步调试一个现成，让其他线程都挂起，或者同时单步调试几个线程。

如果想使用non-stop模式，在attach到进程之前，执行以下命令：

	#If using the CLI, pagination breaks non-stop.
	set pagination off
	# Finally, turn it on!
	set non-stop on
	
	set non-stop on
		#Enable selection of non-stop mode.
	set non-stop off
		#Disable selection of non-stop mode.
	show non-stop		
		#Show the current non-stop enablement setting.

这几个命令指示告诉使用者 non-stop模式是否开启，而不是当前运行环境是否为non-stop模式。并且，能否开启non-stop模式需要在gdb启动或连接到目标时进行协商。不是所有的调试目标都是支持non-stop模式的，有时甚至你开启了non-stop模式，还是回到了all-stop模式。

在non-stop模式中，所有的命令都是针对当前线程的，也就是说continue只会让当前线程continue，如果想让所有线程continue,那么请使用`continue -a`

可以使用gdb在后台运行某个命令，而你可以去查看其他的线程。MI命令在non-stop模式下一直都是异步的（什么是MI命令？）

当在后台运行时，可以用`interrupt`挂起在后台运行的命令,`ctrl-c`终止一个前台运行的线程。如果是all-stop模式，整个进程都会stop,但是在non-stop模式，只有当前线程会断住，如果想让整个进程断住，使用interrupt -a

在non-stop模式下，其他线程如果断住，gdb不会自动切换到断住的线程。这是因为线程断住通知对于gdb命令解释器是异步的。				
	
					
### Background Execution					
gdb执行命令有两种方式：前台（同步的）和后台（异步的）.在前台模式gdb会等待程序运行到一个端点，然后提示执行另外一条命令。在后台模式中，GDB立刻显示提示符，你就可以再次输入一条命令了。

如果目标不支持异步模式，当你尝试使用异步命令时，gdb就会提示一个error message.

给命令增加一个&就可以后台运行了。例如continue& 或者c&后台执行的命令有：

	run
	attach
	step
	stepi
	next
	nexti
	continue
	finish
	until

后台执行non-stop模式下，调试多线程环境特别有用。	但是，在all-stop模式下，你也可以等待这些命令运行完毕再执行其他的命令。

用interrupt可以终止一个后台执行的命令。

	interrupt
	interrupt -a

### Thread-Specific Breakpoints

When your program has multiple threads you can choose whether to set breakpoints on all threads, or on a particular thread.

	break linespec thread threadno
	break linespec thread threadno if ...


### Interrupted System Calls

如果一个线程遇到断点断住了，另外一个线程此时正被一个系统调用block住，那么这个系统调用会提前返回。
This is a consequence of the interaction between multiple threads and the signals that gdb uses to implement breakpoints and other events that stop execution.

To handle this problem, your program should check the return value of each system call and react appropriately. This is good programming style anyways.For example, do not write code like this:

	sleep (10);

The call to sleep will return early if a di↵erent thread stops at a breakpoint or for some other reason.Instead, write this:
	int unslept = 10;    while (unslept > 0)    	unslept = sleep (unslept);	
A system call is allowed to return early, so the system is still conforming to its specifica- tion. But gdb does cause your multi-threaded program to behave di↵erently than it would without gdb.
Also, gdb uses internal breakpoints in the thread library to monitor certain events such as thread creation and thread destruction.When such an event happens, a system call in another thread may return prematurely, even though your program does not appear to stop.


### Observer Mode

如果想用nod-stop模式运行，并且不想让gdb干扰程序运行，就可以禁止一切调试器试图修改状态的行为，如写入内存，插入断点等。这是一个底层命令，可以拦截一切其他命令。

当所有这些都是off的，那么gdb就进入了一种观察者模式。为方便起见，只设置一下oberver就可以达到全部设置为off的目的，它还会顺带设置non-stop模式。

gdb不会帮你检测设置了一些矛盾的设置。如果你enable了may-insert-breakpoints，但是却disable了 may- write-memory， 那么设置断点时需要修改内存，这样设置断点还是会失败的。

	set observer on
	set observer off
	show observer
	
	set may-write-registers on
	set may-write-registers off
	show may-write-registers
	
	set may-write-memory on
	set may-write-memory off
	show may-write-memory
	
	
	set may-insert-breakpoints on
	set may-insert-breakpoints off
	show may-insert-breakpoints
	
	set may-insert-tracepoints
	
	set may-insert-fast-tracepoints
	
	set may-interrupt on

	


	
		

	
			
	
			

	
				






















	
	
	      					            
            					

	
	 
	
	