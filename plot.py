import boto3
import matplotlib.pyplot as plt
import json
import time
import numpy as np
from numpy import load
import csv

client = boto3.client("kinesis")
stream_name = "grande-strategia"

# get the latest shard iterator
shard_iterator = client.get_shard_iterator(
    StreamName=stream_name, ShardId="shardId-000000000000", ShardIteratorType="LATEST"
)["ShardIterator"]

# -----------------------------------------------------------------------------------------------
with open("tracks.json", "r") as f:
    data = json.load(f)

# track_name = input("Enter the name of a track: ")
print("Select a track number:")
for i, t in enumerate(data["tracks"]):
    print(f"{i+1}. {t['name']}")


# track = None
# for t in data["tracks"]:
#     if t["name"] == track_name:
#         track = t
#         break
track_number = int(input())
if 1 <= track_number <= len(data["tracks"]):
    track = data["tracks"][track_number - 1]
    track_name = track["name"]
    track_length = track["length"]
    print(f"The length of {track_name} is {track_length} meters.")
else:
    print(
        f"Invalid track number. Please select a number between 1 and {len(data['tracks'])}."
    )

def convert_milliseconds_to_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

# if track:
#     track_length = track["length"]
#     print(f"The length of {track_name} is {track_length} meters.")
# else:
#     print(f"{track_name} was not found in the list of tracks.")

# ------------------------------------------------------------------------------------------------
# initialize the plot
fig, (
    ax,
    ax_throttle,
    ax_brake,
    ax_gear,
    axTeammate,
    ax_throttleTeammate,
    ax_brakeTeammate,
    ax_gearTeammate,
    # axspeed_merge,
    # ax_throttle_merge,
    # ax_brake_merge,
    # ax_gear_merge,
) = plt.subplots(nrows=8, ncols=1)


ax.set_xlabel("Distance")
ax.set_ylabel("Speed")


ax_throttle.set_xlabel("Distance")
ax_throttle.set_ylabel("Throttle")


ax_brake.set_xlabel("Distance")
ax_brake.set_ylabel("Brake")

ax_gear.set_xlabel("Distance")
ax_gear.set_ylabel("Gear")

axTeammate.set_xlabel("Distance")
axTeammate.set_ylabel("Speed")


ax_throttleTeammate.set_xlabel("Distance")
ax_throttleTeammate.set_ylabel("Throttle")


ax_brakeTeammate.set_xlabel("Distance")
ax_brakeTeammate.set_ylabel("Brake")

ax_gearTeammate.set_xlabel("Distance")
ax_gearTeammate.set_ylabel("Gear")

# axspeed_merge.set_xlabel("Distance")
# axspeed_merge.set_ylabel("Speed")


# ax_throttle_merge.set_xlabel("Distance")
# ax_throttle_merge.set_ylabel("Throttle")


# ax_brake_merge.set_xlabel("Distance")
# ax_brake_merge.set_ylabel("Brake")

# ax_gear_merge.set_xlabel("Distance")
# ax_gear_merge.set_ylabel("Gear")

# set the x and y limits of the plot
ax.set_xlim(0, track_length)
ax.set_ylim(0, 400)

ax_throttle.set_xlim(0, track_length)
ax_throttle.set_ylim(0, 2)

ax_brake.set_xlim(0, track_length)
ax_brake.set_ylim(0, 2)

ax_gear.set_xlim(0, track_length)
ax_gear.set_ylim(0, 10)


# axspeed_merge.set_xlim(0, track_length)
# axspeed_merge.set_ylim(0, 400)

# ax_throttle_merge.set_xlim(0, track_length)
# ax_throttle_merge.set_ylim(0, 2)

# ax_brake_merge.set_xlim(0, track_length)
# ax_brake_merge.set_ylim(0, 2)

# ax_gear_merge.set_xlim(0, track_length)
# ax_gear_merge.set_ylim(0, 10)


axTeammate.set_xlim(0, track_length)
axTeammate.set_ylim(0, 400)

ax_throttleTeammate.set_xlim(0, track_length)
ax_throttleTeammate.set_ylim(0, 2)

ax_brakeTeammate.set_xlim(0, track_length)
ax_brakeTeammate.set_ylim(0, 2)

ax_gearTeammate.set_xlim(0, track_length)
ax_gearTeammate.set_ylim(0, 10)
# initialize the line object
(line,) = ax.plot([], [])
(line2,) = ax_throttle.plot([], [])
(line3,) = ax_brake.plot([], [])
(line7,) = ax_gear.plot([], [])
(line4,) = axTeammate.plot([], [])
(line5,) = ax_throttleTeammate.plot([], [])
(line6,) = ax_brakeTeammate.plot([], [])
(line8,) = ax_gearTeammate.plot([], [])
# initialize the list of speeds and dictionary of lap counts
throttle_1 = []
speeds_1 = []
distance_1 = []
brake_1 = []
gear_1=[]
count_1 = 0
lap_counts_1 = 1
m_lapNumber_1 = 0
m_timelastlap_1=0

