import gzip


def read(o):
    with gzip.open(o, "rb") as f:
        seq = str(f.read(), "utf-8").split("\n")
    seq_num = len(seq) // 4
    i = 1
    n_count = []
    length = {}
    gc_count = []
    avg_list = []
    dup = {}
    for _ in range(seq_num):
        s = seq[i].split("\n")[0]
        n = len(s)
        avg_list.append(n)
        gc_count.append(round(((s.count("G") + s.count("C")) / n) * 100, 2))
        if s.count("N") != 0:
            n_count.append(round(s.count("N") / n * 100, 2))
        try:
            length[n] += 1
            dup[s] += 1
        except KeyError:
            length[n] = 1
            dup[s] = 1
        i += 4
    repeat = sum(x - 1 for x in dup.values() if x > 1)
    avg = round(sum(avg_list) / len(avg_list))
    gc_avg = round(sum(gc_count) / len(gc_count), 2)
    n_avg = round(sum(n_count) / seq_num, 2)
    return seq_num, avg, repeat, len(n_count), gc_avg, n_avg


# to compare designated index in nested list and return that nested list
# credits: https://dbader.org/blog/python-min-max-and-nested-lists
def compare_item(y):
    return y[3]


def best(seq, key=None):
    if not seq:
        raise ValueError("empty")
    if not key:
        key = compare_item
    minimal = seq[0]
    for items in seq:
        if key(items) < key(minimal):
            minimal = items
    return minimal


files = [input(), input(), input()]
lst = []
for file in files:
    se, a, r, c, gc, na = read(file)
    lst.append([se, a, r, c, gc, na])


the_best = best(lst, key=compare_item)

print(f"Reads in the file = {the_best[0]}")
print(f"Reads sequence average length = {the_best[1]}")
print(f"\nRepeats = {the_best[2]}")
print(f"Reads with Ns = {the_best[3]}")
print(f"\nGC content average = {the_best[4]}%")
print(f"Ns per read sequence = {the_best[5]}%")
