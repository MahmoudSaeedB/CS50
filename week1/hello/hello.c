#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get username
    string name = get_string("What's your name? ");
    
    // Greet the user
    printf("hello, %s\n", name);
}
