#include <stdio.h>

struct Man
{
    char name[50];
    int age;
    float height;
};

struct test
{
    char a;
    int b : 5, c : 11, d : 21; // b is 5 bit int
    struct
    {
        int ee : 32;
    } e;
};

int main()
{

    struct Man man;
    man.age = 25;
    man.height = 5.9;
    snprintf(man.name, sizeof(man.name), "Alice"); // assign the strings Alice to man.name

    // Printing values
    printf("Name: %s\n", man.name);
    printf("Age: %d\n", man.age);
    printf("Height: %.1f ft\n", man.height);

    return 0;
}
