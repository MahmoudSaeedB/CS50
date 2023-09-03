#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

bool only_digits(string text);
char encrypt(char c, int k);
int main(int argc, string argv[]) 
{
    //Make sure program was executed with one command-line argument.
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
       

        return 1;
    }

    // Make sure argv[1] is a digit.
    if (only_digits(argv[1]) == false)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
     
    

    // Convert argv[1] characters from string to int.
    int key = atoi(argv[1]);

    // Ask user to input a plaintext.
    string plaintext = get_string("plaintext: ");

    // encrypt each character that is a letter.
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        printf("%c", encrypt(plaintext[i], key));
        
    }
    printf("\n");
   


}

// Convert string to digit.
bool only_digits(string text)
{
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] < '0' || text[i] > '9')
        {  
            return false;
        }
    }

    return true;
}

// Encrypt letters and reserve other characters.
char encrypt(char c, int k)
{
    if (c >= 'A' && c <= 'Z')
    {
        c = c - 'A';
        c = (c + k) % 26;
        return c + 'A';
    }
        

    if (c >= 'a' && c <= 'z')
    {
        c = c - 'a';
        c = (c + k) % 26;
        return c + 'a';
    }

    else
    {
        return c;
    }

}

