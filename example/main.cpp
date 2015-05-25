/*
 * =====================================================================================
 *
 *       Filename:  main.cpp
 *
 *    Description: test gdb usage 
 *
 *        Version:  1.0
 *        Created:  05/22/2015 09:25:38
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  YOUR NAME (), 
 *        Company:  
 *
 * =====================================================================================
 */
#include <iostream>
using namespace std;


struct s
{
    int a;
    int b;
};

void func()
{
    int* p = NULL;
    *p = 10;
}

double bubble(double, double)
{
    return 0;
}

int bubble(int, int )
{
    return 0;
}

int main()
{
    struct s s1;
    s1.a = 10;
    func();
    return 0;
}    
