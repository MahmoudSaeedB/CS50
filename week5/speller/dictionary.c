// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include "dictionary.h"
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of words loaded successfully to memory
int words = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * 27 * 27; // 18954

// Hash table
node *table[N];

// Prototypes
void free_list(node *list);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{

    for (node *n = table[hash(word)]; n != NULL; n = n->next)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function

    int initials[3];

    initials[0] = tolower(word[0]) - 'a';
    initials[1] = (isalpha(word[1])) ? tolower(word[1]) - 'a' : 26;
    initials[2] = (isalpha(word[2])) ? tolower(word[2]) - 'a' : 26;
7
    return (initials[0] * 729 + initials[1] * 27 + initials[2]);
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    // Open dictionary file
    FILE *loaded_dictionary = fopen(dictionary, "r");

    // Check if program is able to open file, returning false if it can't
    if (loaded_dictionary == NULL)
    {
        return false;
    }

    // Declare a char array the can hold longest word in dictionary
    char word[LENGTH + 1];

    // Read strings from loaded_dictionary
    while (fscanf(loaded_dictionary, "%s", word) != EOF)
    {
        // Create new node
        node *n = malloc(sizeof(node));

        // Check if malloc() has enough memory to store word
        if (n == NULL)
        {
            return false;
        }

        // assign word value to new node's word field.
        strcpy(n->word, word);

        // assign current node(head) to the new node's next 
        n->next = table[hash(word)];

        // insert new node into hash table
        table[hash(word)] = n;

        // Increase words succussfully loaded by one
        words++;
    }

    // Close dictionary file
    fclose(loaded_dictionary);

    // if load() successfuly loads dictionary to memory, return true
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < 18954; i++)
    {
        free_list(table[i]);
    }

    return true;
}

// Free linked list
void free_list(node *head)
{
    while (head != NULL)
    {
        node *tmp = head->next;
        free(head);
        head = tmp;
    }
}
