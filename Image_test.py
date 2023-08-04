import tkinter as tk
from Modules.preference_window import Window
from Modules.functions import functions
from Modules.image_process_class import image_modifier


class App(Window, functions, image_modifier):
    def __init__(self, master):
        super().__init__(master)


if __name__ == "__main__":
    print("Last update: 4 th Aug. 2023 by N. Kawakami")
    application = tk.Tk()
    app = App(application)
    app.run()
