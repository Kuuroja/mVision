 # Import packages
import cv2
import pandas as pd
import numpy as np
from math import sqrt
from modules.camera import Grab
from modules.libraryWriter import addColor

# Function for adding colors to library
def addDetected(camera, name):
    print("adding color...")
    img = Grab(camera, 1)
    color = DetectColors(img, 1000, 580, True)
    rgb = color[1]
    addColor(name, rgb)

# Get reference points from image # Black points with white background
# This is used to detect the reference point in the carrier
def GetRef(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    # Setup SimpleBlobDetector parameters -------------------
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 150
    params.maxThreshold = 255

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 30

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.7

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.8

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.6
    # End of parameters -------------------------------------

    # Create blob detector and get points
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(gray)

    return(keypoints)

# Main detect colors function that measures color from area
# and returns closest color from the database
def DetectColors(frame, x, y, calibration=False, area = 30):
    r = g = b = 0

    # Setup the database (csv file)
    index = ["color", "color_name", "hex", "R", "G", "B"]
    # Calibration needs separate color library because the colorLibrary 
    # file will be cleared during the calibration
    if calibration is True:
        csv = pd.read_csv('modules/colorChecker.csv',
                        names=index, header=None)
    else:
        csv = pd.read_csv('modules/colorLibrary.csv',
                            names=index, header=None)

    # Calculate distance from measured colors to closests color in database
    # Old version
    def RecognizeColor(r, g, b,):
        color_d = []
        # Search every color in csv file
        for i in range(len(csv)):
            # Get values from csv file
            cr = int(csv.loc[i, "R"])
            cg = int(csv.loc[i, "G"])
            cb = int(csv.loc[i, "B"])
            hexa = csv.loc[i,"hex"]
            color = csv.loc[i, "color_name"]
            # Euclidian distance calculation for 3 dimensional space
            # Calculates straight line distance between points
            distance = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
            # Add to array
            color_d.append((distance, color, hexa))

        # Plot(r,g,b,min(color_d)[2])
        # Return color name with smallest difference in values
        return [min(color_d)[1], min(color_d)[2]]

    # Get avarage color value from targeted area in frame
    tArea = frame[y:y+area, x:x+area]
    r_list = []
    g_list = []
    b_list = []
    
    # Store values in arrays
    for n, dim in enumerate(tArea):
        for num, row in enumerate(dim):
            b, g, r = row
            r_list.append(r)
            g_list.append(g)
            b_list.append(b)
    
    # Average values
    r_avg = np.average(r_list)
    g_avg = np.average(g_list)
    b_avg = np.average(b_list)

    # Convert to int and set color values
    b = int(b_avg)
    g = int(g_avg)
    r = int(r_avg)
    
    # Get closest match from database
    data = RecognizeColor(r, g, b)
    colorName = data[0]
    rgb = [r,g,b]

    testData = RecognizeColor(r, g, b)
    hexa = testData[1]
    calibData = testData[0]
    calib = [calibData, rgb, hexa]
    # if calibration is active return color values with the name
    # else return only the name of the color
    if calibration is True:
        return calib
    else:
        return colorName