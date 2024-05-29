#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Intialize the values of the upperclass letters in order
int letter_values[26] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                         1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

// Cite  functions
int compute_score(string word);
void print_winner(int score_1, int score_2);

int main(void)
{
    // Prompt the user for two words
    string word_1 = get_string("Player 1: ");
    string word_2 = get_string("Player 2: ");

    // Compute the score of each word
    int score_1 = compute_score(word_1);
    int score_2 = compute_score(word_2);

    // Print the winner
    print_winner(score_1, score_2);
}

int compute_score(string word)
{   
    // Initialize the word value
    int word_value = 0;

    // Iterate over the word characters
    for (int i = 0; i <= strlen(word); i++)
    {
        // Make sure current character is an alphabetic letter, either uppercase or lowercase
        if (word[i] >= 'A' && word[i] <= 'Z')
        {
            // Calcualte the letter index
            int letter_index = word[i] - 'A';

            // Get the letter value using the index
            int letter_value = letter_values[letter_index];
            
            // Update the word value so far
            word_value += letter_value;
        }
        else if (word[i] >= 'a' && word[i] <= 'z')
        {
            // Calcualte the letter index
            int letter_index = word[i] - 'a'; 

            // Get the letter value using the index
            int letter_value = letter_values[letter_index];
            
            // Update the word value so far
            word_value += letter_value;
        }
    }

    // Reture the word value as the player'score
    return word_value;
}

void print_winner(int score_1, int score_2)
{
    if (score_1 > score_2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score_1 < score_2)
    {
        printf("Player 2 wins!\n");     
    }
    else
    {
        printf("Tie!\n");
    }
}

