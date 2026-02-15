import os
import boto3
import json
import hashlib
from datetime import datetime, timezone
from urllib.parse import unquote_plus

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


# -------------------------------------------------------
# Stream SHA256
# -------------------------------------------------------
def compute_sha256(bucket, key, chunk_size=1024 * 1024):
    sha = hashlib.sha256()
    obj = s3.get_object(Bucket=bucket, Key=key)

    while True:
        chunk = obj["Body"].read(chunk_size)
        if not chunk:
            break
        sha.update(chunk)

    return sha.hexdigest()


# -------------------------------------------------------
# Write audit log
# -------------------------------------------------------
def write_log(action, key, bucket, extra=None):
    ts = datetime.now(timezone.utc).isoformat()

    item = {
        "PK": "LOG#OBJECTS",
        "SK": f"{ts}#{key}",
        "action": action,
        "key": key,
        "bucket": bucket,
        "timestamp": ts
    }

    if extra:
        item.update(extra)

    table.put_item(Item=item)


def lambda_handler(event, context):

    print(json.dumps(event))

    for record in event["Records"]:
        event_name = record["eventName"]
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        if event_name.startswith("ObjectCreated"):

            head = s3.head_object(Bucket=bucket, Key=key)

            sha256 = compute_sha256(bucket, key)

            # ---- check duplicate hash
            dup = table.query(
                IndexName="sha256-index",   # your GSI
                KeyConditionExpression="sha256 = :h",
                ExpressionAttributeValues={":h": sha256},
                Limit=1
            )

            exists = dup.get("Count", 0) > 0

            table.put_item(
                Item={
                    "PK": "OBJECTS",
                    "SK": key,
                    "bucket": bucket,
                    "status": "CREATED",
                    "size": head["ContentLength"],
                    "etag": head["ETag"],
                    "sha256": sha256,
                    "content_type": head.get("ContentType"),
                    "last_modified": head["LastModified"].isoformat(),
                    "metadata": head.get("Metadata", {}),
                }
            )

            if exists:
                write_log("DUPLICATE_HASH", key, bucket, {"sha256": sha256})
            else:
                write_log("OBJECT_CREATED", key, bucket, {"sha256": sha256})

        elif event_name.startswith("ObjectRemoved"):

            table.delete_item(
                Key={"PK": "OBJECTS", "SK": key}
            )

            write_log("OBJECT_REMOVED", key, bucket)

    return {"status": "ok"}
