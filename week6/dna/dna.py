import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: dna.py DATABASE.cvs SEQUENCE.txt")
        return
    # TODO: Read database file into a variable
    database = sys.argv[1]

    database_file = open(database, 'r')
    database_reader = csv.reader(database_file)

    # TODO: Read DNA sequence file into a variable
    sequence = sys.argv[2]

    with open(sequence, 'r') as sequence_file:
        sequence_reader = sequence_file.read()

    # TODO: Find longest match of each STR in DNA sequence
    STRs = []

    for row in database_reader:
        for STR in row[1:]:
            STRs.append(STR)

        break

    STR_counts = []

    for i in range(len(STRs)):
        STR = STRs[i]

        STR_count = longest_match(sequence_reader, STR)

        STR_counts.append(STR_count)

    # TODO: Check database for matching profiles
    # next(database_reader)

    for person in database_reader:

        if STR_counts == [int(STR) for STR in person[1:]]:
            print(person[0])
            database_file.close()
            return

    print("No match")
    database_file.close()


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
