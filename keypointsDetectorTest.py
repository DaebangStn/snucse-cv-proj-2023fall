import os
import cv2
import numpy as np
from glob import glob
from matplotlib import pyplot as plt


img_dir = './img'


def harris_corner(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dst = cv2.cornerHarris(gray, 5, 11, 0.04)
    dst = cv2.dilate(dst, None)
    harris = img.copy()
    harris[dst > 0.001 * dst.max()] = [255, 0, 255]
    return harris


def hough_line(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 200)
    linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, None, 30, 10)
    hough = img.copy()
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(hough, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)
    return hough


def shi_tomasi(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
    corners = np.intp(corners)
    shi_tomasi = img.copy()
    for i in corners:
        x, y = i.ravel()
        cv2.circle(shi_tomasi, (x, y), 3, 255, -1)
    return shi_tomasi


def fast(img):
    fast = cv2.FastFeatureDetector_create()
    kp = fast.detect(img, None)
    fast = cv2.drawKeypoints(img, kp, None, color=(255, 0, 0))
    return fast


if __name__ == '__main__':
    for img_path in glob(img_dir + '/*'):
        if '_result' in img_path:
            print('remove', img_path)
            os.remove(img_path)

    for img_path in glob(img_dir + '/*'):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.figure()
        plt.subplot(2, 2, 1)
        plt.imshow(harris_corner(img))
        plt.title('Harris Corner')
        plt.axis('off')
        plt.subplot(2, 2, 2)
        plt.imshow(hough_line(img))
        plt.title('Hough Line')
        plt.axis('off')
        plt.subplot(2, 2, 3)
        plt.imshow(shi_tomasi(img))
        plt.title('Shi Tomasi')
        plt.axis('off')
        plt.subplot(2, 2, 4)
        plt.imshow(fast(img))
        plt.title('FAST')
        plt.axis('off')
        plt.savefig(img_path.split('/')[-1].split('.')[0] + '_result.jpg')
        plt.show()
