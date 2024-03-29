import os
import re
import numpy as np
import cv2
from dataclasses import dataclass
from typing import List
from PIL import Image


@dataclass
class MosaicT:
    SIFT = 0,
    RGN = 1,  # random gaussian noise


class Mosaic:
    def __init__(self, images, _type: MosaicT):
        self._images = images
        self._type = _type

    def add_image(self, image: Image):
        self._images.append(image)

    def get_mosaic(self) -> Image:
        if self._type == MosaicT.SIFT or self._type == MosaicT.RGN:
            return self._get_mosaic()

    def _get_mosaic(self) -> Image:
        image = self._images[0]
        for i in range(1, len(self._images)):
            if self._type == MosaicT.SIFT:
                image = self._stitch_with_sift(image, self._images[i])
            elif self._type == MosaicT.RGN:
                image = self._stitch_with_rgn(image, self._images[i])

        if self._type == MosaicT.RGN:
            idx = self._get_lastest_index("img")
            image.save(f"img/rng_{idx + 1}.jpg")

        return image

    def _stitch_with_rgn(self, image1: Image, image2: Image) -> Image:
        image1 = np.array(image1)
        image2 = np.array(image2)
        image1_gray = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)

        # Find homography matrix
        homog, _ = self._get_homography_by_sift(image1_gray, image2_gray)

        # add random gaussian noise to the homography matrix
        homog = homog + np.random.normal(0, 0.0001, homog.shape)

        # Create a result canvas that fits both images
        out_shape, ofs = self._output_shape(image1, [image2], [homog])
        result_canvas = np.zeros(out_shape, dtype=np.uint8)

        # Place image2 on the canvas
        result_canvas[0:image1_gray.shape[0], 0:image1_gray.shape[1]] = image1

        # Warp image1 using the homography matrix and place it on the canvas
        warped_image2 = cv2.warpPerspective(image2, homog, (out_shape[1], out_shape[0]))

        # Create a mask to combine the images
        mask_warped = (warped_image2 > 0).astype(np.uint8) * 255

        # Now apply the bitwise_and operation using the 3-channel mask
        idx = (mask_warped != 0)
        result_canvas[idx] = warped_image2[idx]
        return Image.fromarray(result_canvas)

    def _stitch_with_sift(self, image1: Image, image2: Image) -> Image:
        image1 = np.array(image1)
        image2 = np.array(image2)
        image1_gray = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
        image2_gray = cv2.cvtColor(image2, cv2.COLOR_RGB2GRAY)

        # Find homography matrix
        homog, _ = self._get_homography_by_sift(image1_gray, image2_gray)

        # Create a result canvas that fits both images
        out_shape, ofs = self._output_shape(image1, [image2], [homog])
        result_canvas = np.zeros(out_shape, dtype=np.uint8)

        # Place image2 on the canvas
        result_canvas[0:image1_gray.shape[0], 0:image1_gray.shape[1]] = image1

        # Warp image1 using the homography matrix and place it on the canvas
        warped_image2 = cv2.warpPerspective(image2, homog, (out_shape[1], out_shape[0]))

        # Create a mask to combine the images
        mask_warped = (warped_image2 > 0).astype(np.uint8) * 255

        # Now apply the bitwise_and operation using the 3-channel mask
        idx = (mask_warped != 0)
        result_canvas[idx] = warped_image2[idx]
        return Image.fromarray(result_canvas)

    @staticmethod
    def _get_homography_by_sift(image1_gray: np.ndarray, image2_gray: np.ndarray):
        # Initialize SIFT detector
        sift = cv2.SIFT_create()

        # Detect and compute keypoints and descriptors
        k1, d1 = sift.detectAndCompute(image1_gray, None)
        k2, d2 = sift.detectAndCompute(image2_gray, None)

        # Initialize Brute Force Matcher with default params
        bf = cv2.BFMatcher()

        # Match descriptors and apply ratio test
        matches = bf.knnMatch(d1, d2, k=2)
        good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

        # Extract the matched keypoints
        src_pts = np.float32([k1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([k2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Find homography matrix
        homog, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)

        return homog, mask

    @staticmethod
    def _output_shape(image_ref, images, Hs):
        shape = None
        offset = None
        i_start, j_start = 0, 0
        i_end, j_end, channel = image_ref.shape
        for idx, H in enumerate(Hs):
            i, j, _ = images[idx].shape
            vertices = np.array([[0, 0], [i, 0], [0, j], [i, j]])
            vertices_p = np.concatenate([vertices, np.ones((4, 1))], axis=1)

            vertices_transformed = np.matmul(H, vertices_p.T).T
            vertices_transformed = vertices_transformed[:, :2]

            i_start = min(i_start, np.min(vertices_transformed[:, 0]))
            j_start = min(j_start, np.min(vertices_transformed[:, 1]))
            i_end = max(i_end, np.max(vertices_transformed[:, 0]))
            j_end = max(j_end, np.max(vertices_transformed[:, 1]))

        shape = (int(np.ceil(i_end - i_start)), int(np.ceil(j_end - j_start)), channel)
        offset = (-int(np.floor(i_start)), -int(np.floor(j_start)))
        return shape, offset

    @staticmethod
    def _get_lastest_index(dir_path: str) -> int:
        pattern = re.compile(f"rng_([0-9]+)\\.jpg")
        max_index = -1

        for filename in os.listdir(dir_path):
            match = pattern.match(filename)
            if match:
                index = int(match.group(1))
                max_index = max(max_index, index)

        return max_index
