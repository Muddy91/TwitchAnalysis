"""
    This script is a set of helper functions to make uploads from chats to our S3 bucket easy.
"""
import threading
import boto3
import time
import sys
_lock = threading.Lock()
_s3 = boto3.resource('s3')
_bucket = _s3.Bucket('twitch-brede')
file_list = []

# Function to upload a file from a given filepath
def upload_file(file_path):
    f = open(file_path, 'rb')
    _lock.acquire()
    _bucket.put_object(Key=file_path.split('/')[-1], Body=f)
    _lock.release()

