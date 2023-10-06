import random


def loop_game(score, lst):
    if not lst:
        strategy = {"rock": "paper", "scissors": "rock", "paper": "scissors"}
        op = ["rock", "paper", "scissors"]
        choose = random.choice(op)
        player = input()
        while player not in op:
            if player == "!rating":
                print(f"Your rating: {score}")
            if player == "!exit":
                print("Bye!")
                return
            player = input("Invalid input\n")
        if choose == strategy[player]:
            print(f"Sorry, but the computer chose {choose}")
        elif choose == player:
            score += 50
            print(f"There is a draw ({choose})")
        else:
            score += 100
            print(f"Well done. The computer chose {choose} and failed")

    else:
        player = input()
        while player not in lst:
            if player == "!rating":
                print(f"Your rating: {score}")
            if player == "!exit":
                print("Bye!")
                return
            player = input("Invalid input\n")
        half_len = len(lst) // 2
        index = lst.index(player)
        if half_len > index:
            win = lst[index+1: index+half_len+1]
            # loose = lst[:index]+lst[index+half_len+1:]
        elif half_len < index:
            win = lst[index+1:]+lst[:index-half_len+1]
            # loose = lst[index-half_len:index]
        else:
            win = lst[:index]
            # loose = lst[index:]
        choose = random.choice(lst)
        if choose in win:
            print(f"Sorry, but the computer chose {choose}")
        elif choose == player:
            score += 50
            print(f"There is a draw ({choose})")
        else:
            score += 100
            print(f"Well done. The computer chose {choose} and failed")

    loop_game(score, lst)


def greetings(name, score=None):
    print(f"Hello, {name}")
    with open("rating.txt", "r") as f:
        for n in f.readlines():
            if name in n:
                score = int(n.strip(name))
                break
            else:
                score = 0
    user_list = input()
    lst = user_list.split(sep=",") if user_list != "" else []
    print("Okay, let's start")
    loop_game(score, lst)


greetings(input("Enter your name:"))
