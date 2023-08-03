import tkinter as tk
import numpy as np
import cv2


class functions:
    def init_setting(self):
        pass

    def image_formation(self):
        px = int(self.pix_x_entry.get())
        py = int(self.pix_y_entry.get())

        X = np.arange(0, px, 1)
        Y = np.arange(0, py, 1)
        XX, YY = np.meshgrid(X, Y)
        image_rec = []
        for i in self.processes:
            i.px = px
            i.py = py
            image_rec.append(i.run())
            i.print_all()
        """
        for pro in self.processes:
            if pro[0] == "Plane wave":

            elif pro[0] == "Random offset":

            elif pro[0] == 

        data = np.sin(XX + YY)
        cv2.imshow("test", data)
        """
