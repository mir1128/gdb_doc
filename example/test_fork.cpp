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

