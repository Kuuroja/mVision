import pandas as pd
import cv2
import imutils
from modules.detectcolors import DetectColors
from modules.libraryWriter import addColor
from modules.camera import Grab

# Simplified calibration process for mVision project
def Calibration(camera):
    print("Calibration started")
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv('modules/colorLibrary.csv', names=index, header=None)
    referenceData = []
    for i in range(len(csv)):
        # Get color names to a array
        color = csv.loc[i, "color_name"]
        referenceData.append(color)

    print(referenceData)
    # Clear data from the library file
    f = open('modules/colorLibrary.csv', "w+")
    f.close()

    # Measure and add new color values one by one
    for i in range(len(referenceData)):
        k = 0
        while k != 13:
            image = Grab(camera, 1)
            cv2.rectangle(image,(975,555),(1025,605), (255,0,255),2,1)
            reference = imutils.resize(image,900)
            reference = cv2.putText(reference,referenceData[i],(200,200),
                                    cv2.FONT_HERSHEY_SIMPLEX,4,(255,0,255),2,1)
            cv2.imshow("image", reference)
            k = cv2.waitKey(0)

        cv2.destroyAllWindows()
        # Get rgb value from target area
        data = DetectColors(image, 1000,580, True)
        rgb = data[1]
        # Add color with the measured rgb value to the library file
        addColor(referenceData[i], rgb)

    cv2.destroyAllWindows()

def getWB(camera):
    camera.Open()
    camera.BalanceRatioSelector.SetValue("Red")
    wb_r = camera.BalanceRatioAbs.GetValue()
    camera.BalanceRatioSelector.SetValue("Green")
    wb_g = camera.BalanceRatioAbs.GetValue()
    camera.BalanceRatioSelector.SetValue("Blue")
    wb_b = camera.BalanceRatioAbs.GetValue()
    camera.Close()
    print(wb_r,wb_g,wb_b)
    return [wb_r,wb_g,wb_b]

def setWB(camera, values = False, wb = [1.89, 1, 2.14]):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)

    while True:
        img = Grab(camera, 1)
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        cv2.imshow("image", img)
        k = cv2.waitKey(0)
        if k == 13:
            break

    cv2.destroyAllWindows()
    print("set wb")
    wb_r = wb[0]
    wb_g = wb[1]
    wb_b = wb[2]
    # If manual values are give use them
    if values:
        camera.Open()
        wb = "Off"
        camera.BalanceWhiteAuto.SetValue(wb)
        camera.BalanceRatioSelector.SetValue("Red")
        camera.BalanceRatioAbs.SetValue(wb_r)
        camera.BalanceRatioSelector.SetValue("Green")
        camera.BalanceRatioAbs.GetValue(wb_g)
        camera.BalanceRatioSelector.SetValue("Blue")
        camera.BalanceRatioAbs.GetValue(wb_b)
        camera.Close()
    # Automtically determine wb
    else:
        camera.Open()
        wb = "Once"
        camera.BalanceWhiteAuto.SetValue(wb)
        wb = "Off"
        camera.BalanceWhiteAuto.SetValue(wb)
        camera.Close()