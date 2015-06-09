#include <iostream>

int main()
{
	int *p = new int;
	*p = 10;
	delete p;
	return 0;
}
