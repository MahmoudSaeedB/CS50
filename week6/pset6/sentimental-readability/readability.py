# computes the approximate grade level needed to compre hend some text

from cs50 import get_string


def main():
    # Ask the user for the text
    text = get_text()

    # Count the number of letters in the text
    letters = count_letters(text)

    # Count the number of words in the text
    words = count_words(text)

    # Count the number of sentences in the text
    sentences = count_sentences(text)

    # Calculate the average number of letters per 100 words
    L = letters / words * 100

    # Calculate the average number of sentences per 100 words
    S = sentences / words * 100

    # Calculate the grade level according to the Coleman-Liau formula
    level = calculate_level(L, S)

    # Print the grade level

    # Deal with special cases
    if level < 1:
        print("Before Grade 1")

    elif level >= 16:
        print("Grade 16+")

    else:
        print(f"Grade {round(level)}")


def get_text():
    text = get_string("Text: ")

    return text


def count_letters(text):
    letters = 0
    for char in text:
        if char.isalpha():
            letters += 1

    return letters


def count_words(text):
    words = 0

    if len(text) > 0:
        words += 1

    for char in text:
        if char == ' ':
            words += 1

    return words


def count_sentences(text):
    sentences = 0

    for char in text:
        if char == '.' or char == '!' or char == '?':
            sentences += 1

    return sentences


def calculate_level(L, S):
    level = 0.0588 * L - 0.296 * S - 15.8

    return level


main()
