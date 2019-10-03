#################################################################
# ME-555 Experimental Microfluidics
# Instructor: Benjamin Yellen
# Email: yellen@duke.edu
# Date Edited: September 7, 2019
#
#################################################################
# Import Libraries
#################################################################

from tkinter import ttk
from tkinter import filedialog
from tkinter import *
import tkinter as tk
import os
import csv


#################################################################
### Handshake with Arduino
#################################################################

from nanpy import(ArduinoApi,SerialManager)

try:
   print("Trying to make a connection")
   connection = SerialManager()
   a = ArduinoApi(connection=connection)
   print("Success!")
except:
   print("Failed to connect to Arduino")

###############################################################
# Setup Arduino Pins
###############################################################

sensePin1=0
sensePin2=1
sensePin3=2
sensePin4=3
sensePin5=4
sensePin6=5

a.pinMode(sensePin1, a.INPUT)
a.pinMode(sensePin2, a.INPUT)
a.pinMode(sensePin3, a.INPUT)
a.pinMode(sensePin4, a.INPUT)
a.pinMode(sensePin5, a.INPUT)
a.pinMode(sensePin6, a.INPUT)

outPin1 = 3
outPin2 = 5
outPin3 = 6
outPin4 = 9
outPin5 = 10
outPin6 = 11

a.pinMode(outPin1, a.OUTPUT)
a.pinMode(outPin2, a.OUTPUT)
a.pinMode(outPin3, a.OUTPUT)
a.pinMode(outPin4, a.OUTPUT)
a.pinMode(outPin5, a.OUTPUT)
a.pinMode(outPin6, a.OUTPUT)

####################################
# Define Directories
####################################

data_dir = '/home/pi/Documents/Data/'
code_dir = '/home/pi/Documents/'

####################################
# Define Button Functions
####################################

def Reset():
    setPres1.set('')
    setPres2.set('')
    setPres3.set('')
    setPres4.set('')
    setPres5.set('')
    setPres6.set('')

def LoadVal():
    with open(os.path.join(data_dir,
                'PressureValues.csv'), 'r') as f:
        rows=list(csv.reader(f))
        SavedSetPres1 = str(rows[1][1])
        SavedSetPres2 = str(rows[2][1])
        SavedSetPres3 = str(rows[3][1])
        SavedSetPres4 = str(rows[4][1])
        SavedSetPres5 = str(rows[5][1])
        SavedSetPres6 = str(rows[6][1])
        setPres1.set(SavedSetPres1)
        setPres2.set(SavedSetPres2)
        setPres3.set(SavedSetPres3)
        setPres4.set(SavedSetPres4)
        setPres5.set(SavedSetPres5)
        setPres6.set(SavedSetPres6)

def SaveVal():
    SavedSetPres1 = setPres1.get()
    SavedSetPres2 = setPres2.get()
    SavedSetPres3 = setPres3.get()
    SavedSetPres4 = setPres4.get()
    SavedSetPres5 = setPres5.get()
    SavedSetPres6 = setPres6.get()
    with open(os.path.join(data_dir,
                'PressureValues.csv'), 'r') as r:
        rows = list(csv.reader(r))
        rows[1][1] = SavedSetPres1
        rows[2][1] = SavedSetPres2
        rows[3][1] = SavedSetPres3
        rows[4][1] = SavedSetPres4
        rows[5][1] = SavedSetPres5
        rows[6][1] = SavedSetPres6
        writer = csv.writer(open(os.path.join(data_dir,
                            'PressureValues.csv'), 'w'))
        writer.writerows(rows)

def ExitWindow():
    root.destroy()

#################################################################
# Define Pressure Sensor GUI functions
#################################################################


def convertPressure(val):
    pressureConvert = ((val-102.4)* (10/(0.8*1024)) - 5) * 68.9476
    return pressureConvert


def convertSetPoint(val):
    setPoint = math.floor(-float(val)/3.6)
    return setPoint


def setController():
    readSensors()
    storeReadPres()
    setOutPres()
    setPresLabels()
    root.after(200,setController)


def storeReadPres():
    global readPres1
    global readPres2
    global readPres3
    global readPres4
    global readPres5
    global readPres6
    readPres1 = readSensor1.get(block=False)
    readPres2 = readSensor2.get(block=False)
    readPres3 = readSensor3.get(block=False)
    readPres4 = readSensor4.get(block=False)
    readPres5 = readSensor5.get(block=False)
    readPres6 = readSensor6.get(block=False)


