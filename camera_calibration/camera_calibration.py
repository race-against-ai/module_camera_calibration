# Copyright (C) 2022 NG:ITL

import cv2
import numpy as np
from threading import Timer
from camera_calibration.image_sources import VideoFileSource, CameraStreamSource, WebcamSource


def run_scheduled_task(p_time: int, scheduled_task, arg=None) -> None:
    """
    Args:
        p_time: time till the method will be executed in seconds
        scheduled_task: method that should be run
        arg: argument that should be passed to the method

    Returns:
        None
    """
    threading_timer = Timer(p_time, scheduled_task, [arg])
    threading_timer.start()


class Calibrator:
    def __init__(
        self, image_source: VideoFileSource | CameraStreamSource | WebcamSource, p_chessboard_size: tuple, p_size: int
    ):
        self.__ret, self.__matrix, self.__distortion, self.__r_vecs, self.__t_vecs = "", "", "", "", ""
        self.__gray_color = None
        self.__image_source = image_source
        self.__search = True
        self.__count = 0

        # Define the dimensions of chessboard
        self.__chessboard_size: tuple = p_chessboard_size
        self.__size = p_size

        # stop the iteration when specified accuracy, epsilon, is reached or specified number of iterations are
        # completed.
        self.__criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Vector for 3D points
        self.__three_d_points: list = []

        # Vector for 2D points
        self.__two_d_points: list = []

        #  3D points real world coordinates
        self.__object_p_3d = np.zeros((self.__chessboard_size[0] * self.__chessboard_size[1], 3), np.float32)
        j = 0
        for y in range(self.__chessboard_size[1]):
            for x in range(self.__chessboard_size[0]):
                self.__object_p_3d[j] = [self.__size * x, self.__size * y, 0]
                j += 1

        self.__object_p_3d[:, :2] = np.mgrid[0 : self.__chessboard_size[0], 0 : self.__chessboard_size[1]].T.reshape(
            -1, 2
        )

    def find_chessboard(self):
        while True:
            image = self.__image_source.read_new_frame()
            image_copy = image.copy()

            if self.__search:
                cv2.putText(image, "searching", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255, 255), 1)
                self.__gray_color = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Find the chess board corners
                # If desired number of corners are
                # found in the image then ret = true
                ret, corners = cv2.findChessboardCorners(
                    self.__gray_color,
                    self.__chessboard_size,
                    cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE,
                )

                # If desired number of corners can be detected then,
                # refine the pixel coordinates and display
                # them on the images of checkerboard
                if ret:
                    self.__count += 1
                    self.__three_d_points.append(self.__object_p_3d)

                    # Refining pixel coordinates
                    # for given 2d points.
                    corners2 = cv2.cornerSubPix(self.__gray_color, corners, (11, 11), (-1, -1), self.__criteria)

                    self.__two_d_points.append(corners2)

                    # Draw and display the corners
                    image = cv2.drawChessboardCorners(image_copy, self.__chessboard_size, corners2, ret)
                    cv2.imshow("imgcheck", image_copy)
                    self.__search = False
                    run_scheduled_task(2, self.set_search, True)
            else:
                cv2.putText(image, "waiting", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255, 255), 1)
            cv2.putText(
                image,
                f"recognised: {self.__count}",
                (image.shape[1] - 200, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 0, 255, 255),
                1,
            )
            cv2.imshow("img", image)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        print("creating matrix.csv...")
        cv2.destroyAllWindows()

    def create_matrix(self):
        self.__ret, self.__matrix, self.__distortion, self.__r_vecs, self.__t_vecs = cv2.calibrateCamera(
            self.__three_d_points, self.__two_d_points, self.__gray_color.shape[::-1], None, None
        )
        print(self.__distortion)

    def safe_output(self, p_name: str, p_data):
        np.savetxt(p_name, p_data, delimiter=",")
        print("done")

    def set_search(self, p_value: bool):
        self.__search = p_value

    def main(self):
        self.find_chessboard()
        self.create_matrix()
        self.safe_output("matrix.csv", self.__matrix)
        self.safe_output("distortion.csv", self.__distortion)
