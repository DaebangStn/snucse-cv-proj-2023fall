import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_agg import FigureCanvasAgg


class CameraView:
  
    def __init__(self, coords, Ts, Rs):
        self._max_values = [max(col) for col in zip(*coords)]
        self._min_values = [min(col) for col in zip(*coords)]
        self._Ts = Ts
        self._Rs = Rs


    def plot_camera_pyramid(self, ax, pyramid_size=1.0):
        for T, R in zip(self._Ts, self._Rs):
            T = T[:3] / T[3]
            position = (T.T)[0]
            rotation_matrix = R
        
            forward_vector = rotation_matrix[:, 2]
            up_vector = rotation_matrix[:, 1]
            right_vector = rotation_matrix[:, 0]

            apex = np.array(position)

            base_vertices = [
                apex - pyramid_size * (forward_vector + right_vector),
                apex - pyramid_size * (forward_vector - right_vector),
                apex + pyramid_size * (forward_vector + right_vector),
                apex + pyramid_size * (forward_vector - right_vector)
            ]

            pyramid_faces = [
                [base_vertices[0], base_vertices[1], base_vertices[2]],
                [base_vertices[0], base_vertices[2], base_vertices[3]],
                [apex, base_vertices[0], base_vertices[1]],
                [apex, base_vertices[1], base_vertices[3]],
                [apex, base_vertices[3], base_vertices[2]],
                [apex, base_vertices[2], base_vertices[0]]
            ]

            ax.add_collection3d(Poly3DCollection(pyramid_faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=0.5))

    def generate_cuboid_coordinates(self):
        max_values = self._max_values
        min_values = self._min_values
        coordinates = [
            [[min_values[0], min_values[1], min_values[2]], [max_values[0], min_values[1], min_values[2]], [max_values[0], max_values[1], min_values[2]], [min_values[0], max_values[1], min_values[2]]],
            [[min_values[0], min_values[1], max_values[2]], [max_values[0], min_values[1], max_values[2]], [max_values[0], max_values[1], max_values[2]], [min_values[0], max_values[1], max_values[2]]],
            [[min_values[0], min_values[1], min_values[2]], [min_values[0], min_values[1], max_values[2]], [min_values[0], max_values[1], max_values[2]], [min_values[0], max_values[1], min_values[2]]],
            [[max_values[0], min_values[1], min_values[2]], [max_values[0], min_values[1], max_values[2]], [max_values[0], max_values[1], max_values[2]], [max_values[0], max_values[1], min_values[2]]],
            [[min_values[0], min_values[1], min_values[2]], [max_values[0], min_values[1], min_values[2]], [max_values[0], min_values[1], max_values[2]], [min_values[0], min_values[1], max_values[2]]],
            [[min_values[0], max_values[1], min_values[2]], [max_values[0], max_values[1], min_values[2]], [max_values[0], max_values[1], max_values[2]], [min_values[0], max_values[1], max_values[2]]]
        ]
        return coordinates

    def plot_cuboid(self, ax):
        coordinates = self.generate_cuboid_coordinates()
        for coord in coordinates:
            poly3d = [[tuple(coord[0]), tuple(coord[1]), tuple(coord[2]), tuple(coord[3])]]
            ax.add_collection3d(Poly3DCollection(poly3d, facecolors='yellow', linewidths=1, edgecolors='r', alpha=0.5))


    def get_view(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        Ts = self._Ts
        max_val = 0
        for T in Ts:
            T = T[:3] / T[3]
            tmax = np.max(np.abs(T))
            max_val = max(max_val, tmax)
        max_val *= 1.1
        
        ax.set_xlim([-max_val, max_val])
        ax.set_ylim([-max_val, max_val])
        ax.set_zlim([0, max_val])
        ax.set_box_aspect([2,2,1])
        self.plot_cuboid(ax)
        self.plot_camera_pyramid(ax, max_val / 10)
        # self.plot_cameras(ax)
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        result = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
        return result