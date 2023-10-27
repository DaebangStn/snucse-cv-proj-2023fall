import os
from tkinter import *
from PIL import ImageTk, Image


class Workstation:
    def __init__(self, parent: 'GridFrame'):
        self._parent = parent
        self._cv = Canvas(self._parent.f, width=0, height=0)

    def grid(self, row, column, sticky):
        self._cv.grid(row=row, column=column, sticky=sticky)

    def set_image(self, path: str):
        if not os.path.isfile(path):
            raise Exception("file not exist")
        self._cv.delete("all")
        image = Image.open(path)
        self.imgPIL = image
        self._cv.image = ImageTk.PhotoImage(image)
        self._cv.create_image(0, 0, image=self._cv.image, anchor=NW)

    def plot_point(self, x, y, color='red', size=5):
        self._cv.create_oval(x - size, y - size, x + size, y + size, fill=color)

    def reload(self):
        self._cv.image = ImageTk.PhotoImage(self.imgPIL)
        self._cv.create_image(0, 0, image=self._cv.image, anchor=NW)

    def bind_handler(self, key, handler):
        self._cv.bind(key, handler)
