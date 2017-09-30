"""
    This script is a set of helper functions to make gz archives from ended sessions.
"""
import threading
import boto3
import time
import sys
import os
import gzip
import shutil
_lock = threading.Lock()
_s3 = boto3.resource('s3')
_bucket = _s3.Bucket('twitch-brede')
file_list = []

def create_archive(chan_list, archive_name):
  parse_archive = gzip.open('data/'+archive_name, 'wb')
  raw_archive = gzip.open('data/'+archive_name+'_raw', 'wb')
  for c_name in chan_list:
    f_parsed = open('data/'+c_name, 'rb')
    shutil.copyfileobj(f_parsed, parse_archive)
    f_parsed.close()
    f_raw = open('data/'+c_name+'_raw', 'rb')
    shutil.copyfileobj(f_raw, raw_archive)
    f_raw.close()

def upload_archive(archive_path):
  date_suffix = '_' + time.strftime("%d%m%y%H")
  f = open(archive_path, 'rb')
  fr = open(archive_path+'_raw', 'rb')
  path_splits = archive_path.split('/')
  raw_path = 'raw/' + ''.join(splits[1:])
  _lock.acquire()
  _bucket.put_object(Key=f.name+date_suffix, Body=f)
  _bucket.put_object(Key=raw_path+date_suffix, Body=fr)
  _lock.release()
  f.close()
  fr.close()

