# Recording Inferior’s Execution and Replaying It

On some platforms, gdb provides a special process record and replay target that can record a log of the process execution, and replay it later with both forward and reverse execution commands.
（这个需要再查一下）

	record method
		#This command starts the process record and replay target. 如果不指定参数，默认是full
		full: Full record/replay recording using gdb’s software record 
		    and re- play implementation. This method allows replaying and reverse execution.
		btrace: 
			#Hardware-supported instruction recording. This method does not record data. 
			Further, the data is collected in a ring bu↵er so old data will 
			be overwritten when the bu↵er is full. 
			It allows limited replay and reverse execution.
			This recording method may not be available on all processors.

The process record and replay target can only debug a process that is already running.Therefore, you need first to start the process with the run or start commands, and then start the recording with the record method command.
Both record method and rec method are aliases of target record-method.	record stop
	record goto
	record save filename
	record restore filename
	set record full insn-number-max limit
	set record full insn-number-max unlimited
	show record full insn-number-max
	set record full stop-at-limit
	show record full stop-at-limit
	set record full memory-query
	
	show record full memory-query
		set record btrace replay-memory-access
	show record btrace replay-memory-access
	info record
	record delete
	record instruction-history
	set record instruction-history-size size
	
			
		ds
			
								    
