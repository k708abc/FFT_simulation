import tkinter as tk
from Modules.preference_window import Window
from Modules.functions import functions


class App(Window, functions):
    def __init__(self, master):
        super().__init__(master)


if __name__ == "__main__":
    print("Last update: 13 th Sep. 2023 by N. Kawakami")
    application = tk.Tk()
    app = App(application)
    app.run()
