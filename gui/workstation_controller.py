from enum import IntEnum, auto
from gui.workstation import Workstation
from detector import detectors
from detector.base_detector import FeatureType


class WorkstationController:
    class State(IntEnum):
        NO_IMAGE = auto()
        IMAGE_LOADED = auto()
        ERROR = auto()

    def __init__(self, ws: Workstation, main_controller_log):
        self._ws = ws
        self._log = main_controller_log
        self._selected_points = []
        self._detected_points = []
        self._detected_lines = []
        self._bind_handlers()
        self._state = self.State.NO_IMAGE

    def set_image(self, path: str):
        self._ws.set_image(path)
        self._state = self.State.IMAGE_LOADED

    def _bind_handlers(self):
        self._ws.bind_handler('<Button-1>', self._manual_select)

    def _manual_select(self, event):
        if self._state is not self.State.IMAGE_LOADED:
            self._log("no image loaded")
            return
        self._selected_points.append((event.x, event.y))
        self._ws.plot_point(event.x, event.y)
        self._log("manual selection: " + str(self._selected_points[-1]))

    def _plot_detected(self, command):
        if self._state is not self.State.IMAGE_LOADED:
            self._log("no image loaded")
            return
        self._log(f"plotting {len(self._detected_points)} points")
        for point in self._detected_points:
            self._ws.plot_point(point[1], point[0], color='blue', size=2)

    def _clear(self):
        self._log("clear workstation")
        self._selected_points = []
        self._detected_points = []
        self._detected_lines = []
        self._ws.reload()

    def run_command(self, command: str):
        command = command.strip()
        if len(command) == 0:
            return
        commands = command.split(' ')
        first_token = commands[0]
        later_commands = ' '.join(commands[1:])
        if first_token == 'detect':
            self._run_detector(later_commands)
        elif first_token == 'plot':
            self._plot_detected(later_commands)
        elif first_token == 'clear':
            self._clear()

    def _run_detector(self, command):
        if self._state is not self.State.IMAGE_LOADED:
            self._log("no image loaded")
            return
        self._log("run feature detector: " + command)

        commands = command.split(' ')
        name = commands[0]
        kwargs = ' '.join(commands[1:])
        detector = detectors[name](self._ws.imgPIL)

        if detector.get_type() == FeatureType.POINT:
            points = detector.detect()
            self._detected_points.extend(points)
            self._log(f"detected points count: {len(points)}")
        elif detector.get_type() == FeatureType.LINE:
            lines = detector.detect()
            self._detected_lines.extend(lines)
            self._log(f"detected lines count: {len(lines)}")
