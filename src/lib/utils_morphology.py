import numpy as np
from collections import deque


# Define the structure element
str_elem = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def is_fitted(img, x, y, rows, cols):
    for eX, eY in str_elem:
        if not (1 <= x + eX <= rows and 1 <= y + eY <= cols and
                img[x + eX - 1, y + eY - 1] == 1):
            return False
    return True


def erode(img, r):
    rows, cols = img.shape
    temp_image = img.copy()
    eroded_image = np.zeros_like(img)

    for _ in range(r):
        for i in range(rows):
            for j in range(cols):
                if temp_image[i, j] == 1:
                    if is_fitted(temp_image, i + 1, j + 1, rows, cols):
                        eroded_image[i, j] = 1
                    else:
                        eroded_image[i, j] = 0
                else:
                    eroded_image[i, j] = 0
        temp_image = eroded_image.copy()

    return eroded_image


def is_overlapped(img, x, y, rows, cols):
    for eX, eY in str_elem:
        if (1 <= x + eX <= rows and 1 <= y + eY <= cols and
                img[x + eX - 1, y + eY - 1] == 1):
            return True
    return False


def dilate(img, r):
    rows, cols = img.shape
    temp_image = img.copy()
    dilated_image = np.zeros_like(img)

    for _ in range(r):
        for i in range(rows):
            for j in range(cols):
                if temp_image[i, j] == 0:
                    if is_overlapped(temp_image, i + 1, j + 1, rows, cols):
                        dilated_image[i, j] = 1
                    else:
                        dilated_image[i, j] = 0
                else:
                    dilated_image[i, j] = 1
        temp_image = dilated_image.copy()

    return dilated_image


def open_img(img, r):
    eroded_img = erode(img, r)
    return dilate(eroded_img, r)


def close_img(img, r):
    open_inverted = open_img(1 - img, r)
    return 1 - open_inverted


def flood(img, start, conn):
    rows, cols = img.shape
    # Define connectivity based on the conn parameter
    if conn == 1:
        connect_points = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    else:
        connect_points = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]

    # Initialize the result set and visited flags
    S = np.zeros_like(img)
    visited = np.zeros_like(img)
    x, y = start
    S[x, y] = 1
    visited[x, y] = 1

    # Initialize a queue with the starting point
    F = deque()
    F.append((x, y))

    while F:
        temp = F.popleft()
        for dx, dy in connect_points:
            nx, ny = temp[0] + dx, temp[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and not visited[nx, ny]:
                if img[nx, ny] == img[x, y]:
                    S[nx, ny] = 1
                    visited[nx, ny] = 1
                    F.append((nx, ny))

    return S


def labelComponents(img, conn):
    rows, cols = img.shape
    index = 1
    tempImg = img.copy()

    for i in range(rows):
        for j in range(cols):
            if tempImg[i, j] == 1:
                # Run flood algorithm and add index times back to the original image
                flood_fill = flood(img, (i, j), conn)
                tempImg += index * flood_fill
                index += 1

    # Adjust the labels
    tempImg[tempImg != 0] -= 1

    return tempImg


def numberComponents(img, conn):
    # Label the components
    labeled_img = labelComponents(img, conn)

    # Find the maximum label value, which is the number of components
    num_components = np.max(labeled_img)

    return num_components


def getKLargestComponents(img, k, conn):
    rows, cols = img.shape
    res = np.zeros((rows, cols), dtype=int)

    # Label the components
    componentImage = labelComponents(img, conn)

    # Find the number of components
    max_label = np.max(componentImage)

    # Count the size of each component
    sizes = [np.sum(componentImage == i) for i in range(1, max_label + 1)]

    # Find indices of the k largest components
    largeIndex = np.argsort(sizes)[-k:]

    # Mark the k largest components in the result image
    for i in range(1, max_label + 1):
        if i-1 in largeIndex:
            res[componentImage == i] = 1

    return res
