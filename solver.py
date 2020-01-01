try:
    file = open("words.txt")
    words = file.read()
    words = words.split()
    file.close()
except FileNotFoundError:
    print("words.txt not found!")
    exit()


letters = input("Letters: ")
search_type = input("Search type: ")

while search_type not in ["max", "exact"]:
    print("search type must be \"max\" or \"exact\"")
    search_type = input("Search type: ")

word_length = int(input("Word length: "))


def letter_count(string, letter):
    """count occurrences of a letter in a word"""
    count = 0

    for char in string:
        if char == letter:
            count += 1

    return count


def check_word(word):
    """check if a word matches the requirements specified"""

    #  Word is correct length
    if search_type == "exact":
        if len(word) != word_length:
            return False
        else:
            if len(word) > word_length:
                return False

    #  Word only contains available letters
    else:
        for letter in word:
            if letter not in letters:
                return False

    #  Letters in word match quantity provided
    for letter in word:
        if letter_count(word, letter) > letter_count(letters, letter):
            return False

    return True


found_words = 0

for word in words:
    if check_word(word):
        print(word)
        found_words += 1

print("\nFound " + str(found_words) + " words")
