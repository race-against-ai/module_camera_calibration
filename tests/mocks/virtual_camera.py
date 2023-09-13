# Copyright (C) 2023, NG:ITL
from time import sleep
import numpy as np
import cv2
import glob


# Class
class VirtualCamera:
    def __init__(self, frame_rate: float) -> None:
        """Create a virtual camera mimicking the behavior of a real camera.

        Args:
            The first object bottom, last object top.
            frame_rate (int): The frame_rate of the virtual camera.
        """
        self.frame_size: tuple[int, int, int] = (990, 1332, 3)
        self.__time_to_sleep = 1 / frame_rate
        print(self.__time_to_sleep)
        self.__images = glob.glob("./pictures/*.jpg")

        print(self.__images)

    def read_new_frame(self) -> np.ndarray:
        """Read a new frame from the camera.

        Returns:
            np.ndarray: The new frame.
        """
        sleep(self.__time_to_sleep)
        current = cv2.imread(self.__images.pop(0))
        return current


if __name__ == "__main__":
    cam = VirtualCamera(1 / 3)
    while True:
        frame = cam.read_new_frame()
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
