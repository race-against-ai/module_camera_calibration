# Copyright (C) 2023, NG:ITL
from camera_calibration.camera_calibration import Calibrator
from mocks.virtual_camera import VirtualCamera
from pathlib import Path
import json
import numpy as np
from json import load
from typing import Any
import unittest

# Constants
CURRENT_DIR = Path(__file__).parent


# Reminder: Naming convention for unit tests
#
# test_InitialState_PerformedAction_ExpectedResult
def read_config(config_file_path: Path) -> dict:
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

    def test_Calibration_CreateMatrix_CorrectMatrixFile(self) -> None:
        config = read_config(self.__config_path)
        source = VirtualCamera(2)
        # source = WebcamSource()
        calibrator = Calibrator(
            source, config["chessboard"]["chessboard_size"], config["chessboard"]["square_size"], True
        )
        calibrator.main()

        matrix = np.loadtxt(str(CURRENT_DIR.parent / "matrix.csv"), delimiter=",")
        matrix_correct = np.loadtxt(str(CURRENT_DIR / "matrix_correct.csv"), delimiter=",")
        matrix_correct2 = np.loadtxt(str(CURRENT_DIR / "matrix_correct2.csv"), delimiter=",")
        print("Matrix loaded, comparing...")
        print(matrix)
        print(matrix_correct)
        if (matrix == matrix_correct).all() or (matrix == matrix_correct2).all():
            print("yes")
            self.assertTrue(True)
        else:
            print("nono")
            self.assertTrue(False)
