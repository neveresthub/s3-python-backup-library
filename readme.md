# S3 backup library

## How to use
- Create a configuration file `config.py` in the root directory with the folowing structure
```
ACCESS_ID=''
SECRET_KEY=''
SERVICE_NAME=''
REGION_NAME=''
ENDPOINT_URL=''
BUCKET_NAME='

```

- Install all python requirements from the  `requirements.txt` file

- upload a folder like this

```
python spaces.py -d=/path/to/folder/file/to/upload -b=bucketname

