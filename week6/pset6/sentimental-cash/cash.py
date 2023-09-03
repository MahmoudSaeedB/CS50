# Calculates the minimum number of coins required to give a costomer change

from cs50 import get_float


def main():

    # Ask how many cents the costomer is owed
    cents = get_cents()

    # Calculate the number of quarters to give to costomer
    quarters = calculate_quarters(cents)
    cents = cents - quarters * 25

    # Calculate the number of dimes to give to costomer
    dimes = calculate_dimes(cents)
    cents = cents - dimes * 10

    # Calculate the number of nickels to give to costomer
    nickels = calculate_nickels(cents)
    cents = cents - nickels * 5

    # Calculate the number of pennies to give to costomer
    pennies = calculate_pennies(cents)
    cents = cents - pennies * 1

    # Sum coins
    coins = int(quarters + dimes + nickels + pennies)

    print(coins)


def get_cents():

    while True:
        dollars = get_float("Change owed: ")
        if dollars > 0:
            break

    cents = dollars * 100

    return cents


def calculate_quarters(cents):
    quarters = int(cents / 25)
    return quarters


def calculate_dimes(cents):
    dimes = int(cents / 10)
    return dimes


def calculate_nickels(cents):
    nickels = int(cents / 5)
    return nickels


def calculate_pennies(cents):
    return cents


main()
