from concurrent.futures import ThreadPoolExecutor
import boto3
import os
import json
from worker import process_file

# SQS client
sqs = boto3.client(
    'sqs',
    endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"),
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

def poll_sqs(queue_url, max_workers=4):
    """Poll SQS messages and process them concurrently."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,  # Fetch up to 10 messages at a time
                WaitTimeSeconds=5  # Long polling
            )
            if 'Messages' in response:
                for message in response['Messages']:
                    # Submit each message to a worker thread
                    executor.submit(handle_message, message, queue_url)

def handle_message(message, queue_url):
    """Handle individual SQS messages."""
    try:
        # Extract and validate the message body
        body = json.loads(message['Body'])
        bucket_name = body.get('bucket_name')
        file_key = body.get('file_key')

        if not bucket_name or not file_key:
            raise ValueError("Message missing 'bucket_name' or 'file_key'")

        # Process the file
        process_file(bucket_name, file_key)

    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        # Ensure the message is deleted from the queue
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
        print(f"Deleted message: {message['MessageId']}")

if __name__ == "__main__":
    queue_url = os.getenv("SQS_QUEUE_URL", "http://localhost:4566/000000000000/my-queue")
    poll_sqs(queue_url, max_workers=4)  # Adjust max_workers for concurrency