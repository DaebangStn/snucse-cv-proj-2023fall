from tkinter import *
from gui.grid_frame import GridFrame


class Root:
    def __init__(self):
        self.root = Tk()
        self.basic_config(self.root)

        self.root_gf = GridFrame(self.root)
        self.add_widgets()
        self.set_config()

    @staticmethod
    def basic_config(root):
        root.geometry("800x600")
        root.title("Camera Calibration with Non-checkerboard Object")
        root.option_add('*tearOff', FALSE)

    def set_config(self):
        self.root_gf.f.grid(column=0, row=0, sticky=(N, S, E, W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root_gf.set_config()

    def add_widgets(self):
        self.main_gf = self.root_gf.add_vertical_place_child_frame([3, 1])

        self.top_gf = self.main_gf.add_horizontal_place_child_frame([3, 1])
        self.image = self.top_gf.add_canvas()
        self.listbox = self.top_gf.add_listbox()

        self.bottom_gf = self.main_gf.add_horizontal_place_child_frame([1, 1])
        self.text_command = self.bottom_gf.add_text_box()
        self.text_output = self.bottom_gf.add_text_box()