throttle_2 = []
speeds_2 = []
distance_2 = []
brake_2 = []
gear_2=[]
count_2 = 0
lap_counts_2 = 1
m_lapNumber_2 = 0
m_timelastlap_2=0
while True:
    # get the latest records
    response = client.get_records(ShardIterator=shard_iterator, Limit=100)

    # update the shard iterator
    shard_iterator = response["NextShardIterator"]

    # extract the speed data and lap count from the records
    for record in response["Records"]:
        if record["PartitionKey"] == "Lapdata-1":
            data_str1 = record["Data"].decode("utf-8")
            data_obj1 = json.loads(data_str1)
            m_lapNumber_1 = data_obj1["m_currentLapNum"]
            m_lapdistance_1 = data_obj1["m_lapDistance"]
            m_timelastlap_1=data_obj1["m_lastLapTimeInMS"]
        elif record["PartitionKey"] == "Lapdata-2":
            data_str2 = record["Data"].decode("utf-8")
            data_obj2 = json.loads(data_str2)
            m_lapNumber_2 = data_obj2["m_currentLapNum"]
            m_lapdistance_2 = data_obj2["m_lapDistance"]
            m_timelastlap_2=data_obj2["m_lastLapTimeInMS"]
        elif record["PartitionKey"] == "Car-1":
            data_str3 = record["Data"].decode("utf8")
            data_obj3 = json.loads(data_str3)
            m_speed_1 = data_obj3["m_speed"]
            m_throttle_1 = data_obj3["m_throttle"]
            m_brake_1 = data_obj3["m_brake"]
            m_gear_1 = data_obj3["m_gear"]
            if m_speed_1 != 0:
                speeds_1.append(m_speed_1)
                distance_1.append(m_lapdistance_1)
                throttle_1.append(m_throttle_1)
                brake_1.append(m_brake_1)
                gear_1.append(m_gear_1)
        elif record["PartitionKey"] == "Car-2":
            data_str4 = record["Data"].decode("utf8")
            data_obj4 = json.loads(data_str4)
            m_speed_2 = data_obj4["m_speed"]
            m_throttle_2 = data_obj4["m_throttle"]
            m_brake_2 = data_obj4["m_brake"]
            m_gear_2 = data_obj4["m_gear"]
            if m_speed_2 != 0:
                speeds_2.append(m_speed_2)
                distance_2.append(m_lapdistance_2)
                throttle_2.append(m_throttle_2)
                brake_2.append(m_brake_2)
                gear_2.append(m_gear_2)
        # update the dictionary of lap counts
    # print("SPEED",speeds)
    # print("Distance",distance)
    # check if any lap counts have changed

    if lap_counts_1 != m_lapNumber_1:
        print("Last lap time of #1 driver: ",m_timelastlap_1)
        with open('lapdata.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Throttle', 'Speeds', 'Distance','Brake','Gear','Lap'])  # write header
            for i in range(len(distance_1)):
                writer.writerow([throttle_1[i], speeds_1[i], distance_1[i],brake_1[i],gear_1[i],lap_counts_1])

        s3 = boto3.client('s3')
        bucket_name = 'myteamplayer1'
        s3.upload_file('lapdata.csv', bucket_name,'teamlapdata/'+'lapdata.csv')
        speeds_1 = []
        distance_1 = []
        throttle_1 = []
        brake_1 = []
        gear_1=[]
        lap_counts_1 = m_lapNumber_1
        # axspeed_merge.clear()
        # ax_throttle_merge.clear()
        # ax_brake_merge.clear()
        # ax_gear_merge.clear()

    if lap_counts_2 != m_lapNumber_2:
        print("Last lap time of #2 driver: ",m_timelastlap_2)
        with open('lapdata2.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Throttle', 'Speeds', 'Distance','Brake','Gear','Lap'])  # write header
            for i in range(len(distance_2)):
                writer.writerow([throttle_2[i], speeds_2[i], distance_2[i],brake_2[i],gear_2[i],lap_counts_2])

        s3 = boto3.client('s3')
        bucket_name = 'myteamplayer1'
        s3.upload_file('lapdata2.csv', bucket_name,'teamlapdata/'+'lapdata2.csv')
        speeds_2 = []
        distance_2 = []
        throttle_2 = []
        brake_2 = []
        gear_2=[]
        lap_counts_2 = m_lapNumber_2
        # axspeed_merge.clear()
        # ax_throttle_merge.clear()
        # ax_brake_merge.clear()
        # ax_gear_merge.clear()
    # update the plot data
    line.set_xdata(distance_1)
    line.set_ydata(speeds_1)

    line2.set_xdata(distance_1)
    line2.set_ydata(throttle_1)

    line3.set_xdata(distance_1)
    line3.set_ydata(brake_1)

    line7.set_xdata(distance_1)
    line7.set_ydata(gear_1)


    line4.set_xdata(distance_2)
    line4.set_ydata(speeds_2)

    line5.set_xdata(distance_2)
    line5.set_ydata(throttle_2)

    line6.set_xdata(distance_2)
    line6.set_ydata(brake_2)

    line8.set_xdata(distance_2)
    line8.set_ydata(gear_2)

    # axspeed_merge.plot(distance_1, speeds_1, label="Player 1")
    # axspeed_merge.plot(distance_2, speeds_2, label="Player 2")

    # ax_throttle_merge.plot(distance_1, throttle_1, label="Player 1")
    # ax_throttle_merge.plot(distance_2, throttle_2, label="Player 2")

    # ax_brake_merge.plot(distance_1, brake_1, label="Player 1")
    # ax_brake_merge.plot(distance_2, brake_2, label="Player 2")

    # ax_gear_merge.plot(distance_1, gear_1, label="Player 1")
    # ax_gear_merge.plot(distance_2, gear_2, label="Player 2")

    # # update the plot
    plt.draw()
    plt.pause(0.1)

   
