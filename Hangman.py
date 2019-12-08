from random import choice

def hangman():
    global word, guess, tries_left
    word = choice(words)
    guess = ["_"] * len(word)
    tries_left = 10
    chosen_letters = []
    win = False
    print_guess()

    while tries_left > 0 and not win:
        letter = input("Enter a letter: ")

        if letter not in chosen_letters:
            chosen_letters.append(letter)
            check_letter(letter)
            print_guess()
            win = check_win()
        else:
            print("Letter already chosen!")

    if win == True:
        print("good job! Word was", word)
    else:
        print("Lose!, word was", word )

def check_letter(letter):
    global word, tries_left

    if letter in word:
        for pos, val in enumerate(word):
            if val == letter:
                guess[pos] = letter
    else:
        tries_left -= 1

def print_guess():
    global tries_left
    for letter in guess:
        print(letter, end = " ") #doing this because guess is a list, there is no doubt a better way to do this
    print("Incorrect tries left:", tries_left)

def check_win():
    global word, guess

    for pos, letter in enumerate(word):
        if letter == guess[pos]:
            pass
        else:
            return False
    
    return True
    
try:
    words_file = open("words.txt")
except FileNotFoundError:
    print("words.txt not found!")
    exit()  #This probably isn't good practise, but too bad buddy

words = words_file.read()
words_file.close()
words = words.split(sep = "\n")

hangman()