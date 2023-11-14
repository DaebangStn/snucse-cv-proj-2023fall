from tkinter import *
from gui.main_controller import MainController
from gui.grid_frame import GridFrame
from gui.workstation_frame import WorkstationFrame
from gui.log_frame import LogFrame
from gui.menubar import Menubar


class GUI:
    def __init__(self):
        self.root = Tk()
        self._basic_config()

        self._add_menubar()
        self._add_widgets()
        self._set_config()

        self.io_handler = MainController(self.root_gf, self._menubar)

    def _basic_config(self):
        self.root.geometry("400x400")
        self.root.title("Camera Calibration with Non-checkerboard Object")


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
        self.ws_f = self.top_gf.add_ws_frame()

        self.state_f = self.top_gf.add_vertical_place_child_frame([0, 1, 0, 1])

        self.d1 = self.state_f.add_description_window("Working Directory")
        self.lb1 = self.state_f.add_photo_manager()
        self.d2 = self.state_f.add_description_window("Opened Images")
        self.lb2 = self.state_f.add_text_window()

        self.bottom_gf = self.main_gf.add_horizontal_place_child_frame([1, 1])

        self.command_f = self.bottom_gf.add_vertical_place_child_frame([0, 1])
        self.d3 = self.command_f.add_description_window("Command")
        self.text_command = self.command_f.add_command_window()
        self.log_f = self.bottom_gf.add_vertical_place_child_frame([0, 1])
        self.d4 = self.log_f.add_description_window("Log")
        self.text_log = self.log_f.add_log_window()

    def run(self):
        self.root.mainloop()
