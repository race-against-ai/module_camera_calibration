# Copyright (C) 2022 NG:ITL
from camera_calibration.image_sources import VideoFileSource, CameraStreamSource, WebcamSource
from camera_calibration.camera_calibration import Calibrator

# Constants
address_rec_frame = "ipc:///tmp/RAAI/camera_frame.ipc"

if __name__ == "__main__":
    # source = CameraStreamSource(FRAME_RECEIVE_LINK)
    source = WebcamSource()
    calibrator = Calibrator(source, (5, 5))
    calibrator.main()
