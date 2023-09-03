#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Get the username
    string name = get_string("What's your name? ");
    
    // Welcome the user
    printf("hello, %s\n", name);
}
