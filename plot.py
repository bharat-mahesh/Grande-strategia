import boto3
import matplotlib.pyplot as plt
import json
import time
import numpy as np
from numpy import load
import csv

client = boto3.client('kinesis')
stream_name = 'grande-strategia'

# get the latest shard iterator
shard_iterator = client.get_shard_iterator(
    StreamName=stream_name,
    ShardId='shardId-000000000000',
    ShardIteratorType='LATEST'
)['ShardIterator']

#-----------------------------------------------------------------------------------------------
with open('tracks.json', 'r') as f:
    data = json.load(f)

track_name = input("Enter the name of a track: ")

track = None
for t in data['tracks']:
    if t['name'] == track_name:
        track = t
        break

if track:
    track_length = track['length']
    print(f"The length of {track_name} is {track_length} meters.")
else:
    print(f"{track_name} was not found in the list of tracks.")

#------------------------------------------------------------------------------------------------
# initialize the plot
fig, (ax,ax_throttle,ax_brake) = plt.subplots(nrows=3, ncols=1, sharex=True)
ax.set_xlabel('Distance')
ax.set_ylabel('Speed')


ax_throttle.set_xlabel('Distance')
ax_throttle.set_ylabel('Throttle')


ax_brake.set_xlabel('Distance')
ax_brake.set_ylabel('Brake')

# set the x and y limits of the plot
ax.set_xlim(0, track_length)
ax.set_ylim(0, 400)

ax_throttle.set_xlim(0, track_length)
ax_throttle.set_ylim(0, 2)

ax_brake.set_xlim(0, track_length)
ax_brake.set_ylim(0, 2)

# initialize the line object
line, = ax.plot([], [])
line2,=ax_throttle.plot([],[])
line3,=ax_brake.plot([],[])
# initialize the list of speeds and dictionary of lap counts
throttle=[]
speeds = []
distance=[]
count=0
lap_counts=1
m_lapNumber=0
while True:
    # get the latest records
    response = client.get_records(
        ShardIterator=shard_iterator,
        Limit=100
    )

    # update the shard iterator
    shard_iterator = response['NextShardIterator']

    # extract the speed data and lap count from the records
    for record in response['Records']:
        if record["PartitionKey"]=='Lapdata':
            data_str2 = record["Data"].decode('utf-8')
            data_obj2 = json.loads(data_str2)
            m_lapNumber=data_obj2['m_currentLapNum']
            m_lapdistance=data_obj2['m_lapDistance']
        else:
            data_str=record["Data"].decode("utf8")
            data_obj = json.loads(data_str)
            m_speed = data_obj['m_speed']
            m_throttle=data_obj['m_throttle']
            m_brake=data_obj['m_brake']
            if m_speed !=0:
                speeds.append(m_speed)
                distance.append(m_lapdistance)                
                throttle.append(m_throttle)
                brake.append(m_brake)
        # update the dictionary of lap counts
    # print("SPEED",speeds)
    # print("Distance",distance)    
    # check if any lap counts have changed
        
    if lap_counts !=m_lapNumber:
        speeds=[]
        distance=[]
        throttle=[]
        brake=[]
        lap_counts=m_lapNumber
    
    # update the plot data
    line.set_xdata(distance)
    line.set_ydata(speeds)

    line2.set_xdata(distance)
    line2.set_ydata(throttle)

    line3.set_xdata(distance)
    line3.set_ydata(brake)

    # # update the plot
    plt.draw()
    plt.pause(0.2)

    #-----------------------------------------
#     # Saving arrays
#     np.savez('data.npz', throttle=throttle, speeds=speeds, distance=distance)

# # Saving plot
#     plt.savefig('myplot.png')
#     data = load('data.npz')
#     lst = data.files
#     for item in lst:
#         print(item)
#         print(data[item])
#------------------------------------------------------

# Save data to CSV file
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Throttle', 'Speeds', 'Distance'])
        for i in range(len(throttle)):
            writer.writerow([throttle[i], speeds[i], distance[i]])