
import boto3
from botocore.exceptions import NoCredentialsError
import configparser
import os
config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '/settings.ini')

ACCESS_KEY = config['AWS']['ACCESS_KEY']
SECRET_KEY = config['AWS']['SECRET_KEY']
BUCKET_NAME = config['AWS']['BUCKET_NAME']


def upload_to_aws(local_file, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, BUCKET_NAME, s3_file,
                       ExtraArgs={'ACL': 'public-read'})
        print("Upload Successful")
        bucket_location = boto3.client(
            's3').get_bucket_location(Bucket=BUCKET_NAME)
        object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
            bucket_location['LocationConstraint'],
            BUCKET_NAME,
            s3_file)

        return object_url
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
