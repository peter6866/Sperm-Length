import numpy as np


def buildCC2D(array):
    zeroPos = np.array([[1, 1], [1, -1], [-1, -1], [-1, 1]])
    onePos = np.array([[1, 0], [0, -1], [-1, 0], [0, 1]])

    rows, cols = array.shape
    indexArray = np.zeros((2 * rows + 1, 2 * cols + 1), dtype=int)

    zeroIdx, oneIdx, twoIdx = 0, 0, 0
    res0, res1, res2 = [], [], []

    for i in range(rows):
        for j in range(cols):
            if array[i, j] == 1:
                temp2 = []
                x, y = 2 * i, 2 * j
                twoIdx += 1
                indexArray[x, y] = twoIdx

                # Check and insert one cells
                for l in range(len(onePos)):
                    m, n = [x, y] + onePos[l]
                    if indexArray[m, n] == 0:
                        oneIdx += 1
                        indexArray[m, n] = oneIdx
                    temp2.append(indexArray[m, n])
                res2.append(temp2)

                # Check and insert zero cells
                for l in range(len(zeroPos)):
                    m, n = [x, y] + zeroPos[l]
                    if indexArray[m, n] == 0:
                        zeroIdx += 1
                        indexArray[m, n] = zeroIdx
                        res0.append([(n - 1) / 2, (m - 1) / 2])

                # For one-cells, iterate through each pair of zero cells
                for k in range(len(zeroPos)):
                    x1, y1 = indexArray[x + zeroPos[k, 0], y + zeroPos[k, 1]], indexArray[
                        x + zeroPos[(k + 1) % len(zeroPos), 0], y + zeroPos[(k + 1) % len(zeroPos), 1]]
                    if [x1, y1] not in res1 and [y1, x1] not in res1:
                        res1.append([x1, y1])

    return [res0, res1, res2]


def thin(cc, thresholds):
    depth = len(cc)

    removed = [np.zeros(len(cc[d]), dtype=int) for d in range(depth)]
    parentTable = [np.zeros(len(cc[d]), dtype=int) for d in range(depth)]

    # Populate parent table
    for d in range(1, depth):
        for r in range(len(cc[d])):
            for c in range(len(cc[d][r])):
                parentTable[d - 1][cc[d][r][c] - 1] += 1

    # Create isolation table
    isolated = [np.where(pt == 0, 0, None) for pt in parentTable]

    k = 1
    while True:
        simplePairs = []
        for d in range(1, depth):
            for r in range(len(cc[d])):
                if removed[d][r] != 1:
                    candidates = [c for c in cc[d][r] if parentTable[d - 1][c - 1] == 1]
                    if candidates:
                        t = candidates[0] - 1
                        cell1 = (d - 1, t)
                        cell2 = (d, r)
                        ix = isolated[cell2[0]][cell2[1]]
                        if cell2[0] != 1:
                            if not ((k - ix > thresholds[0][0]) and (1 - ix / k > thresholds[0][1])):
                                simplePairs.append((cell1, cell2))
                        else:
                            simplePairs.append((cell1, cell2))

        if not simplePairs:
            break

        for cell1, cell2 in simplePairs:
            for m in cc[cell2[0]][cell2[1]]:
                tx, ty = cell2[0] - 1, m - 1
                parentTable[tx][ty] -= 1
                if parentTable[tx][ty] == 0:
                    isolated[tx][ty] = k

            if cell1[0] > 0:
                for m in cc[cell1[0]][cell1[1]]:
                    tx, ty = cell1[0] - 1, m - 1
                    parentTable[tx][ty] -= 1
                    if parentTable[tx][ty] == 0:
                        isolated[tx][ty] = k

            removed[cell1[0]][cell1[1] - 1] = 1
            removed[cell2[0]][cell2[1] - 1] = 1

        k += 1

    temp1 = []
    rTemp = 0
    dict1 = {}
    for r in range(len(cc[0])):
        dict1[r + 1] = rTemp
        if removed[0][r] != 1:
            temp1.append(cc[0][r])
            rTemp += 1

    temp2 = []
    rTemp = 0
    dict2 = {}
    for r in range(len(cc[1])):
        dict2[r + 1] = rTemp
        if removed[1][r] != 1:
            temp2.append(
                [cc[1][r][0] - dict1[cc[1][r][0]],
                 cc[1][r][1] - dict1[cc[1][r][1]]]
            )
            rTemp += 1

    temp3 = []
    for r in range(len(cc[2])):
        if removed[2][r] != 1:
            temp = []
            for j in range(len(cc[2][r])):
                temp.append(cc[2][r][j] - dict2[cc[2][r][j]])
            temp3.append(temp)

    return [temp1, temp2, temp3]

