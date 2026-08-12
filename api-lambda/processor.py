import os
import json
import boto3
from decimal import Decimal


TABLE_NAME = os.environ["TABLE_NAME"]
AWS_REGION = os.environ.get("AWS_REGION", "eu-north-1")


dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

table = dynamodb.Table(TABLE_NAME)


def decimal_to_number(value):
    """
    Convert DynamoDB Decimal values into JSON-compatible numbers.
    """

    if isinstance(value, Decimal):

        if value % 1 == 0:
            return int(value)

        return float(value)

    return value


def clean_item(item):

    return {
        key: decimal_to_number(value)
        for key, value in item.items()
    }


def response(status_code, body):

    return {
        "statusCode": status_code,

        "headers": {
            "Content-Type": "application/json"
        },

        "body": json.dumps(body)
    }


def get_events(limit=50):

    result = table.scan(
        Limit=limit
    )

    items = result.get(
        "Items",
        []
    )

    return [
        clean_item(item)
        for item in items
    ]


def get_statistics():

    result = table.scan(
        Select="COUNT"
    )

    total = result.get(
        "Count",
        0
    )

    anomaly_result = table.scan(
        FilterExpression="#status = :anomaly",
        ExpressionAttributeNames={
            "#status": "status"
        },
        ExpressionAttributeValues={
            ":anomaly": "ANOMALY"
        },
        Select="COUNT"
    )

    anomalies = anomaly_result.get(
        "Count",
        0
    )

    normal = total - anomalies

    anomaly_rate = (
        (anomalies / total) * 100
        if total > 0
        else 0
    )

    return {
        "total_events": total,
        "normal_events": normal,
        "anomalies": anomalies,
        "anomaly_rate": round(
            anomaly_rate,
            2
        )
    }

def lambda_handler(event, context):

    print("API Event:")
    print(json.dumps(event))

    path = event.get(
        "rawPath",
        "/"
    )

    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", "GET")
    )

    try:

        if method == "GET" and path == "/events":

            events = get_events()

            return response(
                200,
                events
            )

        if method == "GET" and path == "/statistics":

            statistics = get_statistics()

            return response(
                200,
                statistics
            )

        if method == "GET" and path == "/health":

            return response(
                200,
                {
                    "status": "healthy",
                    "service": "sensor-api"
                }
            )

        return response(
            404,
            {
                "error": "Route not found"
            }
        )

    except Exception as error:

        print(
            f"API Error: {error}"
        )

        return response(
            500,
            {
                "error": "Internal server error"
            }
        )