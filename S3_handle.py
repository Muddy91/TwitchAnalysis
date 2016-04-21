"""
    This script is a set of helper functions to make uploads from chats to our S3 bucket easy.
"""
import threading
import boto3
import time
import sys
import os
_lock = threading.Lock()
_s3 = boto3.resource('s3')
_bucket = _s3.Bucket('twitch-brede')
file_list = []

# Function to upload a file from a given file path
def upload_file(file_path):
    # Abort if we try to upload empty file!
    if os.path.getsize(file_path) <= 0:
        return
    date_suffix = '_' + time.strftime("%d%m%y")
    f = open(file_path, 'rb')
    fr = open(file_path+"_raw", 'rb')
    splits = file_path.split('/')
    raw_path = "raw/" + splits[1:]
    _lock.acquire()
    _bucket.put_object(Key=f.name+date_suffix, Body=f)
    _bucket.put_object(Key=raw_path+date_suffix, Body=fr)
    _lock.release()
    f.close()

