import os
from tkinter import *
from PIL import ImageTk, Image


class PhotoWorkstation:
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
        self._cv.image = ImageTk.PhotoImage(image)
        self._cv.create_image(0, 0, image=self._cv.image, anchor=NW)
