import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def take_inputs():
    area = input("What's the area of the membrane? (in cm^2)")
    blank = input("What's your blank value? (in ohms)")
    return float(area.strip()), float(blank.strip())

def read_csv():
    data = pd.read_csv('voltagevalues.txt', sep=" ", header=None)
    data.columns = ["voltage", "time"]
    return data

def process_voltage(data):
    voltage = data.voltage.tolist()
    data['voltage'] = data['voltage'].astype(float)
    return voltage

def process_time(data):
    time = data.time.tolist()
    data['time'] = data['time'].astype(float)
    return time

def find_resistance(voltage):
    resistance = []
    for value in voltage:
        r2 = (5 * 20000) / (5 - value)
        resistance.append(float(r2))
    return resistance

def find_TEER(resistance, area, blank):
    TEER = []

    for value in resistance:
        teer = (value - blank) * (area)
        TEER.append(float(teer))

    return TEER

def plot_everything(TEER, time):
    answer = input('Do you want to plot with plotly or with Matlab?')
    if (answer.lower()).strip() == 'matlab':
        plt.plot(time,TEER)
        plt.title('TEER vs time')
        plt.xlabel('Time (s)')
        plt.ylabel('TEER (ohm/cm^2)')
        plt.show()
    elif (answer.lower()).strip() == 'plotly':
        fig = go.Figure(data=go.Scatter( x = time,
            y = TEER,
            mode = 'lines'
        ))
        fig.update_layout(
        title=go.layout.Title(
            text="TEER vs time",
            xref="paper",
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
            text="Time in seconds",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
        )
        )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
            text="TEER in ohm/cm^2",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
            )
            )
            )

        fig.show()
    else:
        print("That's not an option, sorry!")

if __name__ == '__main__':
    area, blank = take_inputs()
    data = read_csv()
    voltage = process_voltage(data)
    time = process_time(data)
    resistance = find_resistance(voltage)
    TEER = find_TEER(resistance, area, blank)
    plot_everything(TEER, time)
