# Tracepoints

对于一些应用程序实时性很强，被调试器挂接后由于中断时间较长会影响程序执行的结果。观察一个程序而不中断它有时是非常有用的。

Using gdb’s trace and collect commands, you can specify locations in the program, called tracepoints, and arbitrary expressions to evaluate when those tracepoints are reached.

用`trace`和`collect`命令，可以在指定位置设置tracepoint，在这些点上设置好表达式，当程序执行到跟踪点时会计算这些表达式的值。然后使用`tfind`命令，你可以查看表达式的值。

The expressions may also denote objects in memory— structures or arrays, for example—whose values gdb should record; while visiting a partic- ular tracepoint, you may inspect those objects as if they were in memory at that moment. However, because gdb records these values without interacting with you, it can do so quickly and unobtrusively, hopefully not disturbing the program’s behavior.


The tracepoint facility is currently available only for remote targets. ????
(只支持remote对象？)

It is also possible to get trace data from a file, in a manner reminiscent of corefiles; you specify the filename, and use tfind to search through the file.


## Commands to Set Tracepoints

1. tracepoint没有数量上的限制,多少都可以.tracepoint实际上是一种特殊的断点。所以标准断点的命令都可以用。tracepoint的编号也是连续增加的。许多命令用tracepoint的编号作为参数。
2. 对于每个tracepoint，当代码执行到的时候，可以随意采集数据,包括：寄存器，局部变量，全局变量.采集完后可以用gdb命令来查看
3. tracepoint不是支持所有的断点特性，比如ignore, 断点命令也不好用. 而且不是现成绑定的。
4. 一些调试目标不支持fast tracepoint, 他们采用一种不同的实现方式（使用jmp指令，而不是trap）.这样可能速度更快，但是在安装时可能被限制住。

### Create and Delete Tracepoints

	trace location
		# 定义了一个tracepoint,在一个tracepoint程序会短暂的停住，收集一些数据，然后允许程序继续执行。
		
	trace location if cond
		# 条件tracepoint

	ftrace location [ if cond ]
		# The ftrace command sets a fast tracepoint.
		# fast tracepoints will use a more
		
	strace location [ if cond ]
		# The strace command sets a static tracepoint.
		# setting a static tracepoint probes a static instrumentation point, 
		or marker, found at location.		

	delete tracepoint [num]		

### Enable and Disable Tracepoints
	disable tracepoint [num]			
	enable tracepoint [num]
### Tracepoint Passcounts
	passcount [n [num]]
		# 只有第n次才停下记录
		
	
例子
		(gdb) passcount 5 2 // Stop on the 5th execution of // tracepoint 2	(gdb) passcount 12 // Stop on the 12th execution of the 						// most recently defined tracepoint.	(gdb) trace foo 	(gdb) pass 3 	(gdb) trace bar 	(gdb) pass 2 	(gdb) trace baz 	(gdb) pass 1			// Stop tracing when foo has been // executed 3 times OR when bar has			// been executed 2 times			// OR when baz has been executed 1 time.
					### Tracepoint Conditions
### Trace State Variables
A trace state variable is a special type of variable that is created and managed by target-side code.The syntax is the same as that for GDB’s convenience variables.but they are stored on the target. They must be created explicitly, using a tvariable command. They are always 64-bit signed integers.
Trace state variables are remembered by gdb, and downloaded to the target along with tracepoint information when the trace experiment starts. There are no intrinsic limits on the number of trace state variables, beyond memory limitations of the target.
	tvariable $name [ = expression ]
		#The tvariable command creates a new trace state variable named $name, 
		and optionally gives it an initial value of expression. 
		The expression is evaluated when this command is entered; 
		the result will be converted to an integer if possible, 
		otherwise gdb will report an error. 
		A subsequent tvariable command specifying the same name does not create a variable,
		but instead assigns the supplied initial value to the existing variable of that name,
		overwriting any previous initial value. The default initial value is 0.

	info tvariables
		List all the trace state variables along with their initial values. 
		Their current values may also be displayed,
		if the trace experiment is currently running.

	delete tvariable [ $name ... ]
		Delete the given trace state variables, 
		or all of them if no arguments are speci- fied.

### Tracepoint Action Lists			

	actions [num]
		#one action at a time, and terminate the actions list with a line containing just end.
		So far, the only defined actions are collect, teval, and while-stepping.

	collect[/mods] expr1, expr2, ...
		$regs Collect all registers.
		$args Collect all function arguments.
		$locals Collect all local variables.
		$_ret Collect the return address. 
		This is helpful if you want to see more of a backtrace.
		$_probe_argc
		$_probe_argn
		$_sdata

	teval expr1, expr2, ...				
		Evaluate the given expressions when the tracepoint is hit.
		The results are discarded, 
		so this is mainly useful for assigning values to trace state variables

	while-stepping n
	
	set default-collect expr1, expr2, ...
	
### Listing Tracepoints

	info tracepoints [num...]

### Listing Static Tracepoint Markers
	
	info static-tracepoint-markers

### Starting and Stopping Trace Experiments

	tstart
		This command starts the trace experiment, and begins collecting data. 
		It has the side e↵ect of discarding all the data collected 
		in the trace bu↵er during the previous trace experiment. 

	tstop
		This command stops the trace experiment. 
		If any arguments are supplied, they are recorded with the experiment as a note.

	tstatus
		This command displays the status of the current trace data collection.

the variable `disconnected-tracing` lets you decide whether the trace should continue running without gdb.						

	set disconnected-tracing on
	set disconnected-tracing off
	show disconnected-tracing

When you reconnect to the target, the trace experiment may or may not still be running; it might have filled the trace bu↵er in the meantime, or stopped for one of the other reasons. If it is running, it will continue after reconnection.

