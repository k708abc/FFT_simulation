import numpy as np
from scipy import ndimage
import cv2
from scipy import signal


class Plane_wave:
    name = "Plane wave"
    period = None
    phase = None
    amp = None
    angle = None
    px = None
    py = None
    params = ["Period", "Phase", "Amp.", "Angle"]

    def rewrite(self, params):
        self.period = params[0]
        self.phase = params[1]
        self.amp = params[2]
        self.angle = params[3]

    def getval(self, p_name):
        if p_name == "Period":
            return self.period
        elif p_name == "Phase":
            return self.phase
        elif p_name == "Amp.":
            return self.amp
        elif p_name == "Angle":
            return self.angle

    def print_all(self):
        print("Plane wave")
        print("period:" + str(self.period))
        print("phase:" + str(self.phase))
        print("Amp.:" + str(self.amp))
        print("angle:" + str(self.angle))

    def run(self):
        k = 2 * np.pi / self.period
        kx = k * np.cos(-self.angle / 180 * np.pi)
        ky = k * np.sin(-self.angle / 180 * np.pi)
        X = np.arange(0, self.px, 1)
        Y = np.arange(0, self.py, 1)
        XX, YY = np.meshgrid(X, Y)
        data = np.sin(kx * XX + ky * YY - self.phase) * self.amp
        return data

    def rec(self):
        return (
            "Plane_wave:" + "\n\t"
            "period "
            + "\t"
            + str(self.period)
            + "\n\t"
            + "phase:"
            + "\t"
            + str(self.phase)
            + "\n\t"
            + "Amplitude:"
            + "\t"
            + str(self.amp)
            + "\n\t"
            + "angle:"
            + "\t"
            + str(self.angle)
            + "\n"
        )


class Random_offset:
    name = "Random offset"
    amp = None
    params = ["Amp."]

    def rewrite(self, params):
        self.amp = params[0]

    def getval(self, p_name):
        if p_name == "Amp.":
            return self.amp

    def print_all(self):
        print(self.name)
        print("Amp.:" + str(self.amp))

    def run(self):
        noise = np.random.rand(self.py) * self.amp
        data = np.zeros((self.px, self.py))
        data[:] = noise
        data = data.T
        return data

    def rec(self):
        return "Random_offset:" + "\n\t" + "Amplitude:" + "\t" + str(self.amp) + "\n"


class Noise:
    name = "Noise"
    amp = None
    params = ["Amp."]

    def rewrite(self, params):
        self.amp = params[0]

    def getval(self, p_name):
        if p_name == "Amp.":
            return self.amp

    def print_all(self):
        print(self.name)
        print("Amp.:" + str(self.amp))

    def run(self):
        noise = np.random.rand(self.px * self.py) * self.amp
        data = noise.reshape([self.py, self.px])
        return data

    def rec(self):
        return "Random_offset:" + "\n\t" + "Amplitude:" + "\t" + str(self.amp) + "\n"


class Smothing:
    name = "Smoothing"
    image = None
    range = None
    params = ["range"]

    def rewrite(self, params):
        self.range = params[0]

    def getval(self, p_name):
        if p_name == "range":
            return self.range

    def run(self):
        image_mod = ndimage.gaussian_filter(self.image, float(self.range))
        """
        image_mod = cv2.GaussianBlur(
            self.image, (int(self.range), int(self.range)), float(self.range)
        )
        """
        return image_mod

    def rec(self):
        return "Smoothing:" + "\n\t" "Range: " + "\t" + str(self.range) + "\n"


class Rotation:
    name = "Rotation"
    image = None
    angle = None
    params = ["angle"]

    def rewrite(self, params):
        self.val = params[0]

    def getval(self, p_name):
        if p_name == "angle":
            return self.angle

    def rec(self):
        return "Rotation:" + "\n\t" "angle: " + "\t" + str(self.angle) + "\n"

    def run(self):
        width, height = self.image.shape[1], self.image.shape[0]
        center = (int(width / 2), int(height / 2))
        affine_trans = cv2.getRotationMatrix2D(center, self.angle, 1)
        image_mod = cv2.warpAffine(
            self.image,
            affine_trans,
            (width, height),
            flags=cv2.INTER_CUBIC,
        )
        return image_mod


