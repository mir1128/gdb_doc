# Running programs backward

倒回去，重新执行!

如果调试目标支持，可以尝试以下命令：

	reverse-continue [ignore-count]
	rc [ignore-count]
		Beginning at the point where your program last stopped, start executing in reverse. 
		Reverse execution will stop for breakpoints and synchronous exceptions (signals), 
		just like normal execution. Behavior of asynchronous signals depends 
		on the target environment.
	
	reverse-step [count]
	reverse-stepi [count]
	reverse-next [count]
	reverse-nexti [count]
	reverse-finish
	set exec-direction
		Set the direction of target execution.
	set exec-direction reverse
	set exec-direction forward
	
sddsf	
	
				