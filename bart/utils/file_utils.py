from cv2 import imread, imwrite
import numpy as np


def open_image(path: str) -> np.ndarray:
    """
    Loads and image as a ndarray
    """
    try:
        image = imread(path)
        if image is None:
            raise FileNotFoundError("File does not exist or is not supported: %s", path)
        return image
    except FileNotFoundError as exc:
        print("Error occurred while opening the image: %s", path)


def save_image(path: str, image: np.ndarray) -> None:
    """
    Saves and image
    """
    try:
        imwrite(path, image)
    except Exception as exc:
        print("Error occurred while saving the image: %s", path)
