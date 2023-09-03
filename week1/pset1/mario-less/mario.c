#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //Pyramid Height:
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
    
    for (int i = 0; i < n; i++)
    {   
        //Print spaces
        for (int s = i; s < n - 1; s++)
        {
            printf(" ");
        }

        //print hashes
        for (int x = 0; x <= i; x++)
        {   
           
            printf("#");
        }
        //print a new line
        printf("\n");
       

    }
}




