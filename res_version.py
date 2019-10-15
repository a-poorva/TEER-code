from nanpy import(ArduinoApi, SerialManager)

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
import schedule
import time
from time import sleep
import random
import math

#setting up Arduino pins
VoltPin1 = 0
a.pinMode = (VoltPin1, a.INPUT)

start_time = time.time()

root = tk.Tk() #making a window called root, refreshes continually so that it updates information
root.title("ME-555 Controller")

#Get previously stored values
data_dir = '/home/pi/Documents/data'
code_dir = '/home/pi/Documents/'

Voltage = StringVar()
Voltage.set("------")

#function definition
def Reset():
    SetVolt.set('0')

def Exit():
    root.destroy()

def readVoltage():
    for counter in range (1,12):
        with open(os.path.join(code_dir, 'voltagevalues.txt'),'a+') as fb:
            VoltReading1 = a.analogRead(VoltPin1)
            VoltActual = str(VoltReading1 * (5.0 / 1023.0))
            Voltage.set(str(VoltActual))
            elapsed_time = time.time() - start_time
            fb.write('\n')
            fb.write("Voltage is: ")
            fb.write(str(VoltActual))
            fb.write(', ')
            fb.write(str("Time:"))
            fb.write(str(elapsed_time))
            time.sleep(5)
    root.after(5000, readVoltage)

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

SetVolt = StringVar(VoltFrame,value = 1) #initialise
SetRecVoltValue = Entry(VoltFrame, textvariable = SetVolt, width = 20)
SetRecVoltValue.grid(column=1, row=0) #pack, grid, place: placement line

SetVoltLabel2 = Label(VoltFrame, text = "Recorded Voltage:", width = 20)
SetVoltLabel2.grid(column=0, row=1) #pack, grid, place: placement line

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


root.after(5000, readVoltage)
root.mainloop()
