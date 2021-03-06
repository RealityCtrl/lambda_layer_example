import boto3
import os
import json

SQS_CLIENT = boto3.client('sqs')

queue_name = os.environ['QName']
max_messages = int(os.environ['max_messages'])
wait_time = int(os.environ['wait_time'])
queue = SQS_CLIENT.get_queue_by_name(QueueName=queue_name)

def get_file_list_with_location():
    messages = poll_for_messages(max_messages, wait_time)
    return parse_message_contents(messages)


def poll_for_messages(max_messages=10, wait_time=20):
    return queue.receive_messages(
        AttributeNames = ["ALL"],
        MaxNumberOfMessages = max_messages,
        WaitTimeSeconds = wait_time
    )

def parse_message_contents(sqs_messages):
    output = []
    for message in sqs_messages:
        message_output = parse_message(message)
        output.append(message_output)
    return output

def parse_message(message):
    message_output = dict()
    message_output["Id"] = message.receipt_handle
    message_body = json.loads(message.body)
    message_output["Bucket"] = message_body["records"][0]["S3"]["bucket"]["name"]
    message_output["Key"] = message_body["records"][0]["S3"]["object"]["key"]
    return message_output


