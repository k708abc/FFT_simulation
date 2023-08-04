from typing import Dict
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from Modules.image_process_class import Plane_wave, Random_offset, Noise


class Window(ttk.Frame):
    padWE: Dict = dict(sticky=(tk.W, tk.E), padx=15, pady=2)

    def __init__(self, master) -> None:
        super().__init__(master, padding=2)
        self.master = master
        master.geometry("655x730")
        master.title("Image tester")
        self.processes = []
        self.create_frame_header()
        self.create_frame_datalist()
        self.create_widgets_buttons()
        self.create_widgets_process()
        self.create_widgets_image_form()
        self.create_widgets_image_process()
        self.create_widgets_contrast()
        self.create_widgets_record()
        self.create_layouts_image()
        self.create_layouts_process()
        self.image_formed = False
        self.image_processed = False
        self.FFT_processed = False

    def init_setting(self):
        self.num_process = len(self.processes)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _no_mousewheel(self, event):
        pass

    def create_frame_header(self):
        self.canvas_index = tk.Canvas(self.master, width=630, height=20, bg="white")
        self.frame_list_index = tk.Frame(self.canvas_index, bg="white")
        self.form_canvas_header()
        self.create_widgets_header()
        self.create_layout_header()

    def form_canvas_header(self):
        self.canvas_index.grid(row=0, column=0, columnspan=5)
        self.canvas_index.create_window(
            (0, 0),
            window=self.frame_list_index,
            anchor=tk.NW,
            width=self.canvas_index.cget("width"),
        )

    def create_widgets_header(self):
        self.header_check_bln = tk.BooleanVar()
        self.header_check_bln.set(False)
        self.header_chk = tk.Checkbutton(
            self.frame_list_index, width=3, text="", variable=self.header_check_bln
        )
        self.header_chk["command"] = self.all_check
        #

        self.header2 = tk.Label(
            self.frame_list_index, width=28, text="Components", background="white"
        )
        self.header3 = tk.Label(
            self.frame_list_index, width=14, text="Parameters", background="white"
        )

    def create_layout_header(self):
        self.header_chk.grid(row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0)
        self.header2.grid(row=0, column=1, padx=1, pady=0, ipadx=0, ipady=0)
        self.header3.grid(row=0, column=2, padx=1, pady=0, ipadx=0, ipady=0)

    def create_frame_datalist(self):
        self.canvas = tk.Canvas(self.master, width=630, height=250, bg="white")
        self.frame_list = tk.Frame(self.canvas, bg="white")
        self.init_setting()
        self.form_canvas_datalist()
        self.create_widgets_datalist()

    def form_canvas_datalist(self):
        self.canvas.grid(
            row=1, rowspan=max(1, self.num_process), column=0, columnspan=5
        )
        #
        vbar = tk.ttk.Scrollbar(self.master, orient=tk.VERTICAL)
        vbar.grid(row=1, rowspan=1000, column=5, sticky="ns")
        #
        vbar.config(command=self.canvas.yview)
        #
        self.canvas.config(yscrollcommand=vbar.set)
        #
        sc_hgt = int(150 / 6 * (self.num_process))
        self.canvas.config(scrollregion=(0, 0, 500, sc_hgt))
        #
        if self.num_process >= 8:
            self.frame_list.bind_all("<MouseWheel>", self._on_mousewheel)
        else:
            self.frame_list.bind_all("<MouseWheel>", self._no_mousewheel)
        self.canvas.create_window(
            (0, 0),
            window=self.frame_list,
            anchor=tk.NW,
            width=self.canvas.cget("width"),
        )

    def create_widgets_datalist(self):
        self.check_list = []
        self.process_vals = []

        for i in range(self.num_process):
            # color set
            if i % 2 == 0:
                color = "#cdfff7"  # blue
            else:
                color = "white"
            # checkbox
            check_bln = tk.BooleanVar()
            check_bln.set(False)
            chk_btn = tk.Checkbutton(
                self.frame_list,
                variable=check_bln,
                width=3,
                text="",
                background="white",
            )
            chk_btn.grid(row=i + 2, column=0, padx=0, pady=0, ipadx=0, ipady=0)
            self.check_list.append(check_bln)
            #
            # process name
            process_name = tk.Label(
                self.frame_list, width=18, text=self.processes[i].name, background=color
            )
            process_name.grid(row=i + 2, column=1, padx=1, pady=0, ipadx=0, ipady=0)
            #
            process_temp = self.get_process_list(self.processes[i], color, i + 1)
            self.process_vals.append(process_temp)

    def get_process_list(self, process, color, num):
        returns = [process.name]
        clm = 2
        for pro_name in process.params:
            text = tk.Label(self.frame_list, width=8, text=pro_name, background=color)
            var = StringVar()
            entry = tk.Entry(
                self.frame_list, width=6, background=color, textvariable=var
            )
            entry.insert(tk.END, process.getval(pro_name))

            text.grid(row=num + 1, column=clm, padx=1, pady=0, ipadx=0, ipady=0)
            entry.grid(row=num + 1, column=clm + 1, padx=1, pady=0, ipadx=0, ipady=0)
            returns.append(var)
            clm += 2
        return returns

    def all_check(self):
        if self.header_check_bln.get():
            for i in self.check_list:
                i.set(True)
        else:
            for i in self.check_list:
                i.set(False)

    def create_widgets_buttons(self):
        self.del_checked_btn = tk.Button(
            self.master,
            text="Delete checked",
            command=self.delete_checked,
            height=1,
            width=18,
        )

    def create_widgets_process(self):
        self.waves_label = tk.Label(self.master, text="Plane wave")
        self.peri_label = tk.Label(self.master, text="Period")
        self.peri_entry = tk.Entry(self.master, width=6)
        self.peri_entry.insert(tk.END, 10)
        self.phase_label = tk.Label(self.master, text="Phase")
        self.phase_entry = tk.Entry(self.master, width=6)
        self.phase_entry.insert(tk.END, 0)
        self.amp_label = tk.Label(self.master, text="Amp.")
        self.amp_entry = tk.Entry(self.master, width=6)
        self.amp_entry.insert(tk.END, 1)
        self.angle_label = tk.Label(self.master, text="Angle")
        self.angle_entry = tk.Entry(self.master, width=6)
        self.angle_entry.insert(tk.END, 0)
        self.wave_btn = tk.Button(
            self.master,
            text="Add",
            command=self.wave_add_clicked,
            height=1,
            width=15,
        )
        #
        self.offset_label = tk.Label(self.master, text="Random offset")
        self.offset_amp_label = tk.Label(self.master, text="Amp.")
        self.offset_amp_entry = tk.Entry(self.master, width=6)
        self.offset_amp_entry.insert(tk.END, 1)
        self.offset_btn = tk.Button(
            self.master,
            text="Add",
            command=self.offset_add_clicked,
            height=1,
            width=15,
        )
        #
        self.noise_label = tk.Label(self.master, text="Noise")
        self.noise_amp_label = tk.Label(self.master, text="Amp.")
        self.noise_amp_entry = tk.Entry(self.master, width=6)
        self.noise_amp_entry.insert(tk.END, 1)
        self.noise_btn = tk.Button(
            self.master,
            text="Add",
            command=self.noise_add_clicked,
            height=1,
            width=15,
        )

    def create_widgets_image_form(self):
        self.pix_x_label = tk.Label(self.master, text="Pixels (x)")
        self.pix_x_entry = tk.Entry(self.master, width=6)
        self.pix_x_entry.insert(tk.END, 256)
        self.pix_y_label = tk.Label(self.master, text="Pixels (y)")
        self.pix_y_entry = tk.Entry(self.master, width=6)
        self.pix_y_entry.insert(tk.END, 256)
        self.image_form_btn = tk.Button(
            self.master,
            text="Forming image",
            command=self.image_form_clicked,
            height=1,
            width=25,
        )

    def create_widgets_image_process(self):
        self.order_table = ["1", "2", "3", "4", "Off"]
        #
        self.smooth_label = tk.Label(self.master, text="Smooth")
        self.smooth_entry = tk.Entry(self.master, width=6)
        self.smooth_entry.insert(tk.END, 0)
        #
        self.smooth_order_var = tk.StringVar()
        self.smooth_order_cb = ttk.Combobox(
            self.master,
            textvariable=self.smooth_order_var,
            values=self.order_table,
            width=10,
        )
        self.smooth_order_cb.bind("<<ComboboxSelected>>", self.smooth_order_selected)
        self.smooth_order_cb.current(0)
        self.prev_smooth_val = 0
        #
        self.rot_label = tk.Label(self.master, text="Rotation")
        self.rot_entry = tk.Entry(self.master, width=6)
        self.rot_entry.insert(tk.END, 0)
        #
        self.rot_order_var = tk.StringVar()
        self.rot_order_cb = ttk.Combobox(
            self.master,
            textvariable=self.rot_order_var,
            values=self.order_table,
            width=10,
        )
        self.rot_order_cb.bind("<<ComboboxSelected>>", self.rot_order_selected)
        self.rot_order_cb.current(1)
        self.prev_rot_val = 1
        #
        self.resize_label = tk.Label(self.master, text="Resize")
        self.resize_x_label = tk.Label(self.master, text="x")
        self.resize_y_label = tk.Label(self.master, text="y")
        self.resize_x_entry = tk.Entry(self.master, width=6)
        self.resize_x_entry.insert(tk.END, 256)
        self.resize_y_entry = tk.Entry(self.master, width=6)
        self.resize_y_entry.insert(tk.END, 256)
        #
        self.resize_order_var = tk.StringVar()
        self.resize_order_cb = ttk.Combobox(
            self.master,
            textvariable=self.resize_order_var,
            values=self.order_table,
            width=10,
        )
        self.resize_order_cb.bind("<<ComboboxSelected>>", self.resize_order_selected)
        self.resize_order_cb.current(2)
        self.prev_resize_val = 2
        #
        self.drift_label = tk.Label(self.master, text="Drift")
        self.drift_x_label = tk.Label(self.master, text="x (pix/scan)")
        self.drift_y_label = tk.Label(self.master, text="y (pix/scan)")
        self.drift_x_entry = tk.Entry(self.master, width=6)
        self.drift_x_entry.insert(tk.END, 0)
        self.drift_y_entry = tk.Entry(self.master, width=6)
        self.drift_y_entry.insert(tk.END, 0)
        #
        self.drift_order_var = tk.StringVar()
        self.drift_order_cb = ttk.Combobox(
            self.master,
            textvariable=self.drift_order_var,
            values=self.order_table,
            width=10,
        )
        self.drift_order_cb.bind("<<ComboboxSelected>>", self.drift_order_selected)
        self.drift_order_cb.current(3)
        self.prev_drift_val = 3
        #
        self.image_process_btn = tk.Button(
            self.master,
            text="Processing",
            command=self.image_process_clicked,
            height=7,
            width=15,
        )
        #
        self.FFT_label = tk.Label(self.master, text="FFT")
        self.FFT_btn = tk.Button(
            self.master,
            text="FFT",
            command=self.FFT_clicked,
            height=3,
            width=15,
        )
        #
        self.method_fft_var = tk.StringVar()
        self.method_fft_table = ["Linear", "Sqrt", "Log"]
        self.method_fft_cb = ttk.Combobox(
            self.master,
            textvariable=self.method_fft_var,
            values=self.method_fft_table,
        )
        self.method_fft_cb.bind("<<ComboboxSelected>>", self.cb_method_selected)
        self.method_fft_cb.current(1)
        self.method_text = ttk.Label(self.master, text="Intensity")
        #
        self.fft_window_var = tk.StringVar()
        self.window_table = ["None", "Hann", "Hamming", "Blackman"]
        self.window_cb = ttk.Combobox(
            self.master, textvariable=self.fft_window_var, values=self.window_table
        )
        self.window_cb.bind("<<ComboboxSelected>>", self.cb_window_selected)
        self.window_cb.current(0)
        self.window_text = ttk.Label(self.master, text="Window")
        #

    def create_widgets_contrast(self):
        self.upper_val = tk.DoubleVar()
        self.def_max = 255
        self.upper_val.set(self.def_max)
        self.upper_val.trace("w", self.upper_value_change)
        self.scale_upper = ttk.Scale(
            self.master,
            variable=self.upper_val,
            orient=tk.HORIZONTAL,
            length=300,
            from_=-50,
            to=300,
        )
        #
        self.lower_val = tk.DoubleVar()
        self.def_min = 0
        self.lower_val.set(self.def_min)
        self.lower_val.trace("w", self.lower_value_change)
        self.scale_lower = ttk.Scale(
            self.master,
            variable=self.lower_val,
            orient=tk.HORIZONTAL,
            length=300,
            from_=-50,
            to=300,
        )
        self.upper_text = ttk.Label(self.master, text="Upper")
        self.lower_text = ttk.Label(self.master, text="lower")

    def create_widgets_record(self):
        self.record_label = tk.Label(self.master, text="Record name")
        self.record_entry = tk.Entry(self.master, width=40)
        self.record_entry.insert(tk.END, "artificial_image")
        self.record_btn = tk.Button(
            self.master,
            text="Record",
            command=self.record_clicked,
            height=1,
            width=15,
        )

    def create_layouts_image(self):
        y_1 = 280
        y_2 = y_1 + 40
        y_3 = y_2 + 30
        y_4 = y_3 + 30
        x_1 = 20
        x_2 = 120
        x_3 = 170
        x_4 = 220
        x_5 = 270
        x_6 = 320
        x_7 = 370
        x_8 = 420
        x_9 = 470
        x_btn = 520
        #
        # self.components_label.place(x=20, y=y_1)
        self.del_checked_btn.place(x=20, y=y_1)
        self.pix_x_label.place(x=180, y=y_1 + 2)
        self.pix_x_entry.place(x=250, y=y_1 + 2)
        self.pix_y_label.place(x=310, y=y_1 + 2)
        self.pix_y_entry.place(x=380, y=y_1 + 2)
        self.image_form_btn.place(x=450, y=y_1)
        #
        self.waves_label.place(x=x_1, y=y_2)
        self.peri_label.place(x=x_2, y=y_2)
        self.peri_entry.place(x=x_3, y=y_2)
        self.phase_label.place(x=x_4, y=y_2)
        self.phase_entry.place(x=x_5, y=y_2)
        self.amp_label.place(x=x_6, y=y_2)
        self.amp_entry.place(x=x_7, y=y_2)
        self.angle_label.place(x=x_8, y=y_2)
        self.angle_entry.place(x=x_9, y=y_2)
        self.wave_btn.place(x=x_btn, y=y_2)
        #
        self.offset_label.place(x=x_1, y=y_3)
        self.offset_amp_label.place(x=x_2, y=y_3)
        self.offset_amp_entry.place(x=x_3, y=y_3)
        self.offset_btn.place(x=x_btn, y=y_3)
        #
        self.noise_label.place(x=x_1, y=y_4)
        self.noise_amp_label.place(x=x_2, y=y_4)
        self.noise_amp_entry.place(x=x_3, y=y_4)
        self.noise_btn.place(x=x_btn, y=y_4)
        #

    def create_layouts_process(self):
        y_1 = 420
        y_2 = y_1 + 30
        y_3 = y_2 + 30
        y_4 = y_3 + 30
        y_5 = y_4 + 30
        y_6 = y_5 + 30
        y_7 = y_6 + 50
        y_8 = y_7 + 30
        y_9 = y_8 + 40
        x_1 = 20
        x_2 = 120
        x_3 = 170
        x_4 = 220
        x_5 = 270
        x_6 = 320
        x_7 = 370
        x_8 = 420
        x_9 = 470
        x_btn = 520
        self.smooth_label.place(x=x_1, y=y_1)
        self.smooth_entry.place(x=x_2, y=y_1)
        self.smooth_order_cb.place(x=x_8 - 30, y=y_1)
        #
        self.rot_label.place(x=x_1, y=y_2)
        self.rot_entry.place(x=x_2, y=y_2)
        self.rot_order_cb.place(x=x_8 - 30, y=y_2)
        #
        #
        self.resize_label.place(x=x_1, y=y_3)
        self.resize_x_label.place(x=x_2, y=y_3)
        self.resize_y_label.place(x=x_4, y=y_3)
        self.resize_x_entry.place(x=x_3, y=y_3)
        self.resize_y_entry.place(x=x_5, y=y_3)
        self.resize_order_cb.place(x=x_8 - 30, y=y_3)
        #
        self.drift_label.place(x=x_1, y=y_4)
        self.drift_x_label.place(x=x_2, y=y_4)
        self.drift_y_label.place(x=x_5 - 30, y=y_4)
        self.drift_x_entry.place(x=x_4 - 30, y=y_4)
        self.drift_y_entry.place(x=x_7 - 60, y=y_4)
        self.drift_order_cb.place(x=x_8 - 30, y=y_4)
        #
        self.image_process_btn.place(x=x_btn, y=y_1)
        #
        self.FFT_label.place(x=x_1, y=y_5 + 20)
        self.FFT_btn.place(x=x_btn, y=y_5 + 20)
        self.method_text.place(x=x_2, y=y_5 + 20)
        self.method_fft_cb.place(x=x_4, y=y_5 + 20)

        self.window_text.place(x=x_2, y=y_6 + 20)
        self.window_cb.place(x=x_4, y=y_6 + 20)
        #
        self.scale_upper.place(x=x_2, y=y_7)
        self.scale_lower.place(x=x_2, y=y_8)
        self.upper_text.place(x=x_1, y=y_7)
        self.lower_text.place(x=x_1, y=y_8)
        #
        self.record_label.place(x=x_1, y=y_9)
        self.record_entry.place(x=x_2, y=y_9)
        self.record_btn.place(x=x_btn, y=y_9)

    def wave_add_clicked(self):
        var = Plane_wave()
        var.period = float(self.peri_entry.get())
        var.phase = float(self.phase_entry.get())
        var.amp = float(self.amp_entry.get())
        var.angle = float(self.angle_entry.get())
        self.processes.append(var)
        self.update_process_w()

    def offset_add_clicked(self):
        var = Random_offset()
        var.amp = float(self.offset_amp_entry.get())
        self.processes.append(var)
        self.update_process_w()

    def noise_add_clicked(self):
        var = Noise()
        var.amp = float(self.noise_amp_entry.get())
        self.processes.append(var)
        self.update_process_w()

    def image_form_clicked(self):
        self.rewrite_process()
        self.image_formation()
        self.image_formed = True

    def image_process_clicked(self):
        if self.image_formed:
            self.image_processing()
            self.image_processed = True

    def FFT_clicked(self):
        if self.image_processed:
            self.image_FFT = self.FFT_process(
                self.processed_image, self.method_fft_cb.get(), self.window_cb.get()
            )
            self.FFT_image = self.normarize(self.image_FFT)
            self.show_FFT()
            self.FFT_processed = True
        elif self.image_formed:
            self.image_FFT = self.FFT_process(
                self.image, self.method_fft_cb.get(), self.window_cb.get()
            )
            self.FFT_image = self.normarize(self.image_FFT)
            self.show_FFT()
            self.FFT_processed = True

    def update_process_w(self):
        self.create_frame_datalist()

    def delete_checked(self):
        self.rewrite_process()
        for i, chk in enumerate(self.check_list):
            if chk.get():
                self.processes[i] = None
        self.processes = [pro for pro in self.processes if pro is not None]
        self.create_frame_datalist()

    def rewrite_process(self):
        for i in range(len(self.process_vals)):
            params = []
            count = 0
            for vals in self.process_vals[i]:
                if count == 0:
                    count = 1
                else:
                    params.append(float(vals.get()))
            self.processes[i].rewrite(params)

    def cb_method_selected(self, event):
        pass

    def cb_window_selected(self, event):
        pass

    def reorder(self, current, prev, val):
        if current == 4:
            pass
        elif current == prev:
            pass
        else:
            if current == self.smooth_order_cb.current() and val != 0:
                self.smooth_order_cb.current(prev)
                self.prev_smooth_val = prev

            elif current == self.rot_order_cb.current() and val != 1:
                self.rot_order_cb.current(prev)
                self.prev_rot_val = prev

            elif current == self.resize_order_cb.current() and val != 2:
                self.resize_order_cb.current(prev)
                self.prev_resize_val = prev

            elif current == self.drift_order_cb.current() and val != 3:
                self.drift_order_cb.current(prev)
                self.prev_drift_val = prev

    def smooth_order_selected(self, event):
        current = self.smooth_order_cb.current()
        self.reorder(current, self.prev_smooth_val, 0)
        self.prev_smooth_val = current

    def rot_order_selected(self, event):
        current = self.rot_order_cb.current()
        self.reorder(current, self.prev_rot_val, 1)
        self.prev_rot_val = current

    def resize_order_selected(self, event):
        current = self.resize_order_cb.current()
        self.reorder(current, self.prev_resize_val, 2)
        self.prev_resize_val = current

    def drift_order_selected(self, event):
        current = self.drift_order_cb.current()
        self.reorder(current, self.prev_drift_val, 3)
        self.prev_drift_val = current

    def record_clicked(self):
        self.record_function()

    def upper_value_change(self, *args):
        if self.FFT_processed:
            self.show_FFT()

    def lower_value_change(self, *args):
        if self.FFT_processed:
            self.show_FFT()

    def run(self):
        self.mainloop()