def setOutPres():
    a.analogWrite(outPin1, convertSetPoint(SavedSetPres1))
    a.analogWrite(outPin2, convertSetPoint(SavedSetPres2))
    a.analogWrite(outPin3, convertSetPoint(SavedSetPres3))
    a.analogWrite(outPin4, convertSetPoint(SavedSetPres4))
    a.analogWrite(outPin5, convertSetPoint(SavedSetPres5))
    a.analogWrite(outPin6, convertSetPoint(SavedSetPres6))


def setPresLabels():
    pressure1.set(round(readPres1,1))
    pressure2.set(round(readPres2,1))
    pressure3.set(round(readPres3,1))
    pressure4.set(round(readPres4,1))
    pressure5.set(round(readPres5,1))
    pressure6.set(round(readPres6,1))


def readSensors():
    readSensor1.put(convertPressure(a.analogRead(sensePin1)))
    readSensor2.put(convertPressure(a.analogRead(sensePin2)))
    readSensor3.put(convertPressure(a.analogRead(sensePin3)))
    readSensor4.put(convertPressure(a.analogRead(sensePin4)))
    readSensor5.put(convertPressure(a.analogRead(sensePin5)))
    readSensor6.put(convertPressure(a.analogRead(sensePin6)))


#################################################################
# Define Number Pad Functions
#################################################################

num_run = 0
btn_funcid = 0
insert_entry = None


def click(btn):
    global num_run
    global insert_entry
    if insert_entry is None:
        return
    text = "%s" % btn
    if not text == "←" and not text == "X":
        insert_entry.insert(tk.END, text)
    if text == '←':
        insert_entry.delete(0, tk.END)
    if text == 'X':
        boot.destroy()
        num_run = 0
        root.unbind('<Button-1>', btn_funcid)


def numpad():
    global num_run, boot
    boot = tk.Tk()
    boot.geometry('%dx%d+%d+%d' % (250,300,0,0))
    boot['bg'] = 'grey'
    lf = tk.LabelFrame(boot, text="", bd=1)
    lf.pack(padx=1, pady=1)
    btn_list = [
        '7',  '8',  '9',
        '4',  '5',  '6',
        '1',  '2',  '3',
        '0',  '.',  '-',
        '←', 'X']
    r = 1
    c = 0
    n = 0
    btn = list(range(len(btn_list)))
    for label in btn_list:
        cmd = partial(click, label)
        btn[n] = tk.Button(lf, text=label,
                           width=4, height=2,
                           command=cmd)
        btn[n].grid(row=r, column=c)
        n += 1
        c += 1
        if c == 3:
            c = 0
            r += 1


def close(event):
    global num_run, btn_funcid
    if num_run == 1:
        boot.destroy()
        num_run = 0
        root.unbind('<Button-1>', btn_funcid)


def run(event):
    global num_run, btn_funcid
    global insert_entry
    insert_entry = event.widget # use the caller to adapt it
    if num_run == 0:
        num_run = 1
        numpad()
        btn_funcid = root.bind('<Button-1>', close)


#################################################################
# Get Previously Stored Values
#################################################################

with open(os.path.join(data_dir,
            'PressureValues.csv'), 'r') as f:
    rows=list(csv.reader(f))
    SavedSetPres1 = str(rows[1][1])
    SavedSetPres2 = str(rows[2][1])
    SavedSetPres3 = str(rows[3][1])
    SavedSetPres4 = str(rows[4][1])
    SavedSetPres5 = str(rows[5][1])
    SavedSetPres6 = str(rows[6][1])

####################################
# Start Gui
####################################

root = tk.Tk()
root.title("ME-555 Controller")
#root.geometry("720x480")

####################################
# Setup Queues
####################################

readSensor1 = queue.Queue()
readSensor2 = queue.Queue()
readSensor3 = queue.Queue()
readSensor4 = queue.Queue()
readSensor5 = queue.Queue()
readSensor6 = queue.Queue()

####################################
# Define Variables
####################################

labelwidth = 20
notepadwidth = 8
entrywidth = 10
buttonwidth = 10
labelpadding = 2
entrypadding = 2

