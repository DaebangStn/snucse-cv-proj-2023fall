import sys
import os
import numpy as np
from PIL import Image

class Mosaic:
    def __init__(self, Ims, Ks, Rs):
        self._Ims = Ims
        self._Ks = Ks
        self._Rs = Rs

    def output_shape(self, images, Hs):
        shape = None
        offset = None
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for i in range(len(images)):
            height, width = images[i].shape[:2]
            corners = np.array( \
                [[0, 0, 1], \
                [0, height, 1], \
                [width, 0, 1], \
                [width, height, 1]], dtype=np.float32).T
            warped_corners = np.dot(Hs[i], corners)
            warped_corners = warped_corners[:2] / warped_corners[2]
            
            min_x = min(min_x, np.min(warped_corners[0]))
            min_y = min(min_y, np.min(warped_corners[1]))
            max_x = max(max_x, np.max(warped_corners[0]))
            max_y = max(max_y, np.max(warped_corners[1]))
            
        output_width = int(np.ceil(max_x - min_x))
        output_height = int(np.ceil(max_y - min_y))
        offset_x = int(np.floor(min_x))
        offset_y = int(np.floor(min_y))

        shape = [output_height, output_width]
        offset = [offset_x, offset_y]
        return shape, offset

    def image_warp(self, image, H, output, offset):
        input_height, input_width = image.shape[:2]
        output_height, output_width = output.shape[:2]
        y, x = np.indices((output_height, output_width), dtype=np.float32)
        x_ref = x + offset[0]
        y_ref = y + offset[1]
        
        coords = np.vstack((x_ref.flatten(), y_ref.flatten(), np.ones_like(x_ref.flatten())))
        inverse_H = np.linalg.inv(H)
        source_coords = np.dot(inverse_H, coords)
        source_coords = source_coords[:2] / source_coords[2]
        
        x_int, y_int = np.floor(source_coords).astype(int)
        x_frac, y_frac = source_coords - np.floor(source_coords)
        valid_mask = np.logical_and(np.logical_and(x_int >= 0, x_int < input_width - 1),
                                    np.logical_and(y_int >= 0, y_int < input_height - 1))
        
        y = y.flatten().astype(int)[valid_mask]
        x = x.flatten().astype(int)[valid_mask]
        y_int = y_int[valid_mask]
        x_int = x_int[valid_mask]
        y_frac = y_frac[valid_mask]
        x_frac = x_frac[valid_mask]
        
        output[y, x] = (1 - x_frac) * (1 - y_frac) * image[y_int, x_int] \
                    + x_frac * (1 - y_frac) * image[y_int, x_int + 1] \
                    + (1 - x_frac) * y_frac * image[y_int + 1, x_int] \
                    + x_frac * y_frac * image[y_int + 1, x_int + 1]
                    
        return output
    
    def run_mosaic(self):
        result = None

        input_images = []
        Hs = []
        N = len(self._Ims)
        
        for i in range(N):
            image = np.asarray(self._Ims[i])
            image = np.mean(image, axis=2)
            input_images.append(image)
            if i == 0:
                H = np.identity(n=3)
            else:
                K1 = self._Ks[0]
                R1 = self._Rs[0]
                K2 = self._Ks[i]
                R2 = self._Rs[i]
                K2_inv = np.linalg.inv(K2)
                H = K1 @ R1 @ R2.T @ K2_inv
            Hs.append(H)

        shape, offset = self.output_shape(input_images, Hs)
        output = np.zeros(shape)
        
        for i in range(N):
            output = self.image_warp(input_images[i], Hs[i], output, offset)
        result = output.astype(np.uint8)
        result = Image.fromarray(result)
        
        return result

