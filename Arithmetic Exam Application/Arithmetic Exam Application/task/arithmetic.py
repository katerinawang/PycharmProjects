import random


def operations():
    a = str(random.randint(2, 9))
    b = str(random.randint(2, 9))
    operation = random.choice(["+", "-", "*"])
    math = a + operation + b
    print(a, operation, b)
    return eval(math)


def int_sqr():
    base = random.randint(11, 29)
    print(str(base))
    return pow(base, 2)


def validate(option):
    mark = 0
    for _ in range(5):
        if option == "1":
            ans = operations()
        else:
            ans = int_sqr()
        while True:
            try:
                usr = int(input())
                if ans == int(usr):
                    mark += 1
                    print("Right!")
                else:
                    print("Wrong!")
                break
            except ValueError:
                print("Wrong format! Try again.")
    return mark


def main():
    while True:
        level = input("Which level do you want? Enter a number:\n1 - simple operations with numbers 2-9\n2 - integral squares of 11-29\n")
        lv = {"1": "(simple operations with numbers 2-9)", "2": "(integral squares of 11-29)"}
        if level in lv.keys():
            break
        else:
            print("Incorrect format.")
    result = str(validate(level)) + "/5"
    save = input(f"Your mark is {result}. Would you like to save the result? Enter yes or no.\n")
    if save in ["yes", "YES", "y", "Yes"]:
        name = input("What is your name?\n")
        fmt = f"{name}: {result} in level {level} {lv[level]}."
        with open("results.txt", "a") as f:
            f.write(fmt)
        print('The results are saved in "results.txt"')


if __name__ == "__main__":
    main()
