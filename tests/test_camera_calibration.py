# Copyright (C) 2023, NG:ITL
from camera_calibration.camera_calibration import Calibrator
from mocks.virtual_camera import VirtualCamera
from pathlib import Path
import json
import cv2
import numpy as np
from pynng import Sub0
from json import load, loads, dump
from typing import Any
import unittest

# Constants
CURRENT_DIR = Path(__file__).parent


# Reminder: Naming convention for unit tests
#
# test_InitialState_PerformedAction_ExpectedResult
def read_config(config_file_path: str) -> dict:
    with open(config_file_path, "r") as file:
        return json.load(file)


class CameraCalibrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__config_path = CURRENT_DIR.parent / "camera_calibration_config.json"
        self.__config: dict[str, Any]
        with open(self.__config_path, "r") as config_file:
            self.__config = load(config_file)

    def tearDown(self) -> None:
        pass

    def test_Calibration_CreateMatrix_MatrixFile(self) -> None:

        config = read_config("../camera_calibration_config.json")
        source = VirtualCamera(1/3)
        # source = WebcamSource()
        calibrator = Calibrator(source, config["chessboard"]["chessboard_size"],
                                config["chessboard"]["square_size"], True)
        calibrator.main()

        matrix = np.loadtxt("matrix.csv", delimiter=",")
        matrix_correct = np.loadtxt("matrix_correct.csv", delimiter=",")
        print("Matrix loaded, comparing...")
        print(matrix)
        print(matrix_correct)
        if (matrix == matrix_correct).all():
            print("yes")
            self.assertTrue(True)
        else:
            print("nono")
            self.assertTrue(False)


if __name__ == "__main__":
    calib = CameraCalibrationTest()
    calib.test_Calibration_CreateMatrix_MatrixFile()
