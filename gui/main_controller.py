import os
from tkinter import filedialog
from gui.menubar import Menubar
from gui.grid_frame import GridFrame
from gui.text_window import CommandWindow, LogWindow
from gui.photo_manager import PhotoManager
from gui.workstation import Workstation
from gui.workstation_controller import WorkstationController


class MainController:
    def __init__(self, root_gf: GridFrame, menubar: Menubar):
        self._root_gf = root_gf
        self._root = root_gf.parent
        self._menubar = menubar

        self._ws_controllers = []
        self._attach_grid_frame(root_gf)
        self._attach_menubar(menubar)
        self._bind_handlers()
        self._clear_log()
        self.log("Initialized")

    def _attach_menubar(self, menubar: Menubar):
        menubar.add_command('Open', self._browse_folder_menubar)

    def _attach_grid_frame(self, gf: GridFrame):
        for child in gf.get_children():
            self.log("attaching : " + child.__class__.__name__)
            if isinstance(child, GridFrame):
                pass
            elif isinstance(child, LogWindow):
                self._attach_log_window(child)
            elif isinstance(child, CommandWindow):
                self._attach_command_window(child)
            elif isinstance(child, PhotoManager):
                self._attach_photo_manager(child)
            elif isinstance(child, Workstation):
                self._attach_photo_workstation(child)
        for frame in gf.get_children_frames():
            self._attach_grid_frame(frame)

    def _attach_photo_workstation(self, photo_workstation: Workstation):
        controller = WorkstationController(photo_workstation, self.log)
        self._ws_controllers.append(controller)

    def _attach_photo_manager(self, photo_manager: PhotoManager):
        assert not hasattr(self, '_photo_manager'), "photo manager already attached"
        self._photo_manager = photo_manager
        self._set_photo_folder()

    def _attach_log_window(self, log_window: LogWindow):
        assert not hasattr(self, '_log_window'), "log window already attached"
        self._log_window = log_window

    def _attach_command_window(self, command_window: CommandWindow):
        assert not hasattr(self, '_command_window'), "command window already attached"
        self._command_window = command_window

    def _bind_handlers(self):
        self._photo_manager.bind_handler('<Escape>', self._root.quit())
        self._command_window.bind_handler('<Return>', self._run_command)
        self._photo_manager.bind_handler('<Double-Button-1>', self._display_image)
        self._photo_manager.bind_handler('<Up>', self._ws_controllers[0].move_image)
        self._photo_manager.bind_handler('<Down>', self._ws_controllers[0].move_image)
        self._photo_manager.bind_handler('<Left>', self._ws_controllers[0].move_image)
        self._photo_manager.bind_handler('<Right>', self._ws_controllers[0].move_image)

    def log(self, text: str):
        if hasattr(self, '_log_window'):
            self._log_window.log(text)
        else:
            print(text)

    def _clear_log(self):
        assert hasattr(self, '_log_window'), "log window not attached"
        self._log_window.clear()

    def _browse_folder_menubar(self):
        folder_path = filedialog.askdirectory(title="Select image folder")
        if not os.path.isdir(folder_path):
            self.log("invalid folder path: " + folder_path)
            return
        self._set_photo_folder(folder_path)
        self.log("open folder: " + folder_path)

    def _set_photo_folder(self, folder_path: str = None):
        self._photo_manager.set_folder(folder_path)
        num_item = self._photo_manager.get_item_count()
        path_opened = self._photo_manager.get_image_folder_path()
        self.log("open folder: " + path_opened + "\n with " + str(num_item) + " images")

    def _display_image(self, event):
        assert hasattr(self, '_photo_manager'), "photo manager not attached"
        assert len(self._ws_controllers) > 0, "photo workstation not attached"
        path = self._photo_manager.get_selected_image_path()
        self._ws_controllers[0].set_image(path)
        image_name = self._photo_manager.get_selected_image_filename()
        self.log("display image: " + image_name)

    def _run_command(self, event):
        assert hasattr(self, '_command_window'), "command window not attached"
        command = self._command_window.get_command()
        command = command.strip()
        if len(command) == 0:
            return
        self.log('user command: ' + command)
        commands = command.split(' ')
        first_token = commands[0]
        later_commands = ' '.join(commands[1:])
        if first_token == 'ws':
            self._ws_controllers[0].run_command(later_commands)
        else:
            self._run_misc_command(command)

    def _run_misc_command(self, command: str):
        if command == 'clear':
            self._clear_log()
