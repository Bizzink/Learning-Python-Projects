from random import choice, randint, shuffle

def generate(len, nums):
    pword = []

    for i in range(nums):
        pword.append(randint(0, 9))

    for i in range(len - nums):
        pword.append(choice(letters))

    shuffle(pword)
    return pword

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
len = 0
print("Generate a new password")

while len < 6:
    len = int(input("Length of password: "))
    if len < 6:
        print("Password must be at least 6 characters")

nums = len

while nums > len - 2:
    nums = int(input("Amount of numbers in password: "))

    if nums > len - 2:
        print("Must leave room for at least 1 uppercase and 1 lowercase letter")
    elif nums < 1:
        print("must be at lest 1 number")

password = generate(len, nums)
for char in password:
    print(char, end = "")