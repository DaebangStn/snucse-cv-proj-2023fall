from tkinter import *
from PIL import Image
from gui.grid_frame import GridFrame
from typing import Tuple, List


class DemoWindow:
    def __init__(self, gui):
        self._gui = gui
        self.root = None
        self._num_images = 0

    def show(self, image_w_labels):
        self.root = Toplevel(self._gui.root)
        self._num_images = len(image_w_labels)
        self._basic_config()
        self._add_widgets(image_w_labels)
        self._set_config()

    def _basic_config(self):
        size = f"{self._num_images * 400}x400"
        self.root.geometry(size)
        self.root.title("Demonstration")

    def _add_widgets(self, image_w_labels: List[Tuple[str, Image]]):
        self.root_gf = GridFrame(self.root)
        self.root_gf.f.grid(column=0, row=0, sticky=(N, S, E, W))

        row = [1 for _ in range(self._num_images)]
        self.main_gf = self.root_gf.add_horizontal_place_child_frame(row)
        for i in range(self._num_images):
            label, image = image_w_labels[i]
            gf = self.main_gf.add_vertical_place_child_frame([0, 1])
            gf.add_description_window("Image " + str(i + 1) + " : " + label)
            gf.add_pillow_image_window(image, 400, 400)

    def _set_config(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root_gf.set_config()
