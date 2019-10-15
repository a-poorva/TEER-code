Code for TEER measuring device

res_version.py: This code measures TEER every 5 seconds, sleeps for 10 seconds and resumes 
measurement. This can be changed according to requirements, along with the 
file in which it is saved. 

reads_voltagevalues.py: This takes values from the text file populated by res_version.py and processes it such that it plots TEER vs time. It asks for area of membrane and blank reading to be inputted, and plots either using MATLAB or plotly depending on your input.
