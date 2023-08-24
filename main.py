# Copyright (C) 2022 NG:ITL
from camera_calibration.image_sources import VideoFileSource, CameraStreamSource, WebcamSource
from camera_calibration.camera_calibration import Calibrator
import json


def read_config(config_file_path: str) -> dict:
    with open(config_file_path, "r") as file:
        return json.load(file)


if __name__ == "__main__":
    config = read_config("camera_calibration_config.json")
    # source = CameraStreamSource(config["pynng"]["subscribers"]["__sub_frame"]["address"])
    source = WebcamSource()
    calibrator = Calibrator(source, config["chessboard"]["chessboard_size"], config["chessboard"]["square_size"])
    calibrator.main()
