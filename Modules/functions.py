import numpy as np
import cv2
import os


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
        cv2.imshow("Original image", self.image)

    def normarize(self, image):
        val_min = np.min(image)
        val_max = np.max(image)
        diff = val_max - val_min
        if diff == 0:
            return image
        new_image = (image - val_min) / diff
        return new_image

    def image_processing(self):
        self.processed_image = np.copy(self.image)
        for i in range(4):
            if i == self.prev_smooth_val:
                self.processed_image = self.smoothing(
                    self.processed_image, float(self.smooth_entry.get())
                )
            elif i == self.prev_rot_val:
                self.processed_image = self.rotation(
                    self.processed_image, float(self.rot_entry.get())
                )
            elif i == self.prev_resize_val:
                self.processed_image = self.resize(
                    self.processed_image,
                    int(self.resize_x_entry.get()),
                    int(self.resize_y_entry.get()),
                )
            elif i == self.prev_drift_val:
                self.processed_image = self.drift(
                    self.processed_image,
                    float(self.drift_x_entry.get()),
                    float(self.drift_y_entry.get()),
                )
        self.processed_image = self.normarize(self.processed_image)
        cv2.imshow("Processed image", self.processed_image)

    def show_FFT(self):
        upper, lower = self.current_contrast()
        self.FFT_image_mod = self.contrast_change(self.FFT_image, upper, lower)
        cv2.imshow("FFT image", self.FFT_image_mod)

    def current_contrast(self):
        upper = int(self.upper_val.get())
        lower = int(self.lower_val.get())
        return upper, lower

    def contrast_change(self, image, upper, lower):
        LUT = self.get_LUT(upper, lower)
        image_mod = (image) * 255
        image_mod = image_mod.astype(np.uint8)
        modified_image = cv2.LUT(image_mod, LUT)
        return modified_image

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

    def record_function(self):
        folder = "Records"
        if os.path.isdir(folder) is False:
            os.makedirs(folder)

        if self.image_formed:
            im_name = folder + "\\" + self.record_entry.get() + ".bmp"
            cv2.imwrite(im_name, self.image * 255)
        if self.image_processed:
            im_name = folder + "\\" + self.record_entry.get() + "_processed.bmp"
            cv2.imwrite(im_name, self.processed_image * 255)
        if self.FFT_processed:
            im_name = folder + "\\" + self.record_entry.get() + "_FFT.bmp"
            cv2.imwrite(im_name, self.FFT_image_mod)
        #
        txt_name = folder + "\\" + self.record_entry.get() + ".txt"
        if self.image_formed:
            with open(txt_name, mode="w") as f:
                f.write("Name: " + str(self.record_entry.get()) + "\n\n")
                f.write("Artificial image:" + "\n")
                for i in self.processes:
                    f.write(i.rec() + "\n")
                if self.image_processed:
                    f.write("\n" + "Image processing:" + "\n")
                    f.write(
                        "Smooth:"
                        + "\t"
                        + str(self.smooth_entry.get())
                        + "\t"
                        + str(self.smooth_order_cb.get())
                        + "\n"
                    )
                    f.write(
                        "Rotation:"
                        + "\t"
                        + str(self.rot_entry.get())
                        + "\t"
                        + str(self.rot_order_cb.get())
                        + "\n"
                    )
                    f.write(
                        "Resize:"
                        + "\t"
                        + str(self.resize_x_entry.get())
                        + "\t"
                        + str(self.resize_y_entry.get())
                        + "\t"
                        + str(self.resize_order_cb.get())
                        + "\n"
                    )
                    f.write(
                        "Drift:"
                        + "\t"
                        + str(self.drift_x_entry.get())
                        + "\t"
                        + str(self.drift_y_entry.get())
                        + "\t"
                        + str(self.drift_order_cb.get())
                        + "\n"
                    )
                if self.FFT_processed:
                    f.write("\n" + "FF:T" + "\n")
                    f.write("Intensity:" + "\t" + str(self.method_fft_cb.get()) + "\n")
                    f.write("Window:" + "\t" + str(self.window_cb.get()) + "\n")
