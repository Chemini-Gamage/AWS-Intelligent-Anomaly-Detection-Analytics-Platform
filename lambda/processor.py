import os
import json
import uuid
import boto3

from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
from dotenv import load_dotenv

from ml_service import predict_anomaly
AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")

load_dotenv(Path(__file__).resolve().parent / ".env")
# AWS clients
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
    """
    Recursively convert floats to Decimal
    for DynamoDB compatibility.
    """

    if isinstance(obj, float):
        return Decimal(str(obj))

    if isinstance(obj, dict):
        return {
            k: to_decimal(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):
        return [
            to_decimal(v)
            for v in obj
        ]

    return obj


def process_event(event):
    """
    Process one sensor event.

    Performs:
    1. Input validation
    2. ML anomaly prediction
    3. DynamoDB storage
    4. S3 storage
    """

    device_id = event.get("device_id")
    timestamp = event.get("timestamp")
    temperature = event.get("temperature")
    pressure = event.get("pressure")
    vibration = event.get("vibration")


    # -----------------------------------------
    # Validate required fields
    # -----------------------------------------

    if device_id is None:
        raise ValueError("Missing required field: device_id")

    if temperature is None:
        raise ValueError("Missing required field: temperature")

    if pressure is None:
        raise ValueError("Missing required field: pressure")

    if vibration is None:
        raise ValueError("Missing required field: vibration")


    # -----------------------------------------
    # ML anomaly prediction
    # -----------------------------------------

    prediction = predict_anomaly(
    float(temperature),
    float(pressure),
    float(vibration) if vibration is not None else 0.0
)
    print(f"prediction: {prediction}")


    # -----------------------------------------
    # Generate event information
    # -----------------------------------------

    event_id = str(uuid.uuid4())

    processed_at = datetime.now(
        timezone.utc
    ).isoformat()


    # -----------------------------------------
    # Create sensor record
    # -----------------------------------------

    record = {
        "id": event_id,
        "device_id": str(device_id),
        "timestamp": (
            str(timestamp)
            if timestamp
            else processed_at
        ),
        "temperature": float(temperature),
        "pressure": float(pressure),
        "vibration": float(vibration),
        "prediction": prediction,
        "processed_at": processed_at
    }


    # -----------------------------------------
    # DynamoDB
    # -----------------------------------------

    dynamodb_record = to_decimal(record)

    table.put_item(
        Item=dynamodb_record
    )

    print(
        f"DynamoDB write successful: "
        f"{TABLE_NAME}"
    )


    # -----------------------------------------
    # S3
    # -----------------------------------------

    s3_key = (
        f"sensor-events/"
        f"{device_id}/"
        f"{event_id}.json"
    )

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=json.dumps(record).encode("utf-8"),
        ContentType="application/json"
    )

    print(
        f"S3 write successful: "
        f"s3://{BUCKET_NAME}/{s3_key}"
    )


    # -----------------------------------------
    # Return result
    # -----------------------------------------

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

    1. Direct Lambda invocation
    2. SQS event-source mapping
    """

    print("Received event:")

    print(
        json.dumps(
            event,
            default=str
        )
    )


    # =========================================
    # SQS EVENT
    # =========================================

    if (
        isinstance(event, dict)
        and "Records" in event
    ):

        results = []

        for record in event["Records"]:

            body = record.get("body")

            if body is None:
                raise ValueError(
                    "SQS record does not contain a body"
                )

            sensor_event = json.loads(body)

            result = process_event(
                sensor_event
            )

            results.append(result)


        print("Processed SQS records:")

        print(
            json.dumps(
                results,
                default=str
            )
        )


        return {
            "statusCode": 200,
            "processed": len(results),
            "results": results
        }


    # =========================================
    # DIRECT LAMBDA INVOCATION
    # =========================================

    result = process_event(event)


    print("Processed sensor event:")

    print(
        json.dumps(
            result,
            default=str
        )
    )


    return {
        "statusCode": 200,
        "result": result
    }