import random


def domino_gen():  # generate dominoes of 28 pairs
    lst = []
    for i in range(7):
        for j in range(i+1):
            lst.append([i, j])
    return lst


def shuffle():  # shuffle the card if no one gets the highest double
    domino = domino_gen()
    random.shuffle(domino)
    stock = domino[:14]
    players = domino[14:21]
    computer = domino[21:]

    players.sort()
    computer.sort()
    snake = [max(players[-1], computer[-1])]
    if snake[0][0] != snake[0][1]:
        return shuffle()
    players.pop() if snake[0] in players else computer.pop()
    is_player = 1 if len(players) > len(computer) else 0
    return stock, players, computer, snake, is_player


def error_handler(p, x, s):  # handle the player's input, p for player seq, x for player input number, s for snake seq
    try:
        x = int(x)
        while x not in range(-len(p), len(p)+1) or x == "":
            x = int(input("Invalid input. please try again.\n"))
        h = p[abs(x)-1]
        if x != 0:
            head = s[0] if x < 0 else s[-1]
            v = [n for n in h if n in head]
            if v:
                if x < 0:
                    if h[0] == head[0]:
                        p.pop(abs(x)-1)
                        s.insert(0, h[::-1])
                    elif h[1] == head[0]:
                        p.pop(abs(x)-1)
                        s.insert(0, h)
                    else:
                        x = input("Illegal move. Please try again.\n")
                        return error_handler(p, x, s)
                elif x > 0:
                    if h[0] == head[1]:
                        p.pop(abs(x)-1)
                        s.append(h)
                    elif h[1] == head[1]:
                        p.pop(abs(x)-1)
                        s.append(h[::-1])
                    else:
                        x = input("Illegal move. Please try again.\n")
                        return error_handler(p, x, s)
                else:
                    x = input("Illegal move. Please try again.\n")
                    return error_handler(p, x, s)
            else:
                x = input("Illegal move. Please try again.\n")
                return error_handler(p, x, s)
        else:
            return x
    except ValueError:
        x = input("Invalid input. please try again.\n")
        return error_handler(p, x, s)


def ai_move(c, s):  # handle computer's move, return 0 for no paired snake, c for computer seq, s for snake seq
    dic = {}  # ai steps
    for i in range(7):
        j = sum(k.count(i) for k in s)
        dic[i] = j
    rank = {}
    for n in c:
        try:
            rank[dic[n[0]] + dic[n[1]]] += [n]
        except KeyError:
            rank[dic[n[0]] + dic[n[1]]] = [n]
    new = dict(sorted(rank.items(), reverse=True))
    c.clear()  # clear old list otherwise error occurs
    for v in new.values():
        c += v
    for i in range(len(c)):
        h = c[i]
        if s[0][0] in h:
            c.remove(h)
            if h[0] == s[0][0]:
                s.insert(0, h[::-1])
            else:
                s.insert(0, h)
            return 1
        elif s[-1][1] in h:
            c.remove(h)
            if h[0] == s[-1][1]:
                s.append(h)
            else:
                s.append(h[::-1])
            return 1
        else:
            continue
    return 0


def get_stock(p, s, x):  # get the remaining stock for players
    if s and x == 0:
        choose = random.randrange(len(s))
        k = s.pop(choose)
        p.append(k)
    else:
        return


def play(s, p, c, n, is_player):  # main game play func, s for stock, p for player, c for computer, n for snake, is_player check if player is current status, z check non pairs for both player and computer to get a draw
    status = ["Computer is about to make a move. Press Enter to continue...\n", "It's your turn to make a move. Enter your command.\n", "You won!", "The computer won!", "It's a draw!"]
    print("=" * 70)
    print(f"Stock size: {len(s)}")
    print(f"Computer pieces: {len(c)}\n")
    if len(n) <= 6:
        print(*n)
    else:
        print(*n[:3], "...", *n[-3:])
    print("\nYour pieces:")
    for i in range(len(p)):
        print(f"{i+1}:{p[i]}")
    line = "\nStatus: The game is over. "
    if len(p) != 0 and len(c) != 0:
        if n[0][0] == n[-1][1] and sum(x.count(n[0][0]) for x in n) == 8:
            return print(f"{line}{status[4]}")  # draw result if snake head eq snake tail and the number appeared 8 times in seq
        x = input(f"\nStatus: {status[is_player]}")
        if is_player:
            x = error_handler(p, x, n)
            get_stock(p, s, x)
        else:
            while x != "":
                x = input("Invalid input. please try again.\n")
            x = ai_move(c, n)
            get_stock(c, s, x)
        play(s, p, c, n, 0 if is_player else 1)  # player switch
    elif len(p) == 0:
        return print(f"{line}{status[2]}")  # player wins
    else:
        return print(f"{line}{status[3]}")  # computer wins


a, b, d, f, e = shuffle()
play(a, b, d, f, e)
