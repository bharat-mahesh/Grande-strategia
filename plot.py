import boto3
import matplotlib.pyplot as plt
import json
import time

client = boto3.client('kinesis')
stream_name = 'grande-strategia'

# get the latest shard iterator
shard_iterator = client.get_shard_iterator(
    StreamName=stream_name,
    ShardId='shardId-000000000000',
    ShardIteratorType='LATEST'
)['ShardIterator']

# initialize the plot
fig, ax = plt.subplots()
ax.set_xlabel('Distance')
ax.set_ylabel('Speed')
ax.set_title('Real-time Speed Data')

# set the x and y limits of the plot
ax.set_xlim(0, 5412)
ax.set_ylim(0, 400)

# initialize the line object
line, = ax.plot([], [])

# initialize the list of speeds and dictionary of lap counts
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
            if m_speed !=0:
                speeds.append(m_speed)
                distance.append(m_lapdistance)                
        # update the dictionary of lap counts
    # print("SPEED",speeds)
    # print("Distance",distance)    
    # check if any lap counts have changed
        
    if lap_counts !=m_lapNumber:
        speeds=[]
        distance=[]
        lap_counts=m_lapNumber
    
    # update the plot data
    line.set_xdata(distance)
    line.set_ydata(speeds)

    # # update the plot
    plt.draw()
    plt.pause(0.2)
