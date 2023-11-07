import os
from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont


class Workstation:
    def __init__(self, parent: 'WorkstationFrame'):
        self._parent = parent
        self._cv = Canvas(self._parent.f, width=0, height=0)
        self.x, self.y, self.factor = 0, 0, 1

    def load(self):
        self._cv.grid(row=0, column=0, sticky='nsew')

    def unload(self):
        self._cv.grid_forget()

    def get_original_coordinate(self, x, y):
        x_coord = int((x + self.x) / self.factor)
        y_coord = int((y + self.y) / self.factor)
        return x_coord, y_coord

    def get_original_coordinate_from_points(self, points: list):
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

    def plot_line(self, lines: list, color='red', width=2):
        for line in lines:
            x1, y1, x2, y2 = line
            self._draw.line((x1, y1, x2, y2), fill=color, width=width)
        self._draw_canvas()

    def plot_letters(
            self, positions: list, letters: list, color=(100, 100, 100), fontsize=20,
            font="C:\\Windows\\Fonts\\calibri.ttf", space=15):
        assert len(positions) == len(letters), "positions and letters must have same length"
        font = ImageFont.truetype(font, fontsize)
        canvas_height, canvas_width = self._cv.winfo_height(), self._cv.winfo_width()
        center_x, center_y = canvas_width / 2, canvas_height / 2
        for i, position in enumerate(positions):
            x, y = position
            dir_x, dir_y = center_x -x, center_y - y
            magnitude = (dir_x ** 2 + dir_y ** 2) ** 0.5
            dir_x, dir_y = dir_x / magnitude, dir_y / magnitude
            x, y = int(x + dir_x * space), int(y + dir_y * space)
            self._draw.text((x, y), letters[i], color, font=font)
        self._draw_canvas()

    def reload(self):
        self.x, self.y, self.factor = 0, 0, 1
        if hasattr(self, 'original_image'):
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
        image_width, image_height = self._edited_image.size
        self.x = min(self.x, image_width * self.factor - canvas_width)
        self.y = min(self.y, image_height * self.factor - canvas_height)
        self._draw_canvas()

    def bind_handler(self, key, handler):
        self._cv.bind(key, handler)
