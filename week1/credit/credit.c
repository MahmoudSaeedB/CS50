#include <cs50.h>
#include <stdio.h>

int calculate_checksum(long number);
// string check_match(long number);

int main(void)
{
    // Ask user for credit card number
    long number = get_long("Number: ");

    // Calculate checksum
    int checksum = calculate_checksum(number);
    
    // Check for card length and starting digits
    // string check_match = check_match(number);

    // Print card name if matches one of the 3 cards
}

int calculate_checksum(long number)
{
    // Get the alternating digits and remaining digits

    int digit;
    int alternating_digits[8];
    int remaining_digits[8];
    int i = 0;
    int j = 0;
    do 
    {
        // Get the last digit of the number
        digit = number % 10;
        printf("%i\n", digit);

        // Update the number
        number = number / 10;

        // Check if the digit is one of the alternating digits or the remaining digits
        if (i % 2 != 0)
        {
            alternating_digits[j] = digit;
        }
        else
        {
            remaining_digits[j] = digit;
            j++;
        }

        // Update the iterator 
        i++;
    }
    while (number >= 1);

    // Calculate checksum
    int checksum = 0;

    for (int k = 0; k < 8; k++)
    {
        printf("%i, %i\n", alternating_digits[k], remaining_digits[k]);
        // checksum = checksum + (alternating_digits[k] * 2) + remaining_digits[k];
    }
    
    printf("%i", checksum);
    return checksum;
}

