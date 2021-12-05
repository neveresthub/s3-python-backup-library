#!/usr/bin/env python3

import os
import time
import logging
from colors import color
from boto3 import session

from cli_tools import parser
from utils import ProgressPercentage
from config import (ACCESS_ID, SECRET_KEY, SERVICE_NAME, REGION_NAME, ENDPOINT_URL, BUCKET_NAME)

cwd_dir = os.getcwd()
logs_dir = os.path.join(cwd_dir, '.logs')
failed_dir = os.path.join(cwd_dir, '.failed_uploads')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
logging.basicConfig(filename=os.path.join(logs_dir, 'logs.log'),
                    filemode='a', format='%(asctime)s %(levelname)s %(message)s',
                    )
if not os.path.exists(failed_dir):
    os.makedirs(failed_dir)


def log_error(error_file):
    log_file = os.path.join(failed_dir, "%s.txt" % time.strftime("%Y%m%d"))
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


def upload_dir(dirpath, bucket_name=None):
    client = set_client()
    if not os.path.isdir(dirpath):
        raise Exception("Not a Valid Directory :%s" % (dirpath))
    bucket = BUCKET_NAME
    if bucket_name:
        bucket = bucket_name

    file_count = 0
    error_count = 0

    print(color("Initializing ...\n", fg="yellow"))
    for (root, dirs, filenames) in os.walk(top=dirpath, topdown=True):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            base = os.path.basename(filepath.rstrip("/"))

            start,folder=os.path.split(dirpath)
            upload_path = os.path.relpath(filepath, start=start).lstrip("../")

            try:
                print(color("%s \nuploading...\n" % filepath, fg='blue'))
                # print("%s" % upload_path)
                client.upload_file(
                    filepath,
                    bucket,
                    upload_path,
                    ExtraArgs={'ACL': 'public-read'},
                    Callback=ProgressPercentage(filepath)
                )
                print(color("Success\n", fg="lime"))

                file_count += 1
            except Exception as e:
                logging.error('FilePath: %s' % filepath, exc_info=True)
                error_count += 1
                print(color("Error encountered: %s" % e, fg="#ff1a1a"))
                log_error("%s\n" % filepath)
                continue

    print(color("Total number of files uploaded: %d.\n" % file_count, fg="lime"))
    if error_count > 0:
        print(color("Total number of errors encountered: %d." % error_count, fg="#ff1a1a"))
        print(color("Please Check the log file located at .logs in the current working directory", fg='#ff1a1a'))


if __name__ == '__main__':
    args = parser.parse_args()
    root_dir = args.dir
    bucket_name = args.bucket
    upload_dir(root_dir, bucket_name)

# /home/coder/Documents/personal_docs/
