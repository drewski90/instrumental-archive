import boto3
from os import environ

s3 = boto3.client("s3")

BUCKET = environ['S3_BUCKET']

paginator = s3.get_paginator("list_objects_v2")

for page in paginator.paginate(Bucket=BUCKET):
    for obj in page.get("Contents", []):
        key = obj["Key"]

        print("Reprocessing:", key)

        s3.copy_object(
            Bucket=BUCKET,
            CopySource={"Bucket": BUCKET, "Key": key},
            Key=key,
            MetadataDirective="COPY"  # keeps metadata unchanged
        )

print("Done.")
