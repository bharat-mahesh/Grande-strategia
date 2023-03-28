import boto3
import matplotlib.pyplot as plt
import json

client = boto3.client('kinesis')
stream_name = 'grande-strategia'

shard_iterator = client.get_shard_iterator(
    StreamName=stream_name,
    ShardId='shardId-000000000000',  # replace with the ID of your shard
    ShardIteratorType='TRIM_HORIZON'
)['ShardIterator']

response = client.get_records(
    ShardIterator=shard_iterator
)

# print(response["Records"])
# print(response)
data = []
speed=[]
time=[]
counter=0
for record in response['Records']:
    data_str = record["Data"].decode('utf-8')  # decode byte string to regular string
    data_obj = json.loads(data_str)  # load string as a JSON object
    m_speed = data_obj['m_speed']  # access value of 'm_speed'
    speed.append(m_speed)  # print the value of 'm_speed'
    counter+=1
    time.append(counter)
    # data.append(float(record['Data']))

plt.plot(time,speed)
plt.title('Histogram of Data from Kinesis Stream')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
