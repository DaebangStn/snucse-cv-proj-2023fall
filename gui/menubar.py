from tkinter import *


class Menubar:
    def __init__(self, root):
        self.menubar = Menu(root)
        root['menu'] = self.menubar

    def add_command(self, name, command):
        self.menubar.add_command(label=name, command=command)
