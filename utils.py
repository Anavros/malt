# Double Malt -> Utils

import tkinter as tk
from contextlib import contextmanager

GUI_TEXT_FIELD = ""
GUI_LAST_INPUT = ""

class Window(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.displayed = tk.StringVar()

        self.output = tk.Label(root, textvariable=self.displayed)
        self.output.config(anchor=tk.SW, justify=tk.LEFT, width=50, height=20)
        self.output.config(relief=tk.RIDGE, bg='gray15', fg='ivory2')
        self.output.config(font="Courier 11")

        self.entry = tk.Entry(root, width=50)
        self.entry.bind("<Return>", self.submit)
        self.entry.config(font="Courier 11")

        self.output.pack()
        self.entry.pack()

        self.entry.focus_set()

    def submit(self, event):
        text = self.entry.get().strip()
        gui_print(text)
        self.clear()
        self.update()

    def update(self):
        self.displayed = GUI_TEXT_FIELD

    def clear(self):
        self.entry.delete(0, tk.END)

    def close(self):
        self.root.quit()


@contextmanager
def gui():
    _init_gui()
    try:
        yield
    finally:
        _exit_gui():


def _init_gui():
    global USE_GUI
    USE_GUI = True
    root = tk.Tk()
    app = Window(root)
    root.mainloop()


def _exit_gui():
    pass


def gui_print(text):
    GUI_TEXT_FIELD += ('\n' + text)


def gui_input():
    return GUI_LAST_INPUT
