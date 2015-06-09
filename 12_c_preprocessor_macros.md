# C Preprocessor Macros

如果想让gdb支持宏调试，必须要添加特殊的编译参数.

让gdb支持宏，需要使用 dwarf格式

	gcc -gdwarf-2 -g3 sample.c -o sample
	
	gdb -nw sample

sd		