class Resize:
    name = "Resize"
    image = None
    size_x = None
    size_y = None
    params = ["size_x", "size_y"]

    def rewrite(self, params):
        self.size_x = params[0]
        self.size_y = params[1]

    def getval(self, p_name):
        if p_name == "size_x":
            return self.size_x
        if p_name == "size_y":
            return self.size_y

    def run(self):
        mod_image = cv2.resize(self.image, (int(self.size_x), int(self.size_y)))
        return mod_image

    def rec(self):
        return (
            "Resize:"
            + "\n\t"
            + "size_x: "
            + "\t"
            + str(int(self.size_x))
            + "\n\t"
            + "size_y: "
            + "\t"
            + str(int(self.size_y))
            + "\n"
        )


class Drift:
    name = "Drift"
    image = None
    x = None
    y = None
    params = ["x", "y"]

    def rewrite(self, params):
        self.x = params[0]
        self.y = params[1]

    def getval(self, p_name):
        if p_name == "x":
            return self.x
        if p_name == "y":
            return self.y

    def run(self):
        ps_x = len(self.image)
        ps_y = len(self.image[0])
        #
        v11 = 1 + self.x / 2 / ps_y / ps_y
        v12 = self.x / ps_y
        v21 = self.y / 2 / ps_y / ps_x
        v22 = 1 + self.y / ps_y
        #
        if v12 < 0:
            x_shift = -v12 * ps_y
        else:
            x_shift = 0
        mat = np.array([[v11, v12, x_shift], [v21, v22, 0]], dtype=np.float32)
        affine_img = cv2.warpAffine(self.image, mat, (2 * ps_x, 2 * ps_y))
        # calculate the edge of the image
        ax = v11 * ps_x
        ay = v21 * ps_x
        bx = v12 * ps_y
        by = v22 * ps_y
        #
        x0 = int(min(bx, 0) + x_shift)
        y0 = int(min(ay, 0))
        xmax = int(max(ax, bx, ax + bx) + x_shift)
        ymax = int(max(by, by + ay, ay))
        # crop the image
        im_crop = affine_img[y0:ymax, x0:xmax]
        return im_crop

    def rec(self):
        return (
            "Drift:"
            + "\n\t"
            + "x: "
            + "\t"
            + str(self.x)
            + "\n\t"
            + "y: "
            + "\t"
            + str(self.y)
            + "\n"
        )


