# Debugging Remote Programs
如果试图调试一台不能正常运行gdb的机器，远程调试就变得有用了。例如，你可以远程调试系统内核，或者一个不支持调试的系统。

gdb可以配置串口或者是tcp/ip协议支持远程调试。另外gdb自带串口协议（只为gdb写的，系统不支持）你可以使用这个协议写一个stub,这个stub运行在远程机器上和你的程序交互。

Other remote targets may be available in your configuration of gdb; use help target to list them.## Connecting to a Remote Target
On the gdb host machine, you will need an unstripped copy of your program, since gdb needs symbol and debugging information. Start up gdb as usual, using the name of the local copy of your program as the first argument.
gdb can communicate with the target over a serial line, or over an IP network using TCP or UDP. In each case, gdb uses the same protocol for debugging your program; only the medium carrying the debugging packets varies. The target remote command establishes a connection to the target. Its arguments indicate which medium to use:
	target remote serial-device
		#Use serial-device to communicate with the target. For example, 
		to use a serial line connected to the device named ‘/dev/ttyb’:
			target remote /dev/ttyb
		If you’re using a serial line, you may want to give gdb the ‘--baud’ option, 
		or use the set serial baud command	before the target command.
			
	target remote host:port
	target remote tcp:host:port
		target remote manyfarms:2828
		target remote :1234

	target remote udp:host:port
	target remote | command
	detach
	disconnect
	monitor cmd

## Sending files to a remote system

## Using the gdbserver Program
gdbserver is a control program for Unix-like systems, which allows you to connect your program with a remote gdb via target remote—but without linking in the usual debugging stub.

gdbserver is not a complete replacement for the debugging stubs, because it requires essentially the same operating-system facilities that gdb itself does.

In fact, a system that can run gdbserver to connect to a remote gdb could also run gdb locally!

gdbserver is sometimes useful nevertheless, because it is a much smaller program than gdb itself. It is also easier to port than all of gdb, so you may be able to get started more quickly on a new system by using gdbserver.

Finally, if you develop code for real-time systems, you may find that the tradeo↵s involved in real-time operation make it more convenient to do as much development work as possible on another system, for example by cross-compiling. You can use gdbserver to make a similar choice for debugging.

gdb and gdbserver communicate via either a serial line or a TCP connection, using the standard gdb remote serial protocol.

### Running gdbserver

在一个系统上运行gdbserver，你需要可执行程序的一个拷贝，还有所有它依赖的库。可执行程序可以没有符号文件，host会hadle所有的符号的。


To use the server, you must:
1. tell it how to communicate with gdb; 
2. the name of your program;
3.  the arguments for your program

The usual syntax is:

	target> gdbserver comm program [ args ... ]

一个例子：
comm is either a device name (to use a serial line), or a TCP hostname and portnumber, or - or stdio to use stdin/stdout of gdbserver. For example, to debug Emacs with the argument ‘foo.txt’ and communicate with gdb over the serial port ‘/dev/com1’:

	target> gdbserver /dev/com1 emacs foo.txt
	
gdbserver waits passively for the host gdb to communicate with it.

To use a TCP connection instead of a serial line:

	target> gdbserver host:2345 emacs foo.txt

#### Attaching to a Running Program
	target>	gdbserver --attach comm pid
	target> gdbserver --attach comm ‘pidof program‘

#### Multi-Process Mode for gdbserver
			













































								
