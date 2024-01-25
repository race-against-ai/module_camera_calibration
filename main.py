# Copyright (C) 2022 NG:ITL
from camera_calibration.image_sources import VideoFileSource, CameraStreamSource, WebcamSource
from camera_calibration.camera_calibration import Calibrator
import json
from pathlib import Path

FILE_DIR = Path(__file__).parent
BASE_DIR = FILE_DIR.parent
CONFIG_FILE_PATH = Path("./camera_calibration_config.json")


def read_config(config_file_path: str) -> dict:
    with open(config_file_path, "r") as file:
        return json.load(file)


if __name__ == "__main__":
    if not CONFIG_FILE_PATH.exists():
        with open(CONFIG_FILE_PATH, "w") as config_file, open(
            FILE_DIR / "templates/time_tracking_config.json", "r"
        ) as template_file:
            json.dump(json.load(template_file), config_file, indent=4)

    config = read_config("camera_calibration_config.json")
    source = CameraStreamSource(config["pynng"]["subscribers"]["__sub_frame"]["address"])
    calibrator = Calibrator(source, config["chessboard"]["chessboard_size"], config["chessboard"]["square_size"])
    calibrator.main()
