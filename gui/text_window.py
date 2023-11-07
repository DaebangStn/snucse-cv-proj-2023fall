from tkinter import *


class TextWindow:
    def __init__(self, parent: 'GridFrame'):
        self._parent = parent
        self._text_box = Text(self._parent.f, wrap=WORD, width=0, height=0, fg="black", bg="white")
        self._text_box.configure(font=("D2Coding", 10))

    def grid(self, row, column, sticky):
        self._text_box.grid(row=row, column=column, sticky=sticky)

    def append(self, text: str):
        self._text_box.configure(state='normal')
        self._text_box.insert(END, text)

    def clear(self):
        self._text_box.configure(state='normal')
        self._text_box.delete('1.0', END)

    def set_scrollbar(self, scrollbar: Scrollbar):
        self._text_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self._text_box.yview)

    def set_color(self, fg, bg):
        self._text_box.configure(fg=fg, bg=bg)

class LogWindow(TextWindow):
    def __init__(self, parent: 'GridFrame'):
        super().__init__(parent)
        self._text_box.configure(state='disabled')
        self._text_box.configure(insertofftime=500, insertontime=500)

    def append(self, text: str):
        super().append(text)
        self._text_box.configure(state='disabled')

    def log(self, text: str):
        self.append(text)
        self.append('\n')
        self._text_box.see(END)


class CommandWindow(TextWindow):
    def __init__(self, parent: 'GridFrame'):
        super().__init__(parent)
        self._text_box.configure(state='normal')

    def append(self, text: str):
        super().append(text)

    def get_command(self):
        return self._text_box.get('1.0', END)

    def bind_handler(self, key, handler):
        self._text_box.bind(key, handler)


class DescriptionWindow(TextWindow):
    def __init__(self, parent: 'GridFrame'):
        super().__init__(parent)
        self._text_box.configure(state='disabled')
        self.set_color('black', (100, 100, 100))

    def set_text(self, text: str):
        self._text_box.configure(state='normal')
        self._text_box.delete('1.0', END)
        self._text_box.insert(END, text)
        self._text_box.configure(state='disabled')
