#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
   
    int count_letters(string text);
    int count_sentences(string text);
    int count_words(string text);

    // Get the text from the user
    string text = get_string("Text: ");
    
    // Calculate the number of words
    int w = count_words(text);
    
    // Calculate the average of letters per 100 words
    float l = (float) count_letters(text) / (float) w * 100;

    // Calculate the average of sentences per 100 words
    float s = (float) count_sentences(text) / (float) w * 100;

    // Recall and the Coleman-Liau index 
    float indexf = 0.0588 * l - 0.296 * s - 15.8;
    // Round the index
    int index;
    if (indexf - (int) indexf >= 0.5)
    {
        index = (int) indexf + 1;
    }
    else
    {
        index = indexf;
    }

    //Print the index       
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}


int count_letters(string text)
{
    int l = 0;
    for (int i = 0; i < strlen(text); i++)
    {

        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            l++;
        }
    }
    return l;
}

int count_words(string text)                    
{
    int w = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((isspace(text[i]) != 0))
        {
            w++;
        }
    }
    return w;
}

int count_sentences(string text)
{
    int s = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if ((text[i] == '.') || (text[i] == '?') || (text[i] == '!'))
        {
            s++;
        }
    }
    return s;
}
