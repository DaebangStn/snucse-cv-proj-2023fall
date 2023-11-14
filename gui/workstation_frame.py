from tkinter import ttk
from gui.workstation_controller import WorkstationController
from gui.workstation import Workstation


class WorkstationFrame:
    def __init__(self, parent: 'GridFrame'):
        self.parent = parent
        self.f = ttk.Frame(parent.f)
        self._next_ws_id = 0
        self._ws_ctrls = []
        self._ctrl_top = None
        self._logger = None
        self.f.columnconfigure(0, weight=1)
        self.f.rowconfigure(0, weight=1)

    def set_logger(self, _logger):
        self._logger = _logger

    def _log(self, text: str):
        if self._logger is not None:
            self._logger(text)
        else:
            print(text)

    def add_ws(self, image_path=None):
        if self._logger is None:
            raise Exception("logger is not set")
        ws = Workstation(self)
        idx = self._next_ws_id
        ws_ctrl = WorkstationController(ws, self._logger, idx)
        self._ws_ctrls.append(ws_ctrl)
        self._log(f"Workstation idx {idx} added")
        self._next_ws_id += 1
        if image_path is not None:
            ws_ctrl.set_image(image_path)
        return idx

    def unload_top_ws(self):
        if self._ctrl_top is not None:
            idx = self._ctrl_top.get_idx()
            self._ctrl_top.unload()
            self._ctrl_top = None
            self._log(f"Workstation {idx} unloaded")

    def load_ws(self, idx):
        ws = self.find_ws(idx)
        if ws is not None:
            self.unload_top_ws()
            self._ctrl_top = ws
            ws.load()
            self._log(f"Workstation {idx} loaded")
        else:
            self._log(f"Workstation {idx} not found")

    def find_ws(self, idx):
        for ws_ctrl in self._ws_ctrls:
            if ws_ctrl.get_idx() == idx:
                return ws_ctrl
        return None

    def delete_ws(self, idx):
        if self._ctrl_top is not None:
            if self._ctrl_top.get_idx() == idx:
                self.unload_top_ws()
        ws = self.find_ws(idx)
        if ws is not None:
            ws.unload()
            self._ws_ctrls.remove(ws)
            self._log(f"Workstation {idx} deleted")
        else:
            self._log(f"Workstation {idx} not found")

    def descriptions(self):
        description_list = []
        for ws_ctrl in self._ws_ctrls:
            description_list.append(ws_ctrl.description())
        if self._ctrl_top is None:
            return None, description_list
        else:
            return self._ctrl_top.get_idx(), description_list

    def get_ws_ctrl_indices(self):
        ret = []
        for ws_ctrl in self._ws_ctrls:
            ret.append(ws_ctrl.get_idx())
        return ret

    def move_image(self, event):
        if self._ctrl_top is not None:
            self._ctrl_top.move_image(event)

    def run_command(self, command):
        if self._ctrl_top is not None:
            self._ctrl_top.run_command(command)

    def get_indices(self):
        indices = []
        for ws_ctrl in self._ws_ctrls:
            indices.append(ws_ctrl.get_idx())
        return indices
