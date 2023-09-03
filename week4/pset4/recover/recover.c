#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check program was run with one command-line argument
    if (argc != 2)
    {
        // Teach user how to use the program
        printf("Usage: ./recover card.raw\n");
        return 1;
    }
    // Open memory card
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        return 1;
    }

    unsigned char buffer[512];

    FILE *img;

    int file_order = 0;

    char *filename = malloc(8);
    if (filename == NULL)
    {
        return 1;
    }

    while (fread(buffer, 1, 512, file) == 512)
    {
        // Check if start of buffer is start of JPG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {

            // Close old image file 
            if (file_order > 0)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", file_order);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                return 1;
            }
            fwrite(buffer, 1, 512, img);

            file_order++;
        }
        else if (file_order > 0)
        {
            fwrite(buffer, 1, 512, img);
        }
    
    }
    // Close any files you have opened.
    fclose(file);
    fclose(img);
    // Free bytes you have allocated
    free(filename);
}