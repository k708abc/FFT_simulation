import numpy as np
import cv2
import os
from Modules.image_process_class import FFT


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
                    image_rec = [self.images[1].image + self.images[5].image]
                elif self.marge_select == 1:
                    image_rec = [self.images[1].image - self.images[5].image]
                elif self.marge_select == 2:
                    image_rec = [self.images[1].image * self.images[5].image]
            for k in self.processes[i][0]:
                k.px = px
                k.py = py
                image_rec.append(k.run())
            image = np.sum(image_rec, axis=0)
            image_or = self.normarize(image)
            self.images[4 * i].image = np.copy(image_or)
            self.images[4 * i].form_mod()
            #
            for k in self.processes[i][1]:
                k.image = image
                image = k.run()
            image_pro = self.normarize(image)
            self.images[4 * i + 1].image = np.copy(image_pro)
            self.images[4 * i + 1].form_mod()
            #
            FFT_image = FFT()
            FFT_image.window = self.window_cb.get()
            FFT_image.scaling = self.method_fft_cb.get()
            FFT_image.image = np.copy(image_or)
            FFT_image.ccut = self.ccut_check_bln.get()
            image_fft = FFT_image.run()
            self.images[4 * i + 2].image = self.normarize(np.copy(image_fft))
            self.images[4 * i + 2].form_mod()
            #
            FFT_image.image = np.copy(image_pro)
            image_fft = self.normarize(FFT_image.run())
            self.images[4 * i + 3].image = np.copy(image_fft)
            self.images[4 * i + 3].form_mod()
        self.show_image()

    def form_each(self, img_list, name_list, val_list, offset):
        x = 0
        y = 0
        for img in img_list:
            x += img.shape[1] + 10
            y = max(y, img.shape[0])
        y = y + 30
        image = np.zeros((y, x))
        x_total = 10
        for img, name, i in zip(img_list, name_list, val_list):
            height, width = img.shape[:2]
            image[0:height, x_total : x_total + width] = img
            self.images[i].pos_x1 = x_total
            self.images[i].pos_x2 = x_total + width
            self.images[i].pos_y1 = 0 + offset
            self.images[i].pos_y2 = height + offset
            cv2.putText(
                image,
                text=name,
                org=(x_total, y - 15),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(255, 255, 255),
                thickness=1,
                lineType=cv2.LINE_4,
            )
            x_total += width + 10
        return image

    def clese_each(self):
        for var in self.images:
            var.unshow()

    def close_uni_each(self):
        try:
            cv2.destroyWindow("First images")
        except:
            pass
        try:
            cv2.destroyWindow("Second images")
        except:
            pass
        try:
            cv2.destroyWindow("Total images")
        except:
            pass

    def close_uni_all(self):
        try:
            cv2.destroyWindow("Images")
        except:
            pass

    def image_close(self):
        if self.uni_each_bln.get():
            self.clese_each()
            self.close_uni_all()
        elif self.uni_all_bln.get():
            self.clese_each()
            self.close_uni_each()
        else:
            self.close_uni_each()
            self.close_uni_all()

    def show_image(self):
        self.image_close()
        if self.uni_each_bln.get() or self.uni_all_bln.get():
            self.show_type = 1
            images_1 = []
            images_1_name = []
            images_1_val = []
            images_2 = []
            images_2_name = []
            images_2_val = []
            images_3 = []
            images_3_name = []
            images_3_val = []
            for i, var in enumerate(self.show_bool_list):
                if i in (0, 1, 2, 3):
                    if var.get():
                        images_1.append(self.images[i].mod_image)
                        images_1_name.append(self.images[i].name)
                        images_1_val.append(i)
                if i in (4, 5, 6, 7):
                    if var.get():
                        images_2.append(self.images[i].mod_image)
                        images_2_name.append(self.images[i].name)
                        images_2_val.append(i)
                if i in (8, 9, 10, 11):
                    if var.get():
                        images_3.append(self.images[i].mod_image)
                        images_3_name.append(self.images[i].name)
                        images_3_val.append(i)
            #
            if self.uni_all_bln.get():
                offset = 10
            else:
                offset = 0
            if len(images_1) != 0:
                self.image1 = self.form_each(
                    images_1, images_1_name, images_1_val, offset
                )
                if self.uni_each_bln.get():
                    cv2.imshow("First images", self.image1)
                    self.show_type = 1
                if self.uni_all_bln.get():
                    offset += len(self.image1)
            else:
                self.image1 = np.zeros((0, 0))
            if len(images_2) != 0:
                self.image2 = self.form_each(
                    images_2, images_2_name, images_2_val, offset
                )
                if self.uni_each_bln.get():
                    cv2.imshow("Second images", self.image2)
                    self.show_type = 1
                if self.uni_all_bln.get():
                    offset += len(self.image2)
            else:
                self.image2 = np.zeros((0, 0))
            if len(images_3) != 0:
                self.image3 = self.form_each(
                    images_3, images_3_name, images_3_val, offset
                )
                if self.uni_each_bln.get():
                    cv2.imshow("Total images", self.image3)
                    self.show_type = 1
            else:
                self.image3 = np.zeros((0, 0))
            if self.uni_all_bln.get():
                self.show_type = 2
                y1, x1 = self.image1.shape[:2]
                y2, x2 = self.image2.shape[:2]
                y3, x3 = self.image3.shape[:2]
                #
                width = max(x1, x2, x3)
                height = y1 + y2 + y3 + 10
                self.int_image = np.zeros((height, width))
                self.int_image[10 : y1 + 10, 0:x1] = self.image1
                self.int_image[y1 + 10 : y1 + y2 + 10, 0:x2] = self.image2
                self.int_image[y1 + y2 + 10 : y1 + y2 + y3 + 10, 0:x3] = self.image3
                cv2.imshow("Images", self.int_image)
                self.show_type = 2

        else:
            self.show_type = 0
            for i, var in enumerate(self.show_bool_list):
                if var.get():
                    self.images[i].shown = True
                    self.images[i].show()
                else:
                    self.images[i].unshow()

    def normarize(self, image):
        val_min = np.min(image)
        val_max = np.max(image)
        diff = val_max - val_min
        if diff == 0:
            return image
        new_image = (image - val_min) / diff
        return new_image

    #
    def record_function(self):
        folder = self.record_fol_entry.get()
        if os.path.isdir(folder) is False:
            os.makedirs(folder)
        file = self.record_file_entry.get()
        rec_name = folder + "\\" + file
        for var in self.images:
            var.rec_name = rec_name
            var.record()

        if self.show_type == 1:
            if len(self.image1) > 1:
                rec_name = folder + "\\" + file + "_1.bmp"
                cv2.imwrite(rec_name, self.image1)
            if len(self.image2) > 1:
                rec_name = folder + "\\" + file + "_2.bmp"
                cv2.imwrite(rec_name, self.image2)
            if len(self.image3) > 1:
                rec_name = folder + "\\" + file + "_total.bmp"
                cv2.imwrite(rec_name, self.image3)

        elif self.show_type == 2:
            rec_name = folder + "\\" + file + "_int.bmp"
            cv2.imwrite(rec_name, self.int_image)

        #
        txt_name = rec_name + ".txt"
        if self.image_formed:
            with open(txt_name, mode="w") as f:
                f.write("Name: " + str(self.record_file_entry.get()) + "\n\n")
                f.write("First image:" + "\n")
                for i in self.processes[0][0]:
                    f.write(i.rec() + "\n")
                for i in self.processes[0][1]:
                    f.write(i.rec() + "\n")
                f.write("Second image:" + "\n")
                for i in self.processes[1][0]:
                    f.write(i.rec() + "\n")
                for i in self.processes[1][1]:
                    f.write(i.rec() + "\n")
                f.write(
                    "Total image:" + "\t" + "Type: " + "\t" + str(self.marge_cb) + "\n"
                )
                for i in self.processes[2][0]:
                    f.write(i.rec() + "\n")
                for i in self.processes[2][1]:
                    f.write(i.rec() + "\n")

                f.write("\n" + "FFT" + "\n")
                f.write("Intensity:" + "\t" + str(self.method_fft_cb.get()) + "\n")
                f.write("Window:" + "\t" + str(self.window_cb.get()) + "\n")

    def cont_change_show(self):
        if self.show_type == 0:
            self.images[self.im_select].show()
        elif self.show_type == 1:
            x1 = self.images[self.im_select].pos_x1
            x2 = self.images[self.im_select].pos_x2
            y1 = self.images[self.im_select].pos_y1
            y2 = self.images[self.im_select].pos_y2
            if self.im_select in (0, 1, 2, 3):
                self.image1[y1:y2, x1:x2] = self.images[self.im_select].mod_image
                cv2.imshow("First images", self.image1)
            elif self.im_select in (4, 5, 6, 7):
                self.image2[y1:y2, x1:x2] = self.images[self.im_select].mod_image
                cv2.imshow("Second images", self.image2)
            else:
                self.image3[y1:y2, x1:x2] = self.images[self.im_select].mod_image
                cv2.imshow("Total images", self.image3)
        else:
            self.int_image[y1:y2, x1:x2] = self.images[self.im_select].mod_image
