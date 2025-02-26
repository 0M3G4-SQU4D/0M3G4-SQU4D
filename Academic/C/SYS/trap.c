#include <stdio.h>

struct test
{
    char a;
    unsigned int b : 5, c : 4, d : 21; // b is 5 bit int
    struct
    {
        int ee : 32;
    } e;
};

int main()
{
    struct test t;
    t.a = 'i';
    t.b = 0b11111111;

    t.e.ee = 0x111;
    printf("b add = %p\nc add = %p\n", &t);
    __asm__("int $3"); // this will cause the program to stop execution if running normally or to breakpoint when its on gdb
    printf("%c\n%d\n%d", t.a, t.b, t.c);
    return 0;
}