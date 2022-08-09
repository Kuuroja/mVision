# Import pakages
import cv2
from modules.testimage import TestImage
from modules.camera import Grab, getCamera
from _thread import *
from modules.ui import UI
# Test file for quick debugging and testing of smaller parts of the program
def Main():
    camera = getCamera()

    UI(camera)

    # k = cv2.waitKey(1)
    # while k != 27:
    #     img = Grab(camera, 1)
    #     data = TestImage(img, 3)
    #     print(data)
    #     k = cv2.waitKey(1)

if __name__ == "__main__":
    Main()
