import boto3
import os

sqs = boto3.resource("sqs")
queue_name = "downloadqueue"

s3 = boto3.resource("s3")
bucket_name = "myteamplayer1"
key_1 = "teamlapdata/lapdata.csv"
key_2 = "teamlapdata/lapdata2.csv"
local_filename2 = (
    "D:\\COLLLEGE LECTURE\\MP\\new\\Grande-strategia\\lapdata2.csv".format(
        os.path.basename(key_2)
    )
)
local_filename = "D:\\COLLLEGE LECTURE\\MP\\new\\Grande-strategia\\lapdata.csv".format(
    os.path.basename(key_1)
)
queue = sqs.get_queue_by_name(QueueName=queue_name)

while True:
    messages = queue.receive_messages()

    for message in messages:
        # Download file from S3
        s3.Bucket(bucket_name).download_file(key_2, local_filename2)
        s3.Bucket(bucket_name).download_file(key_1, local_filename)
        # Delete message from SQS queue
        message.delete()
