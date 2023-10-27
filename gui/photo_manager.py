import os
from tkinter import *


class PhotoManager:
    def __init__(self, parent: 'GridFrame'):
        self._parent = parent
        self._lb = Listbox(self._parent.f, width=0, height=0)
        self._files = []
        self._folder_path = None
        self.update_list()

    def grid(self, row, column, sticky):
        self._lb.grid(row=row, column=column, sticky=sticky)

    def set_folder(self, path: str = None):
        self._folder_path = path
        self.update_list()

    def update_list(self):
        self._files = []
        if self._folder_path is None:
            self._folder_path = self.get_default_image_path()
        self._lb.delete(0, END)
        for file in os.listdir(self._folder_path):
            if os.path.isfile(os.path.join(self._folder_path, file)):
                self._lb.insert(END, file)
                self._files.append(file)

    def get_item_count(self):
        return self._lb.size()

    def get_image_folder_path(self):
        return self._folder_path

    def get_selected_image_filename(self):
        assert self._lb.curselection(), "no image selected"
        return self._files[self._lb.curselection()[0]]

    def get_selected_image_path(self):
        assert self._lb.curselection(), "no image selected"
        return os.path.join(self._folder_path, self.get_selected_image_filename())

    def bind_handler(self, key, handler):
        self._lb.bind(key, handler)

    @staticmethod
    def get_default_image_path():
        path = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(path)
        return os.path.join(root, "img")
