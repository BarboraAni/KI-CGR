from numpy import ndarray


class State:
    def __init__(self, image: ndarray):
        self._image = image
        self._rotation = 0
        self._is_inverted = False
        self._is_warped = False
        self._is_vignetted = False
        self._is_embossed = False
        self._sharpen = 0
        self._blur = 0
        self._red = 0
        self._green = 0
        self._blue = 0
        self._exposure = 0
        self._contrast = 0
        self._perlin_noise = 0
        self._denoise_sldr = 0

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation

    @property
    def is_inverted(self):
        return self._is_inverted

    @is_inverted.setter
    def is_inverted(self, is_inverted):
        self._is_inverted = is_inverted

    @property
    def is_warped(self):
        return self._is_warped

    @is_warped.setter
    def is_warped(self, is_warped):
        self._is_warped = is_warped

    @property
    def is_vignetted(self):
        return self._is_vignetted

    @is_vignetted.setter
    def is_vignetted(self, is_vignetted):
        self._is_vignetted = is_vignetted

    @property
    def is_embossed(self):
        return self._is_embossed

    @is_embossed.setter
    def is_embossed(self, is_embossed):
        self._is_embossed = is_embossed

    @property
    def sharpen(self):
        return self._sharpen

    @sharpen.setter
    def sharpen(self, sharpen):
        self._sharpen = sharpen

    @property
    def blur(self):
        return self._blur

    @blur.setter
    def blur(self, blur):
        self._blur = blur

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, red):
        self._red = red

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, green):
        self._green = green

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, blue):
        self._blue = blue

    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, exposure):
        self._exposure = exposure

    @property
    def contrast(self):
        return self._contrast

    @contrast.setter
    def contrast(self, contrast):
        self._contrast = contrast

    @property
    def perlin_noise(self):
        return self._perlin_noise

    @perlin_noise.setter
    def perlin_noise(self, perlin_noise):
        self._perlin_noise = perlin_noise

    @property
    def denoise_sldr(self):
        return self._denoise_sldr

    @denoise_sldr.setter
    def denoise_sldr(self, denoise_sldr):
        self._denoise_sldr = denoise_sldr
