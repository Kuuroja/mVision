from pypylon import pylon
import cv2

# Initial setup for Basler camera
def getCamera(wb = True):
    # conecting to the first available camera
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

    # Open camera for adjustments
    camera.Open()

    # Camera base settings
    camera.AcquisitionFrameRateAbs.SetValue(100)
    camera.GammaEnable.SetValue(True)

    # Gain, Blacklevel and pixel format
    camera.GainRaw.SetValue(0)
    camera.BlackLevelRaw.SetValue(0)
    camera.DigitalShift.SetValue(0)
    # Options: BayerRG12, YUV422Packed, YUV422_YUYV_Packed, Mono8, default: BayerRG8
    camera.PixelFormat.SetValue("BayerRG12")
    
    # Frame options
    camera.Width.SetValue(1920)
    camera.Height.SetValue(1200)
    camera.OffsetX.SetValue(8)
    camera.OffsetY.SetValue(8)

    # Exposure time of the camera in microseconds: 0.000001s or 1/1000000s
    camera.ExposureTimeAbs.SetValue(3000)

    #Set white balance automatically
    if wb is True:
        wbValue = "Off"
        camera.BalanceWhiteAuto.SetValue(wbValue)
        if wbValue == "Off":
            # White balance values
            camera.BalanceRatioSelector.SetValue("Red")
            camera.BalanceRatioAbs.SetValue(1.890625)
            wb_r = camera.BalanceRatioAbs.GetValue()
            camera.BalanceRatioSelector.SetValue("Green")
            camera.BalanceRatioAbs.SetValue(1)
            wb_g = camera.BalanceRatioAbs.GetValue()
            camera.BalanceRatioSelector.SetValue("Blue")
            camera.BalanceRatioAbs.SetValue(2.140625)
            wb_b = camera.BalanceRatioAbs.GetValue()
            # Good base values: R: 1.890625, G: 1.0, B: 2.140625

    camera.Close()
    return camera

# Function for capturing images with camera
def Grab(camera, imagesToGrab):
    grabbed = 0
    converter = pylon.ImageFormatConverter()

    # Converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    # Grabing Continusely (video) with minimal delay
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    # Grab loop with conversion and closing with esc
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
            # cv2.namedWindow('title', cv2.WINDOW_NORMAL)
            # cv2.imshow('title', img)
            cv2.waitKey(1)
            if grabbed == imagesToGrab:
                # Release resources and return image once imagesToGrab             
                camera.StopGrabbing()
                return img

        grabResult.Release()
        grabbed = grabbed + 1
 
    # Releasing the resource    
    camera.StopGrabbing()
    cv2.destroyAllWindows()