from tkinter import *
from PIL import ImageTk, Image


class PillowImageWindow:
    def __init__(self, parent: 'GridFrame', image, width, height):
        self._parent = parent
        self._cv = Canvas(self._parent.f, width=0, height=0)
        image = image.resize((width, height), resample=Image.Resampling.HAMMING)
        self._image = ImageTk.PhotoImage(image)
        self._cv.create_image(0, 0, image=self._image, anchor=NW)

    def grid(self, row, column, sticky):
        self._cv.grid(row=row, column=column, sticky=sticky)
