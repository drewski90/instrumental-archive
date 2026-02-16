import os
import boto3
import hashlib
import logging
from urllib.parse import unquote_plus
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key

# ---------- logging ----------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

UPLOAD_BUCKET = os.environ["UPLOAD_BUCKET"]
STORAGE_BUCKET = os.environ["STORAGE_BUCKET"]


def compute_sha256(bucket, key):
    sha = hashlib.sha256()
    obj = s3.get_object(Bucket=bucket, Key=key)

    for chunk in iter(lambda: obj["Body"].read(1024 * 1024), b""):
        sha.update(chunk)

    digest = sha.hexdigest()
    logger.info(f"sha256 computed key={key} sha256={digest}")
    return digest


def parse_last_modified(metadata, s3_last_modified):
    lm = metadata.get("last_modified")

    if lm:
        try:
            dt = datetime.fromtimestamp(int(lm) / 1000, tz=timezone.utc)
            logger.info(f"last_modified parsed epoch_ms value={lm}")
        except Exception:
            try:
                dt = datetime.fromisoformat(lm.replace("Z", "+00:00"))
                logger.info(f"last_modified parsed iso value={lm}")
            except Exception:
                logger.warning(f"last_modified invalid fallback_to_s3 value={lm}")
                dt = s3_last_modified
    else:
        logger.info("last_modified missing fallback_to_s3")
        dt = s3_last_modified

    dt = dt.astimezone(timezone.utc)
    metadata["last_modified"] = dt.isoformat()

    return dt, metadata


def lambda_handler(event, context):

    logger.info(f"records_received={len(event['Records'])}")

    for record in event["Records"]:

        key = unquote_plus(record["s3"]["object"]["key"])
        logger.info(f"processing_object key={key}")

        head = s3.head_object(Bucket=UPLOAD_BUCKET, Key=key)
        metadata = head.get("Metadata", {})

        file_category = metadata.get("file_category", 'instrumentals')
        filename = metadata.get("file_name") or key.split("/")[-1]

        last_modified_dt, metadata = parse_last_modified(
            metadata,
            head["LastModified"]
        )

        sha256 = compute_sha256(UPLOAD_BUCKET, key)

        # duplicate check
        resp = table.query(
            IndexName="sha256-index",
            KeyConditionExpression=Key("sha256").eq(sha256),
            Limit=1
        )

        if resp["Count"] > 0:
            logger.warning(f"duplicate_detected key={key} sha256={sha256}")
            s3.delete_object(Bucket=UPLOAD_BUCKET, Key=key)
            logger.info(f"staging_deleted_duplicate key={key}")
            continue

        permanent_key = (
            f"{file_category}/"
            f"{last_modified_dt:%Y/%m/%d}/"
            f"{sha256}/{filename}"
        )

        logger.info(
            f"copying_object src={key} dest={permanent_key} sha256={sha256}"
        )

        s3.copy_object(
            Bucket=STORAGE_BUCKET,
            CopySource={"Bucket": UPLOAD_BUCKET, "Key": key},
            Key=permanent_key,
            Metadata=metadata,
            MetadataDirective="REPLACE",
            ContentType=head.get("ContentType")
        )

        s3.delete_object(Bucket=UPLOAD_BUCKET, Key=key)

        logger.info(
            f"object_ingested key={key} permanent_key={permanent_key}"
        )

    return {"status": "ok"}
