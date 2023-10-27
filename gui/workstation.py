import os
from tkinter import *
from PIL import ImageTk, Image, ImageDraw


class Workstation:
    def __init__(self, parent: 'GridFrame'):
        self._parent = parent
        self._cv = Canvas(self._parent.f, width=0, height=0)
        self.x, self.y, self.factor = 0, 0, 1

    def get_original_coordinate(self, x, y):
        x_coord = int((x + self.x) / self.factor)
        y_coord = int((y + self.y) / self.factor)
        return x_coord, y_coord

    def get_original_coordinate_from_point(self, points: list):
        converted = []
        for point in points:
            x, y = self.get_original_coordinate(point[0], point[1])
            converted.append((x, y))
        return converted

    def _draw_canvas(self):
        size = self._edited_image.size
        size = (int(size[0] * self.factor), int(size[1] * self.factor))
        resized = self._edited_image.resize(size)
        cropped = resized.crop((self.x, self.y, size[0], size[1]))
        self._cv.image = ImageTk.PhotoImage(cropped)
        self._cv.create_image(0, 0, image=self._cv.image, anchor=NW)

    def grid(self, row, column, sticky):
        self._cv.grid(row=row, column=column, sticky=sticky)

    def set_image(self, path: str):
        if not os.path.isfile(path):
            raise Exception("file not exist")
        self._cv.delete("all")
        self.original_image = Image.open(path)
        self._edited_image = self.original_image.copy()
        self._draw = ImageDraw.Draw(self._edited_image)
        self._draw_canvas()

    def plot_point(self, points: list, color='red', size=5):
        for point in points:
            x, y = point
            self._draw.ellipse((x - size, y - size, x + size, y + size), fill=color)
        self._draw_canvas()

    def reload(self):
        self.x, self.y, self.factor = 0, 0, 1
        self._edited_image = self.original_image.copy()
        self._draw = ImageDraw.Draw(self._edited_image)
        self._draw_canvas()

    def zoom(self, factor):
        self.factor *= factor
        self._draw_canvas()

    def move_image(self, x, y):
        self.x += x
        self.y += y
        self.x, self.y = max(self.x, 0), max(self.y, 0)
        canvas_height, canvas_width = self._cv.winfo_height(), self._cv.winfo_width()
        image_height, image_width = self._edited_image.size
        self.x, self.y = min(self.x, image_width - canvas_width), min(self.y, image_height - canvas_height)
        self._draw_canvas()

    def bind_handler(self, key, handler):
        self._cv.bind(key, handler)
