from random import choice

rps = ('r', 'p', 's')
play = True

while play:
    computer = choice(rps)
    player = input("Enter a choice: ")

    while not player in rps:
        player = input("Enter a choice (r, p or s)")
    
    if computer == player:
        print("Tie!", end = " ")
        
    elif computer == "r":
        if player == "p":
            print("Win!", end = " ")
        elif player == "s":
            print("Lose!", end = " ")

    elif computer == "p":
        if player == "r":
            print("Lose!", end = " ")
        elif player == "s":
            print("Win!", end = " ")

    elif computer == "s":
        if player == "p":
            print("Lose!", end = " ")
        elif player == "r":
            print("Win!", end = " ")
    
    print("Computer chose", computer)
    play = input("Play again? y / n  ")
    
    if play.lower() == "y":
        play = True
    else:
        play = False 