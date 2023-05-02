import pandas as pd 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    data1 = pd.read_csv('lapdata.csv')
    data1 = data1.iloc[:-10]
    data2 = pd.read_csv('lapdata2.csv')
    data2 = data2.iloc[:-20]
    x1 = data1['Distance']
    y1 = data1['Gear']
    x2=data2['Distance']
    y2 = data2['Gear']
    plt.cla()
    plt.plot(x1, y1, label='Player#1')
    plt.plot(x2, y2, label='Player#2')
    
    plt.legend(loc='upper left')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()