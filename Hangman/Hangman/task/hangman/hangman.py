import random


def guess_new(v, a, b):
    att = 8
    cor = random.choice(v)
    hint = "-" * (len(cor))
    hit = set()
    while att > 0:
        w = input(f"{hint}\nInput a letter: ")
        if len(w) != 1:
            print(f"Please, input a single letter.")
        elif w.isupper() or not w.isalpha():
            print(f"Please, enter a lowercase letter from the English alphabet.")
        elif w in hit:
            print(f"You've already guessed this letter.")
        elif w in set(cor):
            j = 0
            for _ in range(cor.count(w)):
                i = cor.find(w, j)
                j = i + 1
                hint = hint[:i] + w + hint[i+1:]
                if hint == cor:
                    a += 1
                    print(f"You guessed the word {hint}!\nYou survived!")
                    return a, b
        else:
            att -= 1
            print(f"That letter doesn't appear in the word.  # {att} attempts")
        hit.add(w)
    b += 1
    print("You lost!")
    return a, b


def menu(v1, v2):
    word_list = ["python", "java", "swift", "javascript"]
    choose = 'Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:'
    op = input(choose)
    if op == "play":
        v1, v2 = guess_new(word_list, v1, v2)
        menu(v1, v2)
    elif op == "results":
        print(f"You won: {v1} times.\nYou lost: {v2} times.")
        menu(v1, v2)
    else:
        return


print("H A N G M A N  # 8 attempts")
win = 0
los = 0
menu(win, los)
