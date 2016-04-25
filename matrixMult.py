
w, h = 8, 5

matrixA = [[2 for x in range(w)] for y in range(h)]
matrixB = [[4 for x in range(w)] for y in range(h)]

one = [[12, 7, 3],
     [4, 5, 6],
     [7, 8, 9]]

two  = [[5, 8, 1, 2],
     [6, 7, 3, 0],
     [4, 5, 9, 1]]

result = [[0 for x in range(4)] for y in range(3)]

for i in range(len(one)):
    for j in range(len(two[0])):
        for k in range(len(one)):
            result[i][j] += one[i][k] * two[k][j]

for r in result:
    print(r)

result2 = [[sum(a*b for a,b in zip(one_row, two_col)) for two_col in zip(*two)] for one_row in one]

for r in result2:
    print(r)
