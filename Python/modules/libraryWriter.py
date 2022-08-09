import csv
import pandas as pd

# Path to library file
path = './modules/colorLibrary.csv'

# Write new row to csv file based on inputs
def addColor(name, rgb):
    hex = "#" + str(rgb_to_hex(rgb[0], rgb[1], rgb[2]))
    data = [name, name, hex, rgb[0], rgb[1], rgb[2]]
    with open(path, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    print("Color added")

# Get hex value from rgb
def rgb_to_hex(r,g,b):
    data = ('{:X}{:X}{:X}').format(r, g, b)
    return data

# Remove color from library
def removeColor(color):
    # Setup the database (csv file)
    oldData = pd.read_csv(path, sep=',', header=None)
    newData = []
    
    for x in range(len(oldData)):
        print(oldData[0][x])
        if oldData[0][x] != color:
            newData.append([oldData[0][x], oldData[1][x], oldData[2][x], 
                            oldData[3][x], oldData[4][x], oldData[5][x]])

    # Open csv file and write data to it
    with open(path, 'w+', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # Write the data from array to csv lines
        for i in range(len(newData)):
            writer.writerow(newData[i])

    # Read the new data and the print it to terminal for inspection
    newDataSet = pd.read_csv(path, sep=',', header=None)
    print(newDataSet)

# Get current library
def getLibrary():
    # Open csv file
    data = pd.read_csv(path, sep=',', header=None)
    lib = []
    # Get color names to array
    for x in range(len(data)):
        lib.append(data[0][x])

    # Return names
    return lib