class FFT:
    image = None
    window = None
    scaling = None
    ccut = False

    def datatype_change(self):
        maximum = self.image.max()
        minimum = self.image.min()
        if maximum == minimum:
            image_mod = self.image * 255
        else:
            image_mod = (self.image - minimum) / (maximum - minimum) * 255
        return image_mod.astype(np.uint8)

    def subtraction(self, image):
        minimum = np.min(image)
        image_mod = image - minimum
        return image_mod

    def apply_window(self, image):
        im_copy = np.copy(image)
        if self.window == "Hann":
            wfunc = signal.hann(im_copy.shape[0])
            wfunc2 = signal.hann(im_copy.shape[1])
        elif self.window == "Hamming":
            wfunc = signal.hamming(im_copy.shape[0])
            wfunc2 = signal.hamming(im_copy.shape[1])
        elif self.window == "Blackman":
            wfunc = signal.blackman(im_copy.shape[0])
            wfunc2 = signal.blackman(im_copy.shape[1])
        else:
            wfunc = signal.boxcar(im_copy.shape[0])
            wfunc2 = signal.boxcar(im_copy.shape[1])
        for i in range(im_copy.shape[0]):
            for k in range(im_copy.shape[1]):
                im_copy[i][k] = im_copy[i][k] * wfunc[i] * wfunc2[k]
        target_copy = self.subtraction(im_copy)
        return target_copy

    def fft_processing(self, w_image):
        fimage_or = np.fft.fft2(w_image)
        fimage_or = np.fft.fftshift(fimage_or)
        fimage_or = np.abs(fimage_or)
        return fimage_or

    def fft_scaling(self, image):
        if self.scaling == "Linear":
            fimage = image
        elif self.scaling == "Log":
            fimage = np.log(image, out=np.zeros_like(image), where=(image != 0))
        elif self.scaling == "Sqrt":
            fimage = np.sqrt(image)
        return fimage

    def cut_center(self, image):
        width, height = image.shape[1], image.shape[0]
        image_mod = np.copy(image)
        if width % 2 == 0:
            center_x = int(width / 2)
            center_y = int(height / 2)
        else:
            center_x = int((width - 1) / 2)
            center_y = int((height - 1) / 2)
        #
        value = np.average([
            image_mod[center_y - 1][center_x - 1],
            image_mod[center_y - 1][center_x],
            image_mod[center_y - 1][center_x + 1],
            image_mod[center_y][center_x - 1],
            image_mod[center_y][center_x + 1],
            image_mod[center_y + 1][center_x - 1],
            image_mod[center_y + 1][center_x],
            image_mod[center_y + 1][center_x + 1],
        ]
        )
        #
        image_mod[center_y - 1][center_x - 1] = value
        image_mod[center_y - 1][center_x] = value
        image_mod[center_y - 1][center_x + 1] = value
        image_mod[center_y][center_x - 1] = value
        image_mod[center_y][center_x] = value
        image_mod[center_y][center_x + 1] = value
        image_mod[center_y + 1][center_x - 1] = value
        image_mod[center_y + 1][center_x] = value
        image_mod[center_y + 1][center_x + 1] = value
        return image_mod

    def run(self):
        image_mod = self.datatype_change()
        w_image = self.apply_window(image_mod)
        fft_image = self.fft_processing(w_image)
        fft_image = self.fft_scaling(fft_image)
        fft_image = fft_image.astype(np.float32)
        if self.ccut:
            fft_image = self.cut_center(fft_image)
        return fft_image


class MyImage:
    name = None
    image = None
    upper = 255
    lower = 0
    shown = False
    rec_name = None
    image_uint8 = None
    mod_image = np.zeros((1, 1))
    pos_x1 = None
    pos_y1 = None
    pos_x2 = None
    pos_y2 = None

    def show(self):
        if self.shown:
            cv2.imshow(self.name, self.mod_image)

    def unshow(self):
        if self.shown:
            try:
                cv2.destroyWindow(self.name)
            except:
                pass
            self.shown = False

    def form_mod(self):

        image_mod = (self.image) * 255
        image_mod = image_mod.astype(np.uint8)
        self.image_uint8 = image_mod
        self.contrast_change()

    def contrast_change(self):
        LUT = self.get_LUT(self.upper, self.lower)
        modified_image = cv2.LUT(self.image_uint8, LUT)
        self.mod_image = modified_image

    def get_LUT(self, maximum, minimum):
        LUT = np.zeros((256, 1), dtype="uint8")
        maximum = int(maximum)
        minimum = int(minimum)
        if maximum == minimum:
            for i in range(-50, 301):
                if i < maximum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 0
                elif i == maximum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = maximum
                else:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 255
        elif maximum > minimum:
            diff = 255 / (maximum - minimum)
            k = 0
            for i in range(-50, 301):
                if i < minimum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 0
                elif i <= maximum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = int(diff * k)
                    k = k + 1
                else:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 255
        else:
            diff = 255 / (maximum - minimum)
            k = 0
            for i in range(-50, 301):
                if i < maximum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 255
                elif i <= minimum:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 255 + int(diff * k)
                    k = k + 1
                else:
                    if i >= 0 and i <= 255:
                        LUT[i][0] = 0
        return LUT

    def record(self):
        cv2.imwrite(self.rec_name + "_" + self.name + ".bmp", self.mod_image)
