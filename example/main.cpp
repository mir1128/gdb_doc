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
#include <vector>
using namespace std;

struct SimpleStruct
{
    int i;
    double d;
};

struct ComplexStruct
{
    struct SimpleStruct * ss_p;
    int arr[10];
};

int main()
{
    std::cout << "begin" << std::endl;
    struct SimpleStruct ss = { 10, 1.11 };
    struct ComplexStruct cs = { &ss, { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 } };   

    std::vector<int> v;
    for (int i = 0; i < 10; ++i)
    {
        v.push_back(i);
    }

    std::cout << "end" << std::endl;
    return 0;
}    