Upon reconnection, the target will upload information about the tracepoints in e↵ect. gdb will then compare that information to the set of tracepoints currently defined, and attempt to match them up, allowing for the possibility that the numbers may have changed due to creation and deletion in the meantime. If one of the target’s tracepoints does not match any in gdb, the debugger will create a new tracepoint, so that you have a number with which to specify that tracepoint. This matching-up process is necessarily heuristic, and it may result in useless tracepoints being created; you may simply delete them if they are of no use.

If your target agent supports a circular trace bu↵er, then you can run a trace experiment indefinitely without filling the trace bu↵er; when space runs out, the agent deletes already- collected trace frames, oldest first, until there is enough room to continue collecting. This is especially useful if your tracepoints are being hit too often, and your trace gets termi- nated prematurely because the bu↵er is full. To ask for a circular trace bu↵er, simply set ‘circular-trace-buffer’ to on. You can set this at any time, including during tracing; if the agent can do it, it will change bu↵er handling on the fly, otherwise it will not take e↵ect until the next run.

	set circular-trace-buffer on
	set circular-trace-buffer off
		show circular-trace-buffer
	set trace-buffer-size n
	set trace-buffer-size unlimited
	
	show trace-buffer-size

### Tracepoint Restrictions


## Using the Collected Data

After the tracepoint experiment ends, you use gdb commands for examining the trace data.
The basic idea is that each tracepoint collects a trace snapshot every time it is hit and another snapshot every time it single-steps.All these snapshots are consecutively numbered from zero and go into a bu↵er, and you can examine them later.The way you examine them is to focus on a specific trace snapshot.

When the remote stub is focused on a trace snapshot, it will respond to all gdb requests for memory and registers by reading from the bu↵er which belongs to that snapshot, rather than from real memory or registers of the program being debugged. 

This means that all gdb commands (print, info registers, backtrace, etc.) will behave as if we were currently debugging the program state as it was when the tracepoint occurred. Any requests for data that are not in the bu↵er will fail.


### tfind n

	tfind start
	tfind none
	tfind end
	tfind
	tfind tracepoint num
	tfind -
	tfind pc addr
	tfind outside addr1, addr2
	tfind range addr1, addr2
	tfind line [file:]n
	
例子：

	(gdb) tfind start	(gdb) while ($trace frame != -1)	> printf "Frame %d, PC = %08X, SP = %08X, FP = %08X\n", \                $trace_frame, $pc, $sp, $fp	> tfind > end	
	Frame 0, PC = 0020DC64, SP = 0030BF3C, FP = 0030BF44    Frame 1, PC = 0020DC6C, SP = 0030BF38, FP = 0030BF44    Frame 2, PC = 0020DC70, SP = 0030BF34, FP = 0030BF44    Frame 3, PC = 0020DC74, SP = 0030BF30, FP = 0030BF44    Frame 4, PC = 0020DC78, SP = 0030BF2C, FP = 0030BF44    Frame 5, PC = 0020DC7C, SP = 0030BF28, FP = 0030BF44    Frame 6, PC = 0020DC80, SP = 0030BF24, FP = 0030BF44    Frame 7, PC = 0020DC84, SP = 0030BF20, FP = 0030BF44    Frame 8, PC = 0020DC88, SP = 0030BF1C, FP = 0030BF44    Frame 9, PC = 0020DC8E, SP = 0030BF18, FP = 0030BF44
### tdump
This command takes no arguments. It prints all the data collected at the current trace snapshot.
	(gdb) trace 444	(gdb) actions	Enter actions for tracepoint #2, one per line: 	> collect $regs, $locals, $args, gdb_long_test 	> end
		(gdb) tstart
	(gdb) tfind line 444
	#0 gdb_test (p1=0x11, p2=0x22, p3=0x33, p4=0x44, p5=0x55, p6=0x66)
	at gdb_test.c:444
	444 printp( "%s: arguments = 0x%X 0x%X 0x%X 0x%X 0x%X 0x%X\n", )

	(gdb) tdump
	Data collected at tracepoint 2, trace frame 1:
	￼d0             0xc4aa0085
	d1 0x18 24
	d2 0x80 128
	d3 0x33 51
	d4 0x71aea3d
	d5 0x22 34
	d6 0xe0 224
	d7             0x380035 3670069
	a0             0x19e24a 1696330
	a1 0x3000668
	a2 0x100 256
	a3             0x322000 3284992
	a4 0x3000698
	a5             0x1ad3cc 1758156
	fp 0x30bf3c 0x30bf3c sp 0x30bf34 0x30bf34 ps 0x00
	pc 0x20b2c8 0x20b2c8 fpcontrol 0x0 0 fpstatus 0x0 0 fpiaddr 0x0 0
	p = 0x20e5b4 "gdb-test"
	p1 = (void *) 0x11
	p2 = (void *) 0x22
	p3 = (void *) 0x33
	p4 = (void *) 0x44	
	

### save tracepoints filename

This command saves all current tracepoint definitions together with their actions and pass- counts, into a file ‘filename’ suitable for use in a later debugging session. 



## Convenience Variables for Tracepoints

	$trace_frame
	$tracepoint
	$trace_line	
	$trace_file
	$trace_func

## Using Trace Files
In some situations, the target running a trace experiment may no longer be available; perhaps it crashed, or the hardware was needed for a di↵erent activity. To handle these cases, you can arrange to dump the trace data into a file, and later use that file as a source of trace data, via the target tfile command.

	tsave [ -r ] filename
	tsave [-ctf] dirname
	target tfile filename
	target ctf dirname
	
			    



































		
						
				
				
		


						






