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

    def rewrite(self, per, ph, amp, angle):
        self.period = per
        self.phase = ph
        self.amp = amp
        self.angle = angle

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
        X = np.arange(0, self.px, 1)
        Y = np.arange(0, self.py, 1)
        XX, YY = np.meshgrid(X, Y)

        data = np.sin(XX + YY)
        return data


class Random_offset:
    name = "Random offset"
    amp = None
    var = None
    params = ["Amp.", "Var."]

    def rewrite(self, amp, var):
        self.amp = amp
        self.var = var

    def getval(self, p_name):
        if p_name == "Amp.":
            return self.amp
        elif p_name == "Var.":
            return self.var

    def print_all(self):
        print(self.name)
        print("Amp.:" + str(self.amp))
        print("Var.:" + str(self.var))

    def run(self):
        X = np.arange(0, self.px, 1)
        Y = np.arange(0, self.py, 1)
        XX, YY = np.meshgrid(X, Y)

        data = np.sin(XX + YY)
        return data


class Noise:
    name = "Noise"
    amp = None
    var = None
    params = ["Amp.", "Var."]

    def rewrite(self, amp, var):
        self.amp = amp
        self.var = var

    def getval(self, p_name):
        if p_name == "Amp.":
            return self.amp
        elif p_name == "Var.":
            return self.var

    def print_all(self):
        print(self.name)
        print("Amp.:" + str(self.amp))
        print("Var.:" + str(self.var))

    def run(self):
        X = np.arange(0, self.px, 1)
        Y = np.arange(0, self.py, 1)
        XX, YY = np.meshgrid(X, Y)

        data = np.sin(XX + YY)
        return data
