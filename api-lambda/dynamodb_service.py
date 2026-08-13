import os
import boto3

TABLE_NAME = os.getenv("DYNAMODB_TABLE", "sensor-events")
REGION = os.getenv("AWS_REGION", "eu-north-1")

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION
)

table = dynamodb.Table(TABLE_NAME)


def get_all_events():
    items = []

    response = table.scan()
    items.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"]
        )
        items.extend(response.get("Items", []))

    return items


def get_statistics():
    events = get_all_events()

    total = len(events)

    anomalies = sum(
        1
        for event in events
        if event.get("prediction") == "ANOMALY"
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
        "anomaly_rate": round(anomaly_rate, 2)
    }