readPres1 = 0
pressure1 = StringVar()
pressure1.set("---- ")
pressure2 = StringVar()
pressure2.set("---- ")
pressure3 = StringVar()
pressure3.set("---- ")
pressure4 = StringVar()
pressure4.set("---- ")
pressure5 = StringVar()
pressure5.set("---- ")
pressure6 = StringVar()
pressure6.set("---- ")


####################################
# Define the GUI frames
####################################

Mainframe = tk.Frame(root)
Mainframe.grid(row=0, column=0, rowspan=4,
               columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S)
Sidebar = tk.Frame(root)
Sidebar.grid(row=0, column=3, rowspan=4,
             columnspan=1, sticky=tk.W+tk.E+tk.N+tk.S)

# Defining the notebook
nb = ttk.Notebook(Mainframe)

# Defining the frame in the notebook for regulator 1
pressureFrame1 = ttk.Frame(nb)
nb.add(pressureFrame1, text='Reg 1')
setPres1 = StringVar(pressureFrame1, value = SavedSetPres1)
SetPresLabel1 = Label(pressureFrame1, text="Set Pressure 1:",
                      width = labelwidth, anchor = 'w')
SetPresLabel1.grid(column=0, row=0)
SetPresValue1 = Entry(pressureFrame1, textvariable=setPres1,
                      width = entrywidth, justify = "right")
SetPresValue1.grid(column=1, row=0)
SetPresValue1.bind('<Button-1>', run)
RecPres1 = Label(pressureFrame1, text="Recorded Pressure 1:",
                 width = labelwidth, anchor = 'w')
RecPres1.grid(column=0, row=1)
ReadPres1 = Label(pressureFrame1, textvariable=pressure1,
                  width = entrywidth, anchor = 'e')
ReadPres1.grid(column=1, row=1)
Label(pressureFrame1, text="mbar").grid(column=2, row=0)
Label(pressureFrame1, text="mbar").grid(column=2, row=1)

# Defining the frame in the notebook for regulator 2
pressureFrame2 = ttk.Frame(nb)
nb.add(pressureFrame2, text='Reg 2')
nb.pack(expand=1, fill='both')
setPres2 = StringVar(pressureFrame2, value = SavedSetPres2)
SetPresLabel2 = Label(pressureFrame2, text="Set Pressure 2:",
                      width = labelwidth, anchor = 'w')
SetPresLabel2.grid(column=0, row=0)
SetPresValue2 = Entry(pressureFrame2, textvariable=setPres2,
                      width = entrywidth, justify = "right")
SetPresValue2.grid(column=1, row=0)
SetPresValue2.bind('<Button-1>', run)
RecPres2 = Label(pressureFrame2, text="Recorded Pressure 2:",
                 width = labelwidth, anchor = 'w')
RecPres2.grid(column=0, row=1)
ReadPres2 = Label(pressureFrame2, textvariable=pressure2,
                  width = entrywidth, anchor = 'e')
ReadPres2.grid(column=1, row=1)
Label(pressureFrame2, text="mbar").grid(column=2, row=0)
Label(pressureFrame2, text="mbar").grid(column=2, row=1)

# Defining the frame in the notebook for regulator 3
pressureFrame3 = ttk.Frame(nb)
nb.add(pressureFrame3, text='Reg 3')
nb.pack(expand=1, fill='both')
setPres3 = StringVar(pressureFrame3, value = SavedSetPres3)
SetPresLabel3 = Label(pressureFrame3, text="Set Pressure 3:",
                      width = labelwidth, anchor = 'w')
SetPresLabel3.grid(column=0, row=0)
SetPresValue3 = Entry(pressureFrame3, textvariable=setPres3,
                      width = entrywidth, justify = "right")
SetPresValue3.grid(column=1, row=0)
SetPresValue3.bind('<Button-1>', run)
RecPres3 = Label(pressureFrame3, text="Recorded Pressure 3:",
                 width = labelwidth, anchor = 'w')
RecPres3.grid(column=0, row=1)
ReadPres3 = Label(pressureFrame3, textvariable=pressure3,
                  width = entrywidth, anchor = 'e')
ReadPres3.grid(column=1, row=1)
Label(pressureFrame3, text="mbar").grid(column=2, row=0)
Label(pressureFrame3, text="mbar").grid(column=2, row=1)

