import boto3
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import InstrumentalUploadForm
from datetime import datetime, timezone
from ulid import ULID
import json
import boto3
from flask import request, jsonify, current_app
from boto3.dynamodb.conditions import Key, Attr
from utils import login_required, is_authorized

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")


uploads_router = Blueprint("uploads", __name__)


@uploads_router.route("/uploads/presign", methods=["POST"])
@login_required
def create_upload():

    payload = InstrumentalUploadForm(**request.json)
    bucket = current_app.config["S3_BUCKET"]

    filename = secure_filename(payload.file_name)

    # Convert timestamp
    ts_ms = int(payload.last_modified)
    dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)

    # Partitioned object key
    object_key = (
        f"instrumentals/"
        f"year/{dt.year}/month/{dt.month:02}/day/{dt.day:02}/"
        f"{str(ULID())}/{filename}"
    )

    # Build metadata fields + conditions
    metadata_fields = {}
    metadata_conditions = []

    for k, v in payload.model_dump(exclude_none=True).items():
        field_name = f"x-amz-meta-{k}"
        metadata_fields[field_name] = str(v)
        metadata_conditions.append({field_name: str(v)})

    presigned = s3.generate_presigned_post(
        Bucket=bucket,
        Key=object_key,
        Fields={
            "Content-Type": payload.content_type,
            **metadata_fields
        },
        Conditions=[
            {"bucket": bucket},
            {"key": object_key},
            ["starts-with", "$Content-Type", "audio/"],
            *metadata_conditions
        ],
        ExpiresIn=3600,
    )

    return jsonify({
        "upload": presigned,
        "key": object_key
    })

@uploads_router.route("/uploads/list", methods=["GET"])
def list_instrumentals():

    table = dynamodb.Table(current_app.config["TABLE_NAME"])

    year = request.args.get("year")
    month = request.args.get("month")
    day = request.args.get("day")

    limit = int(request.args.get("limit", 1000))
    cursor = request.args.get("cursor")

    prefix = "instrumentals/"

    if year:
        prefix += f"year/{year}/"
    if month:
        prefix += f"month/{month:0>2}/"
    if day:
        prefix += f"day/{day:0>2}/"

    query_args = {
        "KeyConditionExpression":
            Key("PK").eq("OBJECTS") &
            Key("SK").begins_with(prefix),
        "Limit": limit,
        "ScanIndexForward": False
    }

    print("IS AUTH", is_authorized())

    # Apply public visibility filter ONLY if user is not authorized
    if not is_authorized():
        query_args["FilterExpression"] = Attr("visibility").eq(True)

    if cursor:
        query_args["ExclusiveStartKey"] = json.loads(cursor)

    resp = table.query(**query_args)

    return jsonify({
        "items": resp.get("Items", []),
        "cursor": json.dumps(resp.get("LastEvaluatedKey"))
            if "LastEvaluatedKey" in resp else None
    })


@uploads_router.route("/uploads/toggle-visibility", methods=["PATCH"])
@login_required
def toggle_visibility():

    table = dynamodb.Table(current_app.config["TABLE_NAME"])

    key = request.json.get("key")

    if not key:
        return jsonify({"error": "missing key"}), 400

    # ---- get current value ----
    item = table.get_item(
        Key={
            "PK": "OBJECTS",
            "SK": key
        }
    ).get("Item")

    current = item.get("visibility", False) if item else False

    # ---- update opposite ----
    resp = table.update_item(
        Key={
            "PK": "OBJECTS",
            "SK": key
        },
        UpdateExpression="SET visibility = :v",
        ExpressionAttributeValues={
            ":v": not current
        },
        ReturnValues="ALL_NEW"
    )

    return jsonify({
        "item": resp.get("Attributes")
    })


@uploads_router.route("/uploads/presign-get", methods=["GET"])
def presign_get():

    bucket = current_app.config["S3_BUCKET"]

    # SK from DynamoDB item (the S3 object key)
    key = request.args.get("key")
    if not key:
        return jsonify({"error": "missing key"}), 400

    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": bucket,
            "Key": key
        },
        ExpiresIn=3600  # seconds
    )

    return jsonify({
        "url": url,
        "key": key
    })
