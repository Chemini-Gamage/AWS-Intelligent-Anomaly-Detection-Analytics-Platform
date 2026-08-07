import boto3
import json
import random
import time
import uuid
import os

from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


QUEUE_URL = os.getenv("SQS_QUEUE_URL")

AWS_REGION = os.getenv("AWS_REGION")


if not QUEUE_URL:
    raise Exception("Missing SQS_QUEUE_URL")


sqs = boto3.client(
    "sqs",
    region_name=AWS_REGION
)


DEVICE_ID = str(uuid.uuid4())



def generate_sensor_data():

    if random.random() < 0.95:

        temperature = random.gauss(35,3)

        pressure = random.gauss(1010,5)

        vibration = random.gauss(2,0.5)


    else:

        temperature = random.uniform(80,130)

        pressure = random.uniform(700,850)

        vibration = random.uniform(8,15)


    return {

        "device_id": DEVICE_ID,

        "timestamp":
        datetime.utcnow().isoformat(),

        "temperature": round(temperature,2),

        "pressure": round(pressure,2),

        "vibration": round(vibration,2)

    }



while True:


    event = generate_sensor_data()


    response = sqs.send_message(

        QueueUrl=QUEUE_URL,

        MessageBody=json.dumps(event)

    )


    print(
        "Sent to SQS:",
        event
    )


    time.sleep(5)