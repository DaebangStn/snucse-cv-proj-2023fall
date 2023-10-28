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
        self._clear()
        self._state = self.State.IMAGE_LOADED

    def _bind_handlers(self):
        self._ws.bind_handler('<Button-1>', self._manual_select)
        self._ws.bind_handler('<Button-3>', self._select_among_detected)
        self._ws.bind_handler('<MouseWheel>', self._zoom)

    def _manual_select(self, event):
        if self._state is not self.State.IMAGE_LOADED:
            self._log("no image loaded")
            return
        selected_coordinate = self._ws.get_original_coordinate(event.x, event.y)
        self._selected_points.append(selected_coordinate)
        self._ws.plot_point([selected_coordinate])
        self._log("manual selection: " + str(self._selected_points[-1]))

    def _select_among_detected(self, event):
        if self._state is not self.State.IMAGE_LOADED:
            self._log("no image loaded")
            return
        if len(self._detected_points) == 0:
            self._log("no detected point")
            return
        manually_selected_coordinate = self._ws.get_original_coordinate(event.x, event.y)
        min_distance = 100000000
        min_index = -1
        for i, point in enumerate(self._detected_points):
            distance = (point[0] - manually_selected_coordinate[0]) ** 2 + (
                    point[1] - manually_selected_coordinate[1]) ** 2
            if distance < min_distance:
                min_distance = distance
                min_index = i
        self._selected_points.append(self._detected_points[min_index])
        self._ws.plot_point([self._detected_points[min_index]], color='green', size=2)
        self._log("magnet selection: " + str(self._selected_points[-1]))

    def _plot_detected(self, command):
        if self._state is not self.State.IMAGE_LOADED:
            self._log("no image loaded")
            return
        self._log(f"plotting {len(self._detected_points)} points")
        self._ws.plot_point(self._detected_points, color='blue', size=2)

    def _clear(self):
        self._log("clear workstation")
        self._selected_points = []
        self._detected_points = []
        self._detected_lines = []
        self._ws.reload()

    def _zoom(self, event):
        delta = event.delta
        factor = 1.001 ** delta
        self._ws.zoom(factor)

    def move_image(self, event):
        x, y = 0, 0
        if event.keysym == 'Up':
            x, y = 0, -10
        elif event.keysym == 'Down':
            x, y = 0, 10
        elif event.keysym == 'Left':
            x, y = -10, 0
        elif event.keysym == 'Right':
            x, y = 10, 0
        self._ws.move_image(x, y)

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
        self._log("[detector] " + command)

        commands = command.split(' ')
        name = commands[0]
        kwargs = ' '.join(commands[1:])
        detector = detectors[name](self._ws.original_image)

        if detector.get_type() == FeatureType.POINT:
            points = detector.detect()
            self._detected_points.extend(points)
            self._log(f"detected points count: {len(points)}")
        elif detector.get_type() == FeatureType.LINE:
            lines = detector.detect()
            self._detected_lines.extend(lines)
            self._log(f"detected lines count: {len(lines)}")
