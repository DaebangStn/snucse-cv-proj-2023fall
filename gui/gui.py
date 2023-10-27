from tkinter import *
from gui.main_controller import MainController
from gui.grid_frame import GridFrame
from gui.log_frame import LogFrame
from gui.menubar import Menubar


class GUI:
    def __init__(self):
        self.root = Tk()
        self._basic_config(self.root)

        self._add_menubar()
        self._add_widgets()
        self._set_config()

        self.io_handler = MainController(self.root_gf, self._menubar)

    @staticmethod
    def _basic_config(root):
        root.geometry("400x400")
        root.title("Camera Calibration with Non-checkerboard Object")

    def _set_config(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root_gf.set_config()

    def _add_menubar(self):
        self.root.option_add('*tearOff', FALSE)
        self._menubar = Menubar(self.root)

    def _add_widgets(self):
        self.root_gf = GridFrame(self.root)
        self.root_gf.f.grid(column=0, row=0, sticky=(N, S, E, W))

        self.main_gf = self.root_gf.add_vertical_place_child_frame([3, 1])

        self.top_gf = self.main_gf.add_horizontal_place_child_frame([3, 1])
        self.image = self.top_gf.add_photo_workstation()
        self.listbox = self.top_gf.add_photo_manager()

        self.bottom_gf = self.main_gf.add_horizontal_place_child_frame([1, 1])
        self.text_command = self.bottom_gf.add_command_window()
        self.text_output = LogFrame(self.bottom_gf)

    def run(self):
        self.root.mainloop()
