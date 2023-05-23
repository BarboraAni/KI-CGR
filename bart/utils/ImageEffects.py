from noise import pnoise2
from cv2 import (
    COLOR_BGR2GRAY,
    COLOR_BGR2LAB,
    COLOR_LAB2BGR,
    GaussianBlur,
    addWeighted,
    bitwise_not,
    convertScaleAbs,
    createCLAHE,
    cvtColor,
    filter2D,
    getPerspectiveTransform,
    getRotationMatrix2D,
    imread,
    imshow,
    merge,
    split,
    waitKey,
    warpAffine,
    warpPerspective,
    bilateralFilter,
    getGaussianKernel,
)
from numpy import (
    add,
    array,
    float32,
    ndarray,
    interp,
    full,
    clip,
    uint8,
    linalg,
    copy,
    zeros,
)


class ImageEffects:
    @staticmethod
    def get_rotated_image(image: ndarray, angle: int) -> ndarray:
        """
        Rotates the image around its center by specified angle

        angle (45) (int)
        """
        height, width = image.shape[:2]
        image_center = (width / 2, height / 2)

        rotation_mat = getRotationMatrix2D(image_center, angle, 1.0)

        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]

        rotated_mat = warpAffine(image, rotation_mat, (bound_w, bound_h))
        return rotated_mat

    @staticmethod
    def get_sharpen_image(image: ndarray, degree: float = 1) -> ndarray:
        """
        Sharpens the image

        degree <0, 5>
        """
        filter = array(
            [[0, -degree, 0], [-degree, 1 + 4 * degree, -degree], [0, -degree, 0]]
        )
        return filter2D(image, -1, filter)

    @staticmethod
    def get_blured_image(image: ndarray, degree: float = 1) -> ndarray:
        """
        Adds gaussian blur to the image

        degree {1, 3, 5, 7 ... max 15}
        """
        return GaussianBlur(image, (degree, degree), 0)

    @staticmethod
    def get_inverted_image_colors(image: ndarray) -> ndarray:
        """
        Inverts image colors
        """
        return bitwise_not(image)

    @staticmethod
    def get_embossed_image(image: ndarray, degree: float = 128) -> ndarray:
        """
        Applies grayscale and detects edges

        degree <0, 128>
        """
        image_grayscaled = cvtColor(image, COLOR_BGR2GRAY)
        kernel = array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])
        image_embossed = filter2D(image_grayscaled, -1, kernel)
        return add(image_embossed, degree)

    @staticmethod
    def get_rgb_modified_image(image: ndarray, color: array) -> ndarray:
        """
        Applies R-red, G-green or B-blue color to the image

        color <0, 255>
        """

        adjustments = color

        adjustments = clip(adjustments, -255, 255)

        max_val = full(image.shape, 255)
        positive_adjust = adjustments > 0
        adjusted_image = where(
            positive_adjust, minimum(image + adjustments, max_val), image + adjustments
        )

        print(adjusted_image.dtype)
        adjusted_image = adjusted_image.astype(uint8)
        print(adjusted_image.dtype)

        return adjusted_image

    @staticmethod
    def get_brightness_modified_image(image: ndarray, degree: float = 1) -> ndarray:
        """
        Change exposure of the image

        degree <0, 200>
        """
        return convertScaleAbs(image, alpha=1, beta=degree)

    @staticmethod
    def get_contrast_modified_image(image: ndarray, degree: float = 1) -> ndarray:
        """
        Applies contrast to the image

        degree <0, 2>
        """
        lab = cvtColor(image, COLOR_BGR2LAB)
        l_channel, a, b = split(lab)

        clahe = createCLAHE(clipLimit=degree, tileGridSize=(8, 8))
        cl = clahe.apply(l_channel)

        limg = merge((cl, a, b))
        adjusted_image = cvtColor(limg, COLOR_LAB2BGR)

        return adjusted_image

    @staticmethod
    def get_warped_image(image: ndarray, points: ndarray) -> ndarray:
        """
        Adjust perspective of the image

        points[]
        """
        height, width = image.shape[:2]

        top_left = [0, 0]
        top_right = [width, 0]
        bottom_left = [0, height]
        bottom_right = [width, height]
        converted_points = float32([top_left, top_right, bottom_left, bottom_right])
        perspective_transform = getPerspectiveTransform(points, converted_points)

        return warpPerspective(image, perspective_transform, (width, height))

    @staticmethod
    def get_noise(
        image: ndarray,
        degree: float = 0.1,
        octaves: float = 1,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
    ) -> ndarray:
        """
        Applies perlin noise to the image

        degree <0, 1>
        """
        image_grayscaled = cvtColor(image, COLOR_BGR2GRAY)
        height, width = image_grayscaled.shape

        noise = ImageEffects.get_perlin_noise(
            height, width, degree, octaves, persistence, lacunarity
        )
        noise = interp(noise, (noise.min(), noise.max()), (0, 255)).astype(uint8)

        return addWeighted(image_grayscaled, 0.8, noise, 0.2, 0)

    @staticmethod
    def get_denoised_image(
        image: ndarray, degree: float = 10, sigmaColor: int = 30, sigmaSpace: int = 20
    ) -> ndarray:
        """
        Applies noise reduction to the image using bilateral filter

        degree <0, 50>
        """
        return bilateralFilter(image, degree, sigmaColor, sigmaSpace)

    @staticmethod
    def get_vignette_image(image: ndarray, degree: float = 300) -> ndarray:
        """
        Applies vignette effect to the image

        degree = 150 (default)
        """
        rows, cols = image.shape[:2]

        gaussian_kernel_x = getGaussianKernel(cols, degree)
        gaussian_kernel_y = getGaussianKernel(rows, degree)

        resultant_kernel = gaussian_kernel_y * gaussian_kernel_x.T

        mask = 255 * resultant_kernel / linalg.norm(resultant_kernel)

        adjusted_image = copy(image)

        for i in range(3):
            adjusted_image[:, :, i] = adjusted_image[:, :, i] * mask

        return adjusted_image

    @staticmethod
    def get_perlin_noise(
        height, width, scale=0.1, octaves=1, persistence=0.5, lacunarity=2.0
    ):
        perlin_img = zeros((height, width))
        for i in range(height):
            for j in range(width):
                perlin_img[i][j] = pnoise2(
                    i * scale,
                    j * scale,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                )
        return perlin_img
