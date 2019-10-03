from nanpy import(ArduinoApi, SerialManager)
from time import sleep
#Handshake with arduino
try:
    print("Trying to make a connection")
    connection = SerialManager()
    a = ArduinoApi(connection = connection)
    print("Success!")
except:
    print("Failed to connect to Arduino. :(")

from tkinter import ttk
from tkinter import *
import tkinter as tk
import os
import csv

#setting up Arduino pins
VoltPin1 = 0
a.pinMode = (VoltPin1, a.INPUT)

root = tk.Tk() #making a window called root, refreshes continually so that it updates information
root.title("ME-555 Controller")

#Get previously stored values
data_dir = '/home/pi/Documents/Data/'
code_dir = '/home/pi/Documents/'

#function definition
def Reset():
    SetVolt.set('0')

def readVoltage():
    root.after(200, readVoltage)
    VoltReading1 = a.analogRead(VoltPin1)
    VoltActual = str(VoltReading1 * (5.0 / 1023.0))
    Voltage.set(str(VoltActual))
    fb = open('/home/pi/voltagevalues.txt','a+')
    fb.write(VoltActual)
    fb.write('\n')
    fb.close()

def SaveValues():
    SavedSetVolt = SetVolt.get()
    with open(os.path.join(data_dir, 'resistance_values.csv'),'r') as f:
        rows = list(csv.reader(f))
        rows[1][1] = SavedSetRes
        writer = csv.writer(open(os.path.join(data_dir,'resistance_values.csv'), 'w'))
        writer.writerows(rows)

with open(os.path.join(data_dir, 'resistance_values.csv'), 'r') as f:
     rows = list(csv.reader(f)) #reads each row of the csv file like a list
     SavedSetVolt = str(rows[1][1])

#frame definition
Mainframe = tk.Frame(root) #in tkinter, you're making a frame called Mainframe
Mainframe.grid(row = 0, column = 0, rowspan=4, columnspan=3) #rowspan is how wide, columnspan is how tall
Sidebar = tk.Frame(root)
Sidebar.grid(row = 0, column = 3, rowspan=4, columnspan=1)

nb = ttk.Notebook(Mainframe) #a sub-module for tabs and stuff, all located in the Mainframe

#Defining voltage frame in the notebook
VoltFrame = ttk.Frame(nb)
nb.add(VoltFrame, text = 'Voltage')
SetVoltLabel1 = Label(VoltFrame, text = "Input Voltage:", width = 20)
SetVoltLabel1.grid(column=0, row=0) #pack, grid, place: placement line

SetVoltLabel2 = Label(VoltFrame, text = "Recorded Voltage:", width = 20)
SetVoltLabel2.grid(column=0, row=1) #pack, grid, place: placement line

SetVolt = StringVar(VoltFrame,value = SavedSetVolt) #initialise
SetRecVoltValue = Entry(VoltFrame, textvariable = SetVolt, width = 20)
SetRecVoltValue.grid(column=1, row=0) #pack, grid, place: placement line

Voltage = StringVar()
Voltage.set("------")

ReadVolt1 = Label(VoltFrame, textvariable = Voltage, width = 20,anchor = 'e')
ReadVolt1.grid(column = 1, row = 1)

nb.pack(expand =1, fill = 'both') #pack, grid, place. Pack puts these options in a particular place



#Exit Button
ButtonExit = tk.Button(Sidebar, text = "Exit", width = 20, command = root.destroy) #latter tells you to close the window
ButtonExit.grid(row =0, column =0)


#Reset Button
ButtonExit = tk.Button(Sidebar, text = "Reset",
                       width = 20,
                       command = lambda:Reset()) #lambda is a built in variable that allows#you to call certain functions
ButtonExit.grid(row =1, column =0)


root.after(200, readVoltage)
root.mainloop()
