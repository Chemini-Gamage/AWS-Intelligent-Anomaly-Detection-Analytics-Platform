
import os
import json
import uuid
import boto3
from datetime import datetime, timezone
from decimal import Decimal
from ml_service import predict


AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

TABLE_NAME = os.environ["TABLE_NAME"]
BUCKET_NAME = os.environ["BUCKET_NAME"]

table = dynamodb.Table(TABLE_NAME)

def to_decimal(obj):
    """Recursively convert floats to Decimal for DynamoDB compatibility."""
    if isinstance(obj, float):
        return Decimal(str(obj))
    if isinstance(obj, dict):
        return {k: to_decimal(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_decimal(v) for v in obj]
    return obj


def process_event(event):
    device_id = event.get("device_id")
    timestamp = event.get("timestamp")
    temperature = event.get("temperature")
    pressure = event.get("pressure")
    vibration = event.get("vibration")

    if device_id is None:
        raise ValueError("Missing required field: device_id")
    if temperature is None:
        raise ValueError("Missing required field: temperature")
    if pressure is None:
        raise ValueError("Missing required field: pressure")

    prediction = predict(float(temperature), float(pressure))

    event_id = str(uuid.uuid4())
    processed_at = datetime.now(timezone.utc).isoformat()

    # Plain-float record — used for S3 (JSON-serializable)
    record = {
        "id": event_id,
        "device_id": str(device_id),
        "timestamp": str(timestamp) if timestamp else processed_at,
        "temperature": float(temperature),
        "pressure": float(pressure),
        "vibration": float(vibration) if vibration is not None else None,
        "prediction": prediction,
        "processed_at": processed_at
    }

    record = {k: v for k, v in record.items() if v is not None}

    # DynamoDB write — Decimal-converted copy
    table.put_item(Item=to_decimal(record))

    # S3 write — original float-based record
    s3_key = f"sensor-events/{device_id}/{event_id}.json"
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=json.dumps(record).encode("utf-8"),
        ContentType="application/json"
    )

    return {
        "id": event_id,
        "device_id": device_id,
        "prediction": prediction,
        "dynamodb_table": TABLE_NAME,
        "s3_bucket": BUCKET_NAME,
        "s3_key": s3_key
    }


def lambda_handler(event, context):
    """
    Lambda entry point.

    Supports:
    1. Direct Lambda invocation with a sensor event.
    2. SQS event-source mapping.
    """

    print("Received event:")
    print(json.dumps(event))

    # SQS event
    if isinstance(event, dict) and "Records" in event:
        results = []

        for record in event["Records"]:
            body = record.get("body")

            if body is None:
                raise ValueError("SQS record does not contain a body")

            sensor_event = json.loads(body)

            result = process_event(sensor_event)
            results.append(result)

        print("Processed SQS records:")
        print(json.dumps(results))

        return {
            "statusCode": 200,
            "processed": len(results),
            "results": results
        }

    # Direct Lambda invocation
    result = process_event(event)

    print("Processed sensor event:")
    print(json.dumps(result))

    return {
        "statusCode": 200,
        "result": result
    }

