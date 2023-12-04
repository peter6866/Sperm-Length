import numpy as np
import cv2


def get_roi(image):
    """
        Extracts region of interest (ROI) from an image.

        This function identifies red areas within a specified color range, finds the largest red contour,
        and returns an image with only this contour visible against a black background.

        Parameters:
        image (numpy.ndarray): Input image in BGR format.

        Returns:
        numpy.ndarray: Image with the largest red area isolated.
        """

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

    # Also set the color of contour to black
    mask = ((image >= lower_red) & (image <= upper_red)).all(axis=-1)
    res[mask] = [0, 0, 0]

    return res


def threshold(image, val):
    return np.where(image > val, 1, 0)
