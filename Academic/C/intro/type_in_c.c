#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

#define PRINT_TYPE(var) _Generic((var), \
    int: "int",                         \
    float: "float",                     \
    double: "double",                   \
    char: "char",                       \
    default: "unknown")

int main()
{
    char x = 'i';
    printf("%s", PRINT_TYPE(x));
    return 0;
}