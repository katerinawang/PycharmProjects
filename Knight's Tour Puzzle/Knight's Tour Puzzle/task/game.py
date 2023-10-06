import math


class Knight:
    def __init__(self):
        self.start = None
        self.dimension = None
        self.placeholder = None
        self.matrix = None
        self.usr_try = None
        self.lst = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        self.valid_moves = []
        self.solution_path = []
        self.long = '| '

    def validate(self, msg=''):
        try:
            print(msg, end='')
            var = input()
            lst = [int(n) for n in var.split()]
            if len(lst) != 2:
                raise KeyError
            for n in lst:
                if n <= 0:
                    raise ValueError
            if self.dimension:
                if lst[0] > self.dimension[0] or lst[1] > self.dimension[1]:
                    raise ValueError
            if 'move' in msg:
                if lst[::-1] not in self.valid_moves:
                    raise ValueError
            return lst
        except (IndexError, ValueError, KeyError):
            if 'position' in msg:
                print('Invalid position!')
            elif 'move' in msg:
                return self.validate('Invalid move! '+msg)
            else:
                print('Invalid dimensions!')
            return self.validate(msg)

    def count(self, r, c, count=0):
        for i in self.lst:
            try:
                if r + i[0] >= 0 and c + i[1] >= 0 and [r+i[0], c+i[1]] not in self.valid_moves:
                    if self.matrix[r+i[0]][c+i[1]] == self.placeholder:
                        count += 1
            except IndexError:
                continue
        return count

    def moves(self, r, c):
        self.valid_moves.clear()
        for i in self.lst:
            try:
                if r+i[0] >= 0 and c+i[1] >= 0 and self.matrix[r+i[0]][c+i[1]] == self.placeholder:
                    self.valid_moves.append([r+i[0]+1, c+i[1]+1])
            except IndexError:
                continue
        if self.usr_try == 'y':
            for i in self.valid_moves:
                self.matrix[i[0]-1][i[1]-1] = (len(str(math.prod(self.dimension))) - 1) * ' ' + str(self.count(i[0]-1, i[1]-1))

    def draw(self):
        self.long = self.dimension[0] * (len(self.placeholder) + 1) + 3
        print('-' * self.long)
        for i, row in reversed(list(enumerate(self.matrix, start=1))):
            string = (len(str(self.dimension[0])) - len(str(i))) * ' ' + str(i) + '| '
            for n in row:
                string += str(n) + ' '
            string += '|'
            print(string)
        print('-' * self.long)
        col = ' ' * (len(str(self.dimension[0])) + 2)
        for i, n in enumerate(self.matrix[0], start=1):
            col += (len(str(n)) - len(str(i))) * ' ' + str(i) + ' '
        print(col)

    def init(self):
        self.matrix = [[self.placeholder for _ in range(self.dimension[0])] for _ in range(self.dimension[1])]
        r = self.start[1] - 1
        c = self.start[0] - 1
        self.matrix[r][c] = (len(str(math.prod(self.dimension))) - 1) * ' ' + 'X'
        self.moves(r, c)
        return r, c

    def knight_move(self, r, c, count=1):
        mov = self.validate('Enter your next move:')
        self.matrix[r][c] = (len(str(math.prod(self.dimension))) - 1) * ' ' + '*'
        count += 1
        for i in self.valid_moves:
            if i != mov[::-1]:
                self.matrix[i[0]-1][i[1]-1] = self.placeholder
        self.matrix[mov[1]-1][mov[0]-1] = (len(str(math.prod(self.dimension))) - 1) * ' ' + 'X'
        self.moves(mov[1]-1, mov[0]-1)
        self.draw()
        while self.valid_moves:
            return self.knight_move(mov[1]-1, mov[0]-1, count)
        else:
            if count != math.prod(self.dimension):
                print('No more possible moves!')
                print(f'Your knight visited {count} squares!')
            else:
                print('What a great tour! Congratulations!')

    def solution(self, r, c, step=1):
        self.matrix[r][c] = (len(str(math.prod(self.dimension))) - len(str(step))) * ' ' + str(step)
        if step == math.prod(self.dimension):
            return True
        last_valid = self.valid_moves.copy()
        for i in last_valid:
            self.moves(i[0]-1, i[1]-1)
            if self.solution(i[0] - 1, i[1] - 1, step+1):
                return True
            self.matrix[i[0]-1][i[1]-1] = self.placeholder
        return False

    def main(self):
        self.dimension = self.validate('Enter your board dimensions:')
        self.placeholder = len(str(math.prod(self.dimension))) * '_'
        self.start = self.validate('Enter the knight\'s starting position:')
        r_mv_1, c_mv_1 = self.init()
        solution = self.solution(r_mv_1, c_mv_1)
        self.usr_try = input('Do you want to try the puzzle? (y/n):')
        while self.usr_try not in {'y', 'n'}:
            print('Invalid input!')
            self.usr_try = input('Do you want to try the puzzle? (y/n):')
        if self.usr_try == 'y' and solution:
            self.matrix = None
            self.init()
            self.draw()
            return self.knight_move(r_mv_1, c_mv_1)
        if self.usr_try == 'n' and solution:
            print('\nHere\'s the solution!')
            self.draw()
        else:
            print('No solution exists!')


k = Knight()
k.main()