# Defining the frame in the notebook for regulator 4
pressureFrame4 = ttk.Frame(nb)
nb.add(pressureFrame4, text='Reg 4')
setPres4 = StringVar(pressureFrame4, value = SavedSetPres4)
SetPresLabel4 = Label(pressureFrame4, text="Set Pressure 4:",
                      width = labelwidth, anchor = 'w')
SetPresLabel4.grid(column=0, row=0)
SetPresValue4 = Entry(pressureFrame4, textvariable=setPres4,
                      width = entrywidth, justify = "right")
SetPresValue4.grid(column=1, row=0)
SetPresValue4.bind('<Button-1>', run)
RecPres4 = Label(pressureFrame4, text="Recorded Pressure 4:",
                 width = labelwidth, anchor = 'w')
RecPres4.grid(column=0, row=1)
ReadPres4 = Label(pressureFrame4, textvariable=pressure4,
                  width = entrywidth, anchor = 'e')
ReadPres4.grid(column=1, row=1)
Label(pressureFrame4, text="mbar").grid(column=2, row=0)
Label(pressureFrame4, text="mbar").grid(column=2, row=1)

# Defining the frame in the notebook for regulator 5
pressureFrame5 = ttk.Frame(nb)
nb.add(pressureFrame5, text='Reg 5')
nb.pack(expand=1, fill='both')
setPres5 = StringVar(pressureFrame5, value = SavedSetPres5)
SetPresLabel5 = Label(pressureFrame5, text="Set Pressure 5:",
                      width = labelwidth, anchor = 'w')
SetPresLabel5.grid(column=0, row=0)
SetPresValue5 = Entry(pressureFrame5, textvariable=setPres5,
                      width = entrywidth, justify = "right")
SetPresValue5.grid(column=1, row=0)
SetPresValue5.bind('<Button-1>', run)
RecPres5 = Label(pressureFrame5, text="Recorded Pressure 5:",
                 width = labelwidth, anchor = 'w')
RecPres5.grid(column=0, row=1)
ReadPres5 = Label(pressureFrame5, textvariable=pressure5,
                  width = entrywidth, anchor = 'e')
ReadPres5.grid(column=1, row=1)
Label(pressureFrame5, text="mbar").grid(column=2, row=0)
Label(pressureFrame5, text="mbar").grid(column=2, row=1)

# Defining the frame in the notebook for regulator 6
pressureFrame6 = ttk.Frame(nb)
nb.add(pressureFrame6, text='Reg 6')
nb.pack(expand=1, fill='both')
setPres6 = StringVar(pressureFrame6, value = SavedSetPres6)
SetPresLabel6 = Label(pressureFrame6, text="Set Pressure 6:",
                      width = labelwidth, anchor = 'w')
SetPresLabel6.grid(column=0, row=0)
SetPresValue6 = Entry(pressureFrame6, textvariable=setPres6,
                      width = entrywidth, justify = "right")
SetPresValue6.grid(column=1, row=0)
SetPresValue6.bind('<Button-1>', run)
RecPres6 = Label(pressureFrame6, text="Recorded Pressure 6:",
                 width = labelwidth, anchor = 'w')
RecPres6.grid(column=0, row=1)
ReadPres6 = Label(pressureFrame6, textvariable=pressure6,
                  width = entrywidth, anchor = 'e')
ReadPres6.grid(column=1, row=1)
Label(pressureFrame6, text="mbar").grid(column=2, row=0)
Label(pressureFrame6, text="mbar").grid(column=2, row=1)


####################################
# Define the action buttons
####################################

ButtonPreset = tk.Button(Sidebar, text="Preset",
                         width = buttonwidth,
                         command=lambda:LoadVal())
ButtonPreset.grid(row=1, column=0, padx=1, pady=1)
ButtonReset = tk.Button(Sidebar, text="Reset",
                        width = buttonwidth,
                        command=lambda:Reset())
ButtonReset.grid(row=2, column=0, padx=1, pady=1)
ButtonSaveVal = tk.Button(Sidebar, text="Save",
                          width = buttonwidth,
                          command=lambda:SaveVal())
ButtonSaveVal.grid(row=3, column=0, padx=1, pady=1)
ButtonExit = tk.Button(Sidebar, text="Exit",
                       width = buttonwidth,
                       command=lambda:ExitWindow())
ButtonExit.grid(row=4, column=0, padx=1, pady=1)


####################################
# Mainloop
####################################

root.after(200, setController)
root.mainloop()
