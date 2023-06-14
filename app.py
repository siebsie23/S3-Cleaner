""" This is the main script, it will be run by the Docker
container and will delete the files from the AWS S3 server """
import time
import os
from datetime import datetime, timedelta
import schedule
import boto3


print("Starting AWS S3 file deletion scheduler")

# Load the environment variables

# Get the AWS S3 server info and a list of buckets from the environment variables
url = os.environ.get("SERVER_URL")
buckets = os.environ.get("BUCKETS").split(",")

# Get the AWS S3 access key and secret key from the environment variables
access_key = os.environ.get("ACCESS_KEY")
secret_key = os.environ.get("SECRET_KEY")

# Get the AWS S3 region from the environment variables
region = os.environ.get("REGION")

# Get the amount of days to keep the files from the environment variables
days = int(os.environ.get("DELETE_AFTER_DAYS"))

# Get if the files should be force deleted from the environment variables
force_delete = os.environ.get("FORCE_DELETE")

# Get the hour period to run the job from the environment variables
hour_period = int(os.environ.get("HOUR_PERIOD"))


def job() -> None:
    """ This is the main job that will be run by the scheduler,
    it loops trough the buckets and deletes the files that are older than the
    specified amount of days from the environment variables """
    # Create an S3 client using the access key, secret key, and region
    print(f"Connecting to {url} AWS S3 server")
    s3_client = boto3.client(
        "s3", endpoint_url=url, aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region
    )

    # Loop through the buckets
    for bucket in buckets:
        print(f"Checking {bucket} bucket")
        # List all objects in the bucket
        response = s3_client.list_objects_v2(Bucket=bucket)
        if "Contents" in response:
            for obj in response["Contents"]:
                # Get the last modified timestamp of the object
                last_modified = obj["LastModified"].replace(tzinfo=None)

                # Calculate the difference between the current date and the last modified date
                difference = datetime.now() - last_modified

                # Check if the difference is greater than the specified number of days
                if difference > timedelta(days=days):
                    # Delete the object
                    print(f"Deleting {obj['Key']} from AWS S3")
                    # Check if the file should be force deleted
                    if force_delete == "true":
                        # Force delete the file, skipping the versioning
                        s3_client.delete_object(Bucket=bucket, Key=obj["Key"], BypassGovernanceRetention=True)
                    else:
                        s3_client.delete_object(Bucket=bucket, Key=obj["Key"])

    print(f"Files older than {days} days have been deleted from AWS S3")


schedule.every(hour_period).hours.do(job)

print("Running the job now before starting the scheduler")
job()

print(f"""Scheduler started! Deleting files older than {days} days from AWS S3
       every {hour_period} hours.""")

while True:
    schedule.run_pending()
    time.sleep(1)
