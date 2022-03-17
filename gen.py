import random


def gen_field(size, mines, x1, y1):
    res = [[1 for _ in range(size)] for _ in range(size)]
    while res[x1][y1] != 0:
        res = [[0 for _ in range(size)] for _ in range(size)]
        i = 0
        while i < mines:
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            if res[x][y] == 9:
                continue
            res[x][y] = 9
            i += 1
        for i in range(size):
            for j in range(size):
                if res[i][j] == 9:
                    continue
                n = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        if size > i + x >= 0 and size > j + y >= 0 and res[i + x][j + y] == 9:
                            n += 1
                res[i][j] = n
    return res


def gen_matrix(size, value):
    return [[value for _ in range(size)] for _ in range(size)]
