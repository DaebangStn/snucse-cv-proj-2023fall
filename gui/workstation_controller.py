from typing import Tuple
from enum import IntEnum, auto
from gui.workstation import Workstation
from detector import detectors
from detector.base_detector import FeatureType


class WorkstationController:
    class State(IntEnum):
        NO_IMAGE = auto()
        ERROR = auto()
        MAGNET_POINT = auto()
        MAGNET_LINE = auto()

    def __init__(self, ws: Workstation, main_controller_log):
        self._ws = ws
        self._log = main_controller_log
        self._selected_points = []
        self._detected_points = []
        self._detected_lines = []
        self._considered_lines = []
        self._bind_handlers()
        self._state = self.State.NO_IMAGE

    def set_image(self, path: str):
        self._ws.set_image(path)
        self._clear()
        self._state = self.State.MAGNET_POINT

    def _bind_handlers(self):
        self._ws.bind_handler('<Button-1>', self._select_manual)
        self._ws.bind_handler('<Button-3>', self._select_among_detected)
        self._ws.bind_handler('<MouseWheel>', self._zoom)

    def _change_magent_mode(self, command):
        if self._state is self.State.NO_IMAGE:
            self._log("no image loaded")
            return
        if command == 'point' or command == 'p':
            self._state = self.State.MAGNET_POINT
            self._log("magnet mode: point")
        elif command == 'line' or command == 'l':
            self._state = self.State.MAGNET_LINE
            self._log("magnet mode: line")

    def _find_intersection(self, command):
        if self._state is self.State.NO_IMAGE:
            self._log("no image loaded")
            return
        if len(self._considered_lines) < 2:
            self._log("not enough lines")
            return
        intersections = []
        for i in range(len(self._considered_lines)):
            for j in range(i + 1, len(self._considered_lines)):
                line1 = self._considered_lines[i]
                line2 = self._considered_lines[j]
                flag, point = self._line_intersection(line1, line2)
                if flag:
                    intersections.append(point)
        self._selected_points.extend(intersections)
        self._ws.plot_point(intersections, color='red', size=5)
        self._log(f"intersection count: {len(intersections)}")

    def _select_manual(self, event):
        if self._state <= self.State.ERROR:
            self._log("no image loaded")
            return
        selected_coordinate = self._ws.get_original_coordinate(event.x, event.y)
        self._selected_points.append(selected_coordinate)
        self._ws.plot_point([selected_coordinate])
        self._log("manual selection: " + str(self._selected_points[-1]))

    def _select_among_detected(self, event):
        if self._state is self.State.NO_IMAGE:
            self._log("no image loaded")
            return
        manually_selected_coordinate = self._ws.get_original_coordinate(event.x, event.y)
        if self._state is self.State.MAGNET_POINT:
            self._select_point_among_detected(manually_selected_coordinate)
        elif self._state is self.State.MAGNET_LINE:
            self._select_line_among_detected(manually_selected_coordinate)
        else:
            raise Exception("invalid state")

    def _select_point_among_detected(self, selected_point):
        if len(self._detected_points) == 0:
            self._log("no detected point")
            return
        min_distance = 100000000
        min_index = -1
        for i, point in enumerate(self._detected_points):
            distance = (point[0] - selected_point[0]) ** 2 + (point[1] - selected_point[1]) ** 2
            if distance < min_distance:
                min_distance = distance
                min_index = i
        self._selected_points.append(self._detected_points[min_index])
        self._ws.plot_point([self._detected_points[min_index]], color='red', size=5)
        self._log("magnet point selection: " + str(self._selected_points[-1]))

    def _select_line_among_detected(self, selected_point):
        if len(self._detected_lines) == 0:
            self._log("no detected line")
            return
        min_distance = 100000000
        min_index = -1
        for i, line in enumerate(self._detected_lines):
            distance = self._distance_to_line(line, selected_point)
            if distance < min_distance and self._near_line_segment(line, selected_point):
                min_distance = distance
                min_index = i
        self._considered_lines.append(self._detected_lines[min_index])
        self._ws.plot_line([self._detected_lines[min_index]], color='green', width=2)
        self._log("magnet line selection: " + str(self._considered_lines[-1]))

    @staticmethod
    def _near_line_segment(line, point):
        x1, y1, x2, y2 = line
        inside_bb = WorkstationController._point_in_line_bb(line, point)
        line_length = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        distance = WorkstationController._distance_to_line(line, point)
        return inside_bb or distance < line_length * 0.3

    @staticmethod
    def _point_in_line_bb(line, point):
        x1, y1, x2, y2 = line
        x, y = point
        return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)

    @staticmethod
    def _distance_to_line(line, point):
        x1, y1, x2, y2 = line
        x, y = point
        if x1 == x2:
            return abs(x - x1)
        if y1 == y2:
            return abs(y - y1)
        a = (y2 - y1) / (x2 - x1)
        b = y1 - a * x1
        return abs(a * x - y + b) / (a ** 2 + 1) ** 0.5

    @staticmethod
    def _line_intersection(line1, line2) -> Tuple[bool, Tuple[int, int]]:
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2
        if x1 == x2:
            if x3 == x4:
                return False, (0, 0)
            a2 = (y4 - y3) / (x4 - x3)
            b2 = y3 - a2 * x3
            x = x1
            y = a2 * x + b2
        elif x3 == x4:
            a1 = (y2 - y1) / (x2 - x1)
            b1 = y1 - a1 * x1
            x = x3
            y = a1 * x + b1
        else:
            a1 = (y2 - y1) / (x2 - x1)
            b1 = y1 - a1 * x1
            a2 = (y4 - y3) / (x4 - x3)
            b2 = y3 - a2 * x3
            if a1 == a2:
                return False, (0, 0)
            x = (b2 - b1) / (a1 - a2)
            y = a1 * x + b1
        return True, (int(x), int(y))

    def _plot_points_and_lines(self, command):
        if self._state is self.State.NO_IMAGE:
            self._log("no image loaded")
            return
        self._ws.reload()
        self._ws.plot_line(self._detected_lines, color='blue', width=2)
        self._ws.plot_point(self._detected_points, color='blue', size=2)
        self._ws.plot_line(self._considered_lines, color='green', width=2)
        self._ws.plot_point(self._selected_points, color='red', size=5)

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
        if first_token == 'detect' or first_token == 'd':
            self._run_detector(later_commands)
        elif first_token == 'plot' or first_token == 'p':
            self._plot_points_and_lines(later_commands)
        elif first_token == 'clear' or first_token == 'c':
            self._clear()
        elif first_token == 'magnet' or first_token == 'm':
            self._change_magent_mode(later_commands)
        elif first_token == 'intersection' or first_token == 'i':
            self._find_intersection(later_commands)

    def _run_detector(self, command):
        if self._state is self.State.NO_IMAGE:
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
