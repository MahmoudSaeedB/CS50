
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Pyramid Height:
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);
    
    for (int i = 0; i < height; i++)
    {   
        // Print first pyramid
        // Print spaces
        for (int j = i; j < height - 1; j++)
        {
            printf(" ");
        }

        // Print hashes
        for (int k = 0; k <= i; k++)
        {   
            printf("#");
        }

        // Print gap
        printf("  ");

        // Print second pyramid
        // Print hashes
        for (int l = 0; l <= i; l++)
        {   
            printf("#");
        }

        // Print a new line
        printf("\n");
    }
}
