import tkinter as tk
import numpy as np
import cv2


class functions:
    def init_setting(self):
        pass

    def image_formation(self):
        px = int(self.pix_x_entry.get())
        py = int(self.pix_y_entry.get())
        image_rec = [np.zeros((px, py))]
        for i in self.processes:
            i.px = px
            i.py = py
            image_rec.append(i.run())
        self.image = np.sum(image_rec, axis=0)
        self.image = self.normarize(self.image)
        cv2.imshow("Image", self.image)
        """
        for pro in self.processes:
            if pro[0] == "Plane wave":

            elif pro[0] == "Random offset":

            elif pro[0] == 

        data = np.sin(XX + YY)
        cv2.imshow("test", data)

        """

    def normarize(self, image):
        val_min = np.min(image)
        val_max = np.max(image)
        diff = val_max - val_min
        if diff == 0:
            return image
        new_image = (image - val_min) / diff
        return new_image
