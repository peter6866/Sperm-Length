import numpy as np
from PIL import Image
import cv2


def get_roi(image):
    # Range of red color
    lower_red = np.array([100, 0, 0])
    upper_red = np.array([255, 100, 100])

    # Threshold the image to get only red colors
    mask = cv2.inRange(image, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    # Make the background black
    mask_of_largest = np.zeros_like(mask)
    cv2.drawContours(
        image=mask_of_largest,
        contours=[largest_contour],
        contourIdx=-1,
        color=[255],
        thickness=cv2.FILLED
    )

    res = cv2.bitwise_and(image, image, mask=mask_of_largest)

    return res


def threshold(image, val):
    return np.where(image > val, 1, 0)
