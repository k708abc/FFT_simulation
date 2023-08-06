import numpy as np
import cv2
import os


class functions:
    def init_setting(self):
        pass

    def image_formation(self):
        px = int(self.pix_x_entry.get())
        py = int(self.pix_y_entry.get())
        for i in range(len(self.processes)):
            if i in (0, 1):
                image_rec = [np.ones((px, py))]
            else:
                if self.marge_select == 0:
                    image_rec = [self.images[0][1] + self.images[1][1]]
                elif self.marge_select == 1:
                    image_rec = [self.images[0][1] - self.images[1][1]]
                elif self.marge_select == 2:
                    image_rec = [self.images[0][1] * self.images[1][1]]  
            for k in self.processes[i][0]:
                k.px = px
                k.py = py
                image_rec.append(k.run())
            image = np.sum(image_rec, axis=0)
            image = self.normarize(image)
            self.images[i].image = np.copy(image)
            #
            for k in self.processes[i][1]:
                k.image = image
                image = k.run()
            image = self.normarize(image)
            self.images[i + 1].image = np.copy(image)
            #
            #
            #
            #FFTもここで作成する
        self.show_image()

    def show_image(self):
        cv2.imshow("Original image 1", self.images[0][0])
        cv2.imshow("Processed image 1", self.images[0][1])
        cv2.imshow("Original image 2", self.images[1][0])
        cv2.imshow("Processed image 2", self.images[1][1])
        cv2.imshow("Total image", self.images[2][0])
        cv2.imshow("Processed total image", self.images[2][1])  

    def normarize(self, image):
        val_min = np.min(image)
        val_max = np.max(image)
        diff = val_max - val_min
        if diff == 0:
            return image
        new_image = (image - val_min) / diff
        return new_image
    

    def show_FFT(self):
        upper, lower = self.current_contrast()
        self.FFT_image_mod = self.contrast_change(self.FFT_image, upper, lower)
        cv2.imshow("FFT image", self.FFT_image_mod)



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
