# Examining the Stack

The information is saved in a block of data called a stack frame. The stack frames are allocated in a region of memory called the call stack.

When your program stops, the gdb commands for examining the stack allow you to see all of this information.

When your program stops, gdb automatically selects the currently executing frame and describes it briefly, similar to the frame command

## Stack Frames

Some compilers provide a way to compile functions so that they operate without stack frames. (For example, the gcc option	‘-fomit-frame-pointer’ #generates functions without a frame.
这样做的主要目的是减少一些调用特别频繁的库函数运行时间。

GDB对这种情况支持有限，如果遇到这种情况， 如果是最内层调用，gdb还是可以识别出它的栈帧，如果不是最内层的就无能为力了。

		frame [framespec]
	select-frame
		#This is the silent version of frame.

## Backtraces

	backtrace
	bt
	
	The names where and info stack (abbreviated info s) are additional aliases for backtrace.
	
默认只显示当前线程的堆栈，如果想看其他现成的，用`thread apply`命令. `thread apply all backtrace`可以显示所有线程的堆栈


## Management of Frame Filters.

Frame filters are Python based utilities to manage and decorate the output of frames. 基于python的，用于美化栈帧显示的。

		info frame-filter
	disable frame-filter filter-dictionary filter-name
	enable frame-filter filter-dictionary filter-name
## Selecting a Frame
## Information About a Frame
	info frame
		
	
					