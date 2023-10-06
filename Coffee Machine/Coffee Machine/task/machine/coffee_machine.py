class CoffeeMachine:
    recipe = {
        "1": {
            "water": 250,
            "beans": 16,
            "costs": 4,
            "cups": 1
        },
        "2": {
            "water": 350,
            "milk": 75,
            "beans": 20,
            "costs": 7,
            "cups": 1
        },
        "3": {
            "water": 200,
            "milk": 100,
            "beans": 12,
            "costs": 6,
            "cups": 1
        }
    }

    def __init__(self, water, milk, beans, cups, cost):
        self.remain = {
            "water": water,
            "milk": milk,
            "beans": beans,
            "costs": cost,
            "cups": cups
        }

    def show(self):
        print(f"\nThe coffee machine has:\n"
              f"{self.remain['water']} ml of water\n"
              f"{self.remain['milk']} ml of milk\n"
              f"{self.remain['beans']} g of coffee beans\n"
              f"{self.remain['cups']} disposable cups\n"
              f"${self.remain['costs']} of money\n")
        return self.switch_mode()

    def buy(self):
        op = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n")
        if op == "back":
            return self.switch_mode()
        need_fill = [k for k in CoffeeMachine.recipe[op] if k in self.remain and CoffeeMachine.recipe[op][k] > self.remain[k]]
        if any(need_fill):
            print("Sorry, not enough", *need_fill, "!", sep=" ")
            return self.switch_mode()
        print("I have enough resources, making you a coffee!")
        for k, v in CoffeeMachine.recipe[op].items():
            if k != "costs":
                self.remain[k] -= v
            else:
                self.remain[k] += v
        return self.switch_mode()

    def fill(self):
        self.remain["water"] += int(input("Write how many ml of water you want to add:\n"))
        self.remain["milk"] += int(input("Write how many ml of milk you want to add:\n"))
        self.remain["beans"] += int(input("Write how many grams of coffee beans you want to add:\n"))
        self.remain["cups"] += int(input("Write how many disposable cups you want to add:\n"))
        return self.switch_mode()

    def take(self):
        print(f"I gave you ${self.remain['costs']}")
        self.remain["costs"] = 0
        self.switch_mode()

    def switch_mode(self):
        mode = input("Write action (buy, fill, take, remaining, exit):\n")
        if mode == "buy":
            self.buy()
        if mode == "fill":
            self.fill()
        if mode == "take":
            self.take()
        if mode == "remaining":
            self.show()
        if mode == "exit":
            return


coffee = CoffeeMachine(400, 540, 120, 9, 550)
coffee.switch_mode()
