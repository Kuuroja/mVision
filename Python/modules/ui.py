import tkinter as tk
from tkinter import messagebox
from tkinter import font
from modules.camera import Grab
from PIL import Image, ImageTk
from modules.detectcolors import addDetected
from modules.calibration import Calibration, getWB, setWB
from modules.libraryWriter import removeColor, getLibrary
import cv2

# UI setup
btnColor = '#ffffff'
windowColor = '#333333'
windowSize = "350x550"
fontColor = '#ffffff'
btnFontColor = '#333333'

# UI for mVision quality control module # library settings and calibration
def UI(camera):

    # Root window setup
    root = tk.Tk()
    root.wm_title("mVision")
    root.wm_protocol("WM_DELETE_WINDOW")
    # Set window size
    root.geometry(windowSize)
    # Set window color
    root.configure(bg= windowColor)
    # Set window icon
    # root.iconbitmap("modules/dot.ico")
    # Info label text
    info = "Setup and options for mVision quality control module \n\n"
    # Font setup
    uiFont = font.Font(size=10, weight='normal')

    # Buttons -------------------------------------------------------------------------
    closeBtn = tk.Button(root, text="Start", bg= btnColor, fg= btnFontColor, 
                                command = lambda: Close(root, True))
    closeBtn['font'] = uiFont
    closeBtn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

    noCamBtn = tk.Button(root, text="Start without camera", bg= btnColor, fg= btnFontColor, 
                                command = lambda: Close(root, False))
    noCamBtn['font'] = uiFont
    noCamBtn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

    calibBtn = tk.Button(root, text="Calibrate",bg= btnColor,fg= btnFontColor, 
                                command = lambda: goCalibration(camera))
    calibBtn['font'] = uiFont
    calibBtn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
 
    getWbBtn = tk.Button(root, text="Get White Balance",bg= btnColor,fg= btnFontColor, 
                                command = lambda: goGetWB(camera))
    getWbBtn['font'] = uiFont
    getWbBtn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

    setWbBtn = tk.Button(root, text="Set White Balance",bg= btnColor,fg= btnFontColor, 
                                command = lambda: goSetWB(camera))
    setWbBtn['font'] = uiFont
    setWbBtn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

    addBtn = tk.Button(root, text="Add color",bg= btnColor,fg= btnFontColor, 
                                command = lambda: goAddColor(camera, name_entry.get()))
    addBtn['font'] = uiFont
    addBtn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

    removeBtn = tk.Button(root, text="Remove color",bg= btnColor,fg= btnFontColor, 
                                command = lambda: goRemoveColor(name_entry.get()))
    removeBtn['font'] = uiFont
    removeBtn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

    getLibBtn = tk.Button(root, text="Color library",bg= btnColor,fg= btnFontColor, 
                                command = lambda: goGetLibrary())
    getLibBtn['font'] = uiFont
    getLibBtn.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
    # End of buttons -----------------------------------------------------------------

    # Name entry
    name_entry = tk.Entry(fg="black", bg="white", width=50)
    name_entry['font'] = uiFont
    name_entry.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

    # Labels
    label = tk.Label(text="Color name: ",bg=windowColor, fg = fontColor)
    label['font'] = uiFont
    label.pack(side = "bottom")

    infoLabel = tk.Label(text = info, bg=windowColor, fg = fontColor)
    infoLabel['font'] = uiFont
    infoLabel.pack(side = "bottom")

    # Start the main loop of the UI system
    root.mainloop()

# When window is closed
def Close(root, cam):
    root.destroy()
    return cam

# Button functions ----------------------------------------------------------------------------------------------------
# Button function for calibration
def goCalibration(camera):
    # Ask if user is sure
    msg = '''Calibration will permanently change expected color values and cannot be canceled! Do you wish to continue?'''
    answer = messagebox.askyesno(title="Calibration", message = msg)

    # Proceed to calibration
    if answer:
        # Give short instructions before the calibration starts (better instructions can be found in the user manual)
        msg = '''  The image can be updated by pressing any key (except ENTER)
                \n 1. Image will have the expected color name written on it 
                \n 2. Place piece of that color in the view \n  of the targeting square 
                \n 3. When ready, press ENTER key to save the color \n 
                \n First color will be called 'Missing' 
                \n this is a reference value and there should not be anything in front of the camera'''
        messagebox.showinfo(title="Info", message = msg)
        Calibration(camera)

# Button function for adding colors
def goAddColor(camera, color):
    if color == "":
        messagebox.showerror(title="error", message= "Color name is missing")

    else:
        msg = '''\nPlace desired color in front of the camera so that it shows in the targeting area. 
                \nPress ENTER to save'''
        messagebox.showinfo(title="Info", message = msg)
        cv2.namedWindow("image",cv2.WINDOW_NORMAL)
        # Loop for image
        while True:
            img = Grab(camera, 1)
            # Add targeting rectagle
            cv2.rectangle(img,(975,555),(1025,605), (255,0,255),2,1)
            cv2.imshow("image", img)
            # Wait for button press ENTER (13) breaks the loop
            k = cv2.waitKey(0)
            if k == 13:
                break

        # Destroy image window and ask for confirmation
        cv2.destroyAllWindows()
        answer = messagebox.askyesno(title="Info", message= "Are you sure you want to add : " + str(color) + " to the library?")
        if answer:
            # Add detected color from detection area
            addDetected(camera,color)

# Button function for getting the white balance values
def goGetWB(camera):
    # Get white balance values and show the in a infobox
    wb = getWB(camera)
    messagebox.showinfo(title="Info", message= "Current white balance values are: " +  str(wb))

# Button function for setting the white balance
def goSetWB(camera):
    # Ask for confirmation and inform user of the tools needed
    msg = "You need the colorchecker white balance sheet to get optimal values! Do you wish to continue?"
    answer = messagebox.askyesno(title="WB", message=msg)
    if answer:
        msg = "To set the new wb values place the colorchecker white balance sheet in front of the camera and press ENTER"
        # Short instruction
        messagebox.showinfo(title="Info", message= msg)
        # Set wb and then get the new values and show them in a infobox
        setWB(camera)
        wb = getWB(camera)
        messagebox.showinfo(title="Info", message= "White balance values set to: " +  str(wb))

# Button function for removing colors
def goRemoveColor(color):
    if color == "":
        messagebox.showerror(title="error", message= "Color name is missing")
    else:
        answer = messagebox.askyesno(title="Info", message="Are you sure you want to remove " + str(color) + " from the library?")
        if answer:
            removeColor(color)

# Button function for reading the library
def goGetLibrary():
    lib = getLibrary()
    msg = ""
    for x in range(len(lib)):
        msg = msg + str(lib[x]) + "\n"
    messagebox.showinfo(title="library", message= msg)

# End of button functions -----------------------------------------------------------------------------------------