# Prints a right-aligned pyramid with known height

# Import get_int function from cs50 library that will be used to ask user for pyramid height
from cs50 import get_int

# Ask user for the pyramid height
while True:
    height = get_int("Height: ")

    # Make sure height is beween 1 and 8
    if height >= 1 and height <= 8:
        break

# Iterate over each row in pyramid
for row in range(height):

    # Print spaces
    for spaces in range(height, 1, -1):
        print(' ', end='')

    # Print hashes
    for hashes in range(row+1):
        print('#', end='')

    # Print new line
    print()

    # Update height of remaining part of pyramid
    height -= 1
