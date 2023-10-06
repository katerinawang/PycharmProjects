regex, string = input().split('|')


def reg(a, b):
    if len(a) < 2 or len(b) < 2:
        return a == '.' or a == '' or a == b
    else:
        a, *res_a = a
        b, *res_b = b
        if a == b or a == '.':
            return reg(''.join(res_a), ''.join(res_b))
        else:
            return False


def match(a, b):
    if '$' not in a and '^' not in a:
        if len(a) == len(b):
            return reg(a, b)
        else:
            return a in b or a == '' or a == '.'
    else:
        if a[0] == '^' and a[-1] == '$':
            return reg(a[1:-1], b)
        elif a[0] == '^':
            return reg(a[1:], b[:len(a)-1])
        elif a[-1] == '$':
            return reg(a[:-1], b[-len(a)+1:])


def appearance(a, b, mark=None):
    if '?' in a or '*' in a or '+' in a:
        if '?' in a:
            mark = '?'
        if '*' in a:
            mark = '*'
        if '+' in a:
            mark = '+'
        desired = a[a.index(mark)-1:a.index(mark)+1]
        zero = a.replace(desired, '')
        once = a.replace(mark, '')
        sub = 2
        if '^' in a and '$' in a:
            sub = 4
        elif '^' in a or '$' in a:
            sub = 3
        if len(b) - (len(a) - 2) > 0:
            multiple = a[:a.index(mark)-1] + a[a.index(mark)-1] * (len(b) - (len(a) - sub)) + a[a.index(mark)+1:]
        else:
            multiple = a[:a.index(mark)] + a[a.index(mark)+1:]
        if '?' in a:
            print(match(zero, b) or match(once, b))
        if '*' in a:
            print(match(zero, b) or match(once, b) or match(multiple, b))
        if '+' in a:
            print(match(once, b) or match(multiple, b))
    else:
        return print(match(a, b))


def escape(a, b):
    if '\\' in a:
        return print(match(a.replace('\\', ''), b))
    else:
        return appearance(a, b)


escape(regex, string)
