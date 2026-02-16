import os
import boto3
import json
from datetime import datetime, timezone
from urllib.parse import unquote_plus

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


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


# -------------------------------------------------------
# Handler
# -------------------------------------------------------
def lambda_handler(event, context):

    print(json.dumps(event))

    for record in event["Records"]:
        event_name = record["eventName"]
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        parts = key.split("/")
        sha256 = parts[4] if len(parts) >= 5 else None

        if event_name.startswith("ObjectCreated"):

            head = s3.head_object(Bucket=bucket, Key=key)

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

            write_log("OBJECT_CREATED", key, bucket)

        elif event_name.startswith("ObjectRemoved"):

            table.delete_item(
                Key={"PK": "OBJECTS", "SK": key}
            )

            write_log("OBJECT_REMOVED", key, bucket)

    return {"status": "ok"}
