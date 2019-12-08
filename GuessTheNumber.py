from random import randint

guesses = 0
guess = -1
max = int(input("Maximum value: "))
number = randint(0, max)

while guess != number:
    guesses += 1
    guess = int(input("Enter guess: "))

    if guess > number:
        print("Lower")
    elif guess < number:
        print("Higher")
    else:
        print("Yes! The number was", number, "! Took", guesses, "tries.")
        break