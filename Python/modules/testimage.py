# Import packages
import cv2
from cv2 import _InputArray_STD_BOOL_VECTOR
import numpy as np
import imutils
from modules.detectcolors import DetectColors, GetRef
from scipy.spatial import distance as dist
from datetime import datetime

# Setup
maxTries = 3

# Main fuction for taking measurements from image
def TestImage(frame, tries = maxTries):
    # Save captured image as "image_ + "time of capture".png
    # If statement so that the image is saved only once even 
    # if there is multiple tries to find circles
    if tries == maxTries:
        dTime = datetime.now()
        # File name format # Get current date and time
        dTime = dTime.strftime("%Y%m%d%H%M%S")
        imageName = str(dTime) + '.png'
        saved = cv2.imwrite('images/' + imageName, frame)
        print("Image saved: ", saved)
    # Load the image, convert it to grayscale
    image = imutils.resize(frame, 900)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect circles in the image / Find the "bolt" or the "bolt hole"
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, minDist = 300,
                                minRadius = 50, maxRadius = 100)
    # Ensure at least some circles were found
    if circles is not None:
        # Convert the (x, y) coordinates and radius of
        # the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # Loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # Check the distance between reference point in the carrier 
            # and the central circle of the block
            inPlace = getDistance(image, [x,y])
        
        if not inPlace:
            return "errPos"
        print("Position correct: ", inPlace)
        # Rectangle setup
        # Distance between the circle center and rectangles
        spacing = 150
        # Size of the rectangles
        offsetB = 20
        # create string that contains all color data
        # from three detection zones
        print("Measuring color data")
        colordata = ""
        colordata = colordata + "Box: " + DetectColors(image,
                                            x - spacing - offsetB, y) + " "
        colordata = colordata + "Lid: " + DetectColors(image,
                                            x, y - spacing) + " "
        boltcolor = DetectColors(image, x, y - 20)
        # Change white value to "Metal" for bolt color
        if(boltcolor == "White"):
            colordata = colordata + "Bolt: " + "Metal"
        else:
            colordata = colordata + "Bolt: " + boltcolor

        return colordata

    # If circle is not found try again for maxTries
    else:
        if tries <= maxTries:
            print("part not found")
            error = "errPos"
            return error
        else:
            tries -= 1
            TestImage(frame, tries)

# Get distance from reference point to bolt location
def getDistance(frame, circle):
    # Get reference points
    keypoints = GetRef(frame)
    xmin = 5000
    ymin = 5000
    # Find left most point from keypoints
    for i in range(len(keypoints)):
        x = keypoints[i].pt[0]
        y = keypoints[i].pt[1]

        if x < xmin:
            xmin = x
            ymin = y
    # Get distance between points
    D = dist.euclidean((xmin, ymin), (circle[0], circle[1]))

    # Error tresholds
    if D < 290 or D > 330:
        # Draw line for visual inspection
        cv2.line(frame, (int(xmin), int(ymin)), (int(circle[0]),
                    int(circle[1])), (0,0,255), 2)
        result = False
    else:
        cv2.line(frame, (int(xmin), int(ymin)), (int(circle[0]),
                    int(circle[1])), (0,255,0), 2)
        result = True

    cv2.putText(frame, "{:.1f}".format(D), (int(xmin), int(ymin - 50)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,0,255), 2)

    return result