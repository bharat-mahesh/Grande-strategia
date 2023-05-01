import pandas as pd
import matplotlib.pyplot as plt


# Load the first CSV file and plot the data
df1 = pd.read_csv('lapdata.csv')
df1 = df1.iloc[:-5]

plt.plot(df1['Distance'], df1['Speeds'], label='Graph 1')

# Load the second CSV file and plot the data
df2 = pd.read_csv('lapdata2.csv')
df2 = df2.iloc[:-15]

plt.plot(df2['Distance'], df2['Speeds'], label='Graph 2')

# Add legend and labels to the plot
plt.legend()
plt.xlabel('X-axis label')
plt.ylabel('Y-axis label')

# Show the plot
plt.show()
