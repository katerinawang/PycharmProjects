import random


class PenAndPaper:
    def __init__(self):
        self.players = ['John', 'Jack']
        self.valid_moves = (1, 2, 3)
        self.stick = '|'
        self.nums = None

    def init(self, msg='Who will be the first (John, Jack):\n'):
        first = input(msg)
        if first not in self.players:
            return self.init("Choose between 'John' and 'Jack'\n")
        self.players.remove(first)
        second = self.players[0]
        print(self.stick * self.nums)
        return [first, second]

    def take_turns(self, name, msg=''):
        if not msg:
            msg = f'{name}\'s turn!\n'
        if name == 'John':
            try:
                num = int(input(msg))
                if num <= 0 or num not in self.valid_moves:
                    raise ValueError
                if num > self.nums:
                    return self.take_turns(name, 'Too many pencils were taken\n')
            except ValueError:
                return self.take_turns(name, "Possible values: '1', '2' or '3'\n")
        else:
            print(msg)
            num = (self.nums - 1) % 4
            if num == 0:
                num = random.randint(1, 3)
            if num > self.nums:
                num = self.nums
            print(num)
        return num

    def gaming(self):
        turns = self.init()
        while self.nums != 0:
            for i in turns:
                take_stick = self.take_turns(i)
                self.nums -= take_stick
                if self.nums == 0:
                    turns.remove(i)
                    return turns[0]
                print(self.stick * self.nums)

    def main(self, msg='How many pencils would you like to use:\n'):
        try:
            self.nums = int(input(msg))
            if self.nums <= 0:
                return self.main('The number of pencils should be positive\n')
        except ValueError:
            return self.main('The number of pencils should be numeric\n')
        winner = self.gaming()
        print(f'{winner} won!')


game = PenAndPaper()
game.main()
