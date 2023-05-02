import pandas as pd
import matplotlib.pyplot as plt


def plot_data(filename1, filename2):
    # Load the first CSV file and plot the data
    df1 = pd.read_csv(filename1)
    df1 = df1.iloc[:-10]

    fig, axs = plt.subplots(nrows=4, ncols=1)

    # Load the second CSV file and plot the data
    df2 = pd.read_csv(filename2)
    df2 = df2.iloc[:-20]

    plt.subplot(4,1,1)
    plt.plot(df1['Distance'], df1['Speeds'], label='Player#1')
    plt.plot(df2['Distance'], df2['Speeds'], label='Player#2')

    plt.subplot(4,1,2)
    plt.plot(df1['Distance'], df1['Throttle'], label='Player#1')
    plt.plot(df2['Distance'], df2['Throttle'], label='Player#2')

    plt.subplot(4,1,3)
    plt.plot(df1['Distance'], df1['Brake'], label='Player#1')
    plt.plot(df2['Distance'], df2['Brake'], label='Player#2')

    plt.subplot(4,1,4)
    plt.plot(df1['Distance'], df1['Gear'], label='Player#1')
    plt.plot(df2['Distance'], df2['Gear'], label='Player#2')

    # Add legend and labels to the plot
    fig.legend()
    fig.text(0.5, 0.04, 'Distance', ha='center')
    fig.text(0.04, 0.5, 'Value', va='center', rotation='vertical')

    # Show the plot
    plt.show()


plot_data('lapdata.csv', 'lapdata2.csv')