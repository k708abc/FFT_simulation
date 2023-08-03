import numpy as np


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
