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
    val = None
    params = ["val"]

    def rewrite(self, params):
        self.val = params[0]

    def run(self):
        image_mod = ndimage.gaussian_filter(self.image, float(self.val))
        return image_mod


class Rotation:
    name = "Rotation"
    image = None
    angle = None
    params = ["angle"]

    def rewrite(self, params):
        self.val = params[0]

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

    def run(self):
        mod_image = cv2.resize(self.image, (self.size_x, self.size_y))
        return mod_image


class Drift:
    name = "Drift"
    image = None
    x = None
    y = None
    params = ["x", "y"]

    def rewrite(self, params):
        self.x = params[0]
        self.y = params[1]

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


class image_modifier:
    def datatype_change(self, image):
        maximum = image.max()
        minimum = image.min()
        if maximum == minimum:
            image_mod = image * 255
        else:
            image_mod = (image - minimum) / (maximum - minimum) * 255
        return image_mod.astype(np.uint8)

    def subtraction(self, image):
        minimum = np.min(image)
        image_mod = image - minimum
        return image_mod

    def apply_window(self, target, window):
        target_copy = np.copy(target)
        if window == "Hann":
            wfunc = signal.hann(target.shape[0])
            wfunc2 = signal.hann(target.shape[1])
        elif window == "Hamming":
            wfunc = signal.hamming(target.shape[0])
            wfunc2 = signal.hamming(target.shape[1])
        elif window == "Blackman":
            wfunc = signal.blackman(target.shape[0])
            wfunc2 = signal.blackman(target.shape[1])
        else:
            wfunc = signal.boxcar(target.shape[0])
            wfunc2 = signal.boxcar(target.shape[1])
        for i in range(target.shape[0]):
            for k in range(target.shape[1]):
                target_copy[i][k] = target[i][k] * wfunc[i] * wfunc2[k]
        target_copy = self.subtraction(target_copy)
        return target_copy

    def fft_processing(self, w_image):
        fimage_or = np.fft.fft2(w_image)
        fimage_or = np.fft.fftshift(fimage_or)
        fimage_or = np.abs(fimage_or)
        return fimage_or

    def fft_scaling(self, image, method):
        if method == "Linear":
            fimage = image
        elif method == "Log":
            fimage = np.log(image, out=np.zeros_like(image), where=(image != 0))
        elif method == "Sqrt":
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
        value = max(
            image_mod[center_y - 1][center_x - 1],
            image_mod[center_y - 1][center_x],
            image_mod[center_y - 1][center_x + 1],
            image_mod[center_y][center_x - 1],
            image_mod[center_y][center_x + 1],
            image_mod[center_y + 1][center_x - 1],
            image_mod[center_y + 1][center_x],
            image_mod[center_y + 1][center_x + 1],
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

    def FFT_process(self, image, method, window):
        image_mod = self.datatype_change(image)
        w_image = self.apply_window(image_mod, window)
        fft_image = self.fft_processing(w_image)
        fft_image = self.fft_scaling(fft_image, method)
        fft_image = fft_image.astype(np.float32)
        if self.ccut_check_bln.get():
            fft_image = self.cut_center(fft_image)
        return fft_image
