#!/usr/bin/env python3

import os
import sys
import json
import time
import logging
import threading
from colors import color
from boto3 import session


cwd_dir = os.getcwd()
logs_dir = os.path.join(cwd_dir, '.logs')
failed_dir = os.path.join(cwd_dir, '.failed_uploads')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
logging.basicConfig(filename=os.path.join(logs_dir,'logs.log'), 
		filemode='a',format='%(asctime)s %(levelname)s %(message)s',
	)
if not os.path.exists(failed_dir):
	os.makedirs(failed_dir)

ACCESS_ID = 'UUPDEEZUH4DSX2ZTWKBR'
SECRET_KEY = 'Vt/BRMzJAeKXZ+SAy/Udcuj3c5JRo7ZRtvYg2XW5KHA'

SERVICE_NAME = 's3'
REGION_NAME = 'sfo2'
ENDPOINT_URL = 'https://example-api.sfo2.digitaloceanspaces.com'
BUCKET_NAME = "backup"

class ProgressPercentage(object):

	def __init__(self, filename):
		self._filename = filename
		self._size = float(os.path.getsize(filename))
		self._seen_so_far = 0
		self._lock = threading.Lock()

	def __call__(self, bytes_amount):
		# To simplify, assume this is hooked up to a single filename
		with self._lock:
			self._seen_so_far += bytes_amount
			percentage = (self._seen_so_far / self._size) * 100
			sys.stdout.write(
				"\r%s / %s  (%.2f%%)\n" % (
					self._seen_so_far, self._size,
					percentage
				)
			)
			sys.stdout.flush()

def log_error(error_file):
	log_file = os.path.join(failed_dir,"%s.txt"%time.strftime("%Y%m%d"))
	if not os.path.exists(log_file):
		with open(log_file, 'w'):
			pass	

	with open(log_file, 'a') as f:
		f.write(error_file)

# Initiate session
session = session.Session()

def set_client():
	client = session.client(
		service_name=SERVICE_NAME,
		region_name=REGION_NAME,
		endpoint_url=ENDPOINT_URL,
		aws_access_key_id=ACCESS_ID,
		aws_secret_access_key=SECRET_KEY
	)
	return client

def upload_dir(dirpath):
	client = set_client()
	if not os.path.isdir(dirpath):
		raise Exception("Not a Valid Directory :%s" % (dirpath))
	file_count = 0
	error_count = 0
	print(color("Initializing ...\n",fg="yellow"))
	for (root, dirs, filenames) in os.walk(top=dirpath, topdown=True):
		for filename in filenames:
			filepath = os.path.join(root, filename)
			try:
				print(color("%s \nuploading...\n"%filepath,fg='blue'))
				client.upload_file(filepath, BUCKET_NAME ,os.path.abspath(filepath) ,Callback=ProgressPercentage(filepath))
				print(color("Success\n",fg="lime"))
				file_count += 1
			except Exception as e:
				logging.error('FilePath: %s' % filepath, exc_info=True)
				error_count += 1
				print(color("Error encountered: %s"%e,fg="#ff1a1a"))
				log_error("%s\n"%filepath)
				continue
	
	print(color("Total number of files uploaded: %d.\n" % file_count,fg="lime"))	
	print(color("Total number of errors encountered: %d." % error_count,fg="#ff1a1a"))
	if error_count > 1:
		print(color("Please Check the log file located at .logs in the current working directory",fg='#ff1a1a'))

if __name__ == '__main__':
	upload_dir("/home/coder/Documents/")
