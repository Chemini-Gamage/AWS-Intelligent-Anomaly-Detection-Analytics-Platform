import json
import random
import uuid
import os

import boto3
from datetime import datetime, timezone


sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION", "eu-north-1")
)

QUEUE_URL = os.environ["SQS_QUEUE_URL"]

DEVICE_ID = str(uuid.uuid4())


def generate_sensor_data():

    if random.random() < 0.95:

        temperature = random.gauss(35, 3)
        pressure = random.gauss(1010, 5)
        vibration = random.gauss(2, 0.5)

    else:

        temperature = random.uniform(80, 130)
        pressure = random.uniform(700, 850)
        vibration = random.uniform(8, 15)

    return {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": round(temperature, 2),
        "pressure": round(pressure, 2),
        "vibration": round(vibration, 2)
    }


def lambda_handler(event, context):

    sensor_data = generate_sensor_data()

    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(sensor_data)
    )

    print("Sensor event sent:", sensor_data)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Sensor event generated",
            "sensor_data": sensor_data,
            "message_id": response["MessageId"]
        })
    }