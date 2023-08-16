# Copyright (C) 2022 NG:ITL

import cv2
import numpy as np
import pynng
from camera_calibration.image_sources import VideoFileSource, CameraStreamSource, WebcamSource


class Calibrator:
    def __init__(self, image_source: VideoFileSource | CameraStreamSource | WebcamSource, p_chessboard_size: tuple):
        self.__gray_color = None
        self.__image_source = image_source

        # Define the dimensions of chessboard
        self.__chessboard_size: tuple = p_chessboard_size

        # stop the iteration when specified
        # accuracy, epsilon, is reached or
        # specified number of iterations are completed.
        self.__criteria = (cv2.TERM_CRITERIA_EPS +
                         cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Vector for 3D points
        self.__threedpoints = []

        # Vector for 2D points
        self.__twodpoints = []

        #  3D points real world coordinates
        self.__objectp3d = np.zeros((1, self.__chessboard_size[0]
                                   * self.__chessboard_size[1],
                                   3), np.float32)
        self.__objectp3d[0, :, :2] = np.mgrid[0:self.__chessboard_size[0],
                                   0:self.__chessboard_size[1]].T.reshape(-1, 2)

        self.__ret, self.__matrix, self.__distortion, self.__r_vecs, self.__t_vecs = "", "", "", "", ""

    def find_chessboard(self):
        while True:
            image = self.__image_source.read_new_frame()

            self.__gray_color = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            # If desired number of corners are
            # found in the image then ret = true
            ret, corners = cv2.findChessboardCorners(
                self.__gray_color, self.__chessboard_size,
                cv2.CALIB_CB_ADAPTIVE_THRESH
                + cv2.CALIB_CB_FAST_CHECK +
                cv2.CALIB_CB_NORMALIZE_IMAGE)
            print(ret)

            # If desired number of corners can be detected then,
            # refine the pixel coordinates and display
            # them on the images of checkerboard
            if ret:
                self.__threedpoints.append(self.__objectp3d)

                # Refining pixel coordinates
                # for given 2d points.
                corners2 = cv2.cornerSubPix(
                    self.__gray_color, corners, (11, 11), (-1, -1), self.__criteria)

                self.__twodpoints.append(corners2)

                # Draw and display the corners
                image = cv2.drawChessboardCorners(image,
                                                  self.__chessboard_size,
                                                  corners2, ret)
                cv2.imshow('imgcheck', image)
                print("jo")

            cv2.imshow('img', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        print("habs")
        cv2.destroyAllWindows()

    def create_matrix(self):
        self.__ret, self.__matrix, self.__distortion, self.__r_vecs, self.__t_vecs = cv2.calibrateCamera(
            self.__threedpoints, self.__twodpoints, self.__gray_color.shape[::-1], None, None)

    def safe_output(self, p_name: str,  p_data):
        np.savetxt(p_name, p_data, delimiter=",")
        print("ja")

    def main(self):
        self.find_chessboard()
        self.create_matrix()
        self.safe_output("matrix.csv", self.__matrix)
