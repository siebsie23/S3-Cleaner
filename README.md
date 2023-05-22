# S3-Deleter
Docker image that automatically deletes old files from S3 buckets. Useful for unofficial S3 servers that don't support lifecycle policies or object expiration.

## Usage
The image is available on the GitHub Container Registry:
```
ghcr.io/siebsie23/s3-deleter:latest
```

To run the image you must provide the following environment variables:
```yaml
SERVER_URL: The URL of the S3 server
ACCESS_KEY: The access key for the S3 server
SECRET_KEY: The secret key for the S3 server
REGION: The region of the S3 server
DELETE_AFTER_DAYS: The number of days after which files should be deleted
BUCKETS: A comma-separated list of buckets to delete files from
```

You can also run the image from a docker-compose file an example of which is provided below:
```yaml
version: '3'
services:
  autodelete:
    image: ghcr.io/siebsie23/s3-deleter:latest
    environment:
      SERVER_URL: https://eu2.contabostorage.com
      ACCESS_KEY: 1234567890
      SECRET_KEY: 1234567890
      REGION: eu-central-1
      DELETE_AFTER_DAYS: 10
      BUCKETS: bucket1,bucket2,bucket3
```

A full list of regions can be found here:
https://docs.aws.amazon.com/general/latest/gr/s3.html

## Building
To build the image yourself you can clone the repository locally and use the following command:
```
docker build -t s3-deleter .
```

## Future Plans
- Add support for multiple servers

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
