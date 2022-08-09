# Import pakages
import time
import socket
import threading
from modules.testSubject import TestSubject
from _thread import *
from threading import Thread
from modules.testimage import TestImage
from modules.camera import getCamera
from modules.ui import UI
from modules.camera import Grab

# Setup
clients = set()
clients_lock = threading.Lock()
testData = None
bData = None

def RunTest():
    print("------------------- Testing started -------------------")
    camera = getCamera(wb = False)
    # Read the camera frames and modify them
    frame = Grab(camera, 1)
    # Get test data
    imagedetails = TestImage(frame)
    bData = str(imagedetails)

    return bData

def DataTranslator(data):
    # Translate data from number array to readable string format
    # Values are sensitive since they are directly compared to measured data that is generated by Testimage()
    dList = list((data))
    print(dList)
    # All data is in numeric form and are set in the IMS_6 PLC inside the function block 'FB_IMS6'
    # dList[0] data identifier '?' (key identifier that starts the camera process)
    # dList[1] bolt or no bolt (1 = bolt 0 = no bolt)
    # dList[2] bolt color (1 = metal 0 = red)
    # dList[3] box color (1 = white 0 = black)
    # dList[4] top color (1 = white 0 = black)
    output = ""
    if dList[3] == "1":
        output = "Box: White "
    else:
        output = "Box: Black "
    if dList[4] == "1":
        output = output + "Lid: White "
    else:
        output = output + "Lid: Black "
    if dList[1] == "1":
        if dList[2] == "1":
            output = output + "Bolt: Metal"
        else:
            output = output + "Bolt: Red"
    else:
        output = output + "Bolt: Missing"
    # Return values in a string
    return output

# TCP listener
def Listener(client, address, subject, cam):
    print("accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
    try:
        while True:
            print("listening...")
            time.sleep(1)
            # Data received from client
            data = client.recv(1024)
            data = data.decode('utf-8')
            # Set expected data leght to 5 if identifier "?" is not detected
            if "?" not in data:
                data = data[:5]

            if not data:
                print("Disconnected")
                break

            # Detect and save testData (data of what the measurements should be)
            if "?" in data:
                print("data received")
                if cam == False:
                    print("Running without camera")
                    result = True
                    result = str(result).encode()
                    client.sendall(result)
                else:
                    # Translate data to string
                    tData = DataTranslator(data)
                    with clients_lock:
                        # Save received data to testSubject class
                        subject.testData = tData
                    # Run tests and get data from camera
                    bData = RunTest()
                    if bData == "errPos":
                        data = str("Erpos").encode()
                        client.sendall(data)
                        print("Error: Part not found or in wrong position")
                        print("------------------- Testing finished -------------------")
                        break
                    else:
                        with clients_lock:
                            # Save measured data to testSubject class
                            subject.bData = bData

            print(subject.testData)
            print(subject.bData)
            # When comparison and measurement data are saved run comparison
            if subject.testData is not None and subject.bData is not None:
                # Compare results and save true or false
                if subject.testData == subject.bData:
                    result = True
                else:
                    result = False
                # send result to PLC
                print("Sending result: ", result)
                result_encoded = str(result).encode()
                client.sendall(result_encoded)
                time.sleep(1)
                subject.Reset()
                print("------------------- Testing finished -------------------")
                break

    finally:
        # Remove client form client list and close connection
        print("Closing connection")
        with clients_lock:
            clients.remove(client)
            client.close()

def Main():
    # Hosting address for tcp server
    port = 22000
    host = "192.168.2.148"

    # Get camera with calibrated values 
    # Argument False does not update white balance values 
    # if left blank or True WB values are updated to tested base values
    camera = getCamera(wb = False)

    # Start UI for start and calibration options
    cam = UI(camera)
        
    # Main program for communication
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print("socket binded to port: " + str(port))
    s.listen(3)
    th = []
    print("Waiting for connections...")
    # TestSubject class is used to save the expected data and the measured data for comparison.
    subject = TestSubject()
    while True:
        client, address = s.accept()
        # Open a new thread for the connection
        th.append(Thread(target=Listener, args=(client, address, subject, cam)).start())       
        time.sleep(5)

    s.close()

if __name__ == "__main__":
    Main()