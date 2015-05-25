#GDB Commands

1. 只输入命令的前几个字母(不会引发歧义)就能执行一条命令。
2. 重复执行上一条命令直接按回车即可
3. 用tab可以补全命令


## 命令的语法

命令名+参数

如： **step 5** 执行5次step

The Ctrl-o binding is useful for repeating a complex sequence of commands. This command accepts the current line, like RET, and then fetches the next line relative to the current line from the history for editing. (这个是干嘛的，需要再google一下)


	b 'bubble(加一个引号，然后用tab多次可以显示bubble函数的重载。
(弄明白文档里提到的M- ?是个什么东西)
还可以看一个结构体里面都有哪些成员
	p gdb_stdout. TAB
## getting help
	apropos args	
		#The apropos command searches through all of the gdb commands, 		and their documentation, for the regular expression specified in args. 		It prints out all matches found. For example:
		complete args				#The complete args command lists all the possible completions 		for the begin- ning of a command.
			info 
		info args 可以看当前帧的参数
		info registers
		info breakpoints
		
	show #In contrast to info, show is for describing the state of gdb itself. 


sdfsdf			
		
				