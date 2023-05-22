import schedule
import time
import boto3
from datetime import datetime, timedelta
import os


print("Starting AWS S3 file deletion scheduler")

# Load the environment variables

# Get the AWS S3 server info and a list of buckets from the environment variables
url = os.environ.get('SERVER_URL')
buckets = os.environ.get('BUCKETS').split(',')

# Get the AWS S3 access key and secret key from the environment variables
access_key = os.environ.get('ACCESS_KEY')
secret_key = os.environ.get('SECRET_KEY')

# Get the AWS S3 region from the environment variables
region = os.environ.get('REGION')

# Get the amount of days to keep the files from the environment variables
days = int(os.environ.get('DELETE_AFTER_DAYS'))


def job():
    # Create an S3 client using the access key, secret key, and region
    print("Connecting to {} AWS S3 server".format(url))
    s3_client = boto3.client('s3', endpoint_url=url, aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region)

    # Loop through the buckets
    for bucket in buckets:
        print("Checking {} bucket".format(bucket))
        # List all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket)
        if 'Contents' in response:
            for obj in response['Contents']:
                # Get the last modified timestamp of the object
                last_modified = obj['LastModified'].replace(tzinfo=None)

                # Calculate the difference between the current date and the last modified date
                difference = datetime.now() - last_modified

                # Check if the difference is greater than the specified number of days
                if difference > timedelta(days=days):
                    # Delete the object
                    print("Deleting {} from AWS S3".format(obj['Key']))
                    s3_client.delete_object(Bucket=bucket, Key=obj['Key'])

    print("Files older than {} days have been deleted from AWS S3".format(days))


schedule.every(12).hours.do(job)

print("Running the job now before starting the scheduler")
job()

print("Scheduler started! Deleting files older than {} days from AWS S3 every 12 hours.".format(days))

while True:
    schedule.run_pending()
    time.sleep(1)
