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




































	
	
	      					            
            					

	
	 
	
	