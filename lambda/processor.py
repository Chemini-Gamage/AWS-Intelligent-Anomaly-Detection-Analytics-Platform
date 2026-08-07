import json
import boto3
from datetime import datetime

from ml_service import predict


s3 = boto3.client("s3")

dynamodb = boto3.resource(
    "dynamodb"
)


TABLE_NAME = "sensor-events"

BUCKET_NAME = "YOUR_BUCKET_NAME"


table = dynamodb.Table(
    TABLE_NAME
)



def lambda_handler(event, context):


    for record in event["Records"]:


        body = json.loads(
            record["body"]
        )


        temperature = body["temperature"]

        pressure = body["pressure"]


        status = predict(
            temperature,
            pressure
        )


        processed_event = {


            "id":
            body["device_id"],


            "timestamp":
            body["timestamp"],


            "temperature":
            str(temperature),


            "pressure":
            str(pressure),


            "vibration":
            str(body["vibration"]),


            "status":
            status

        }


        # Save to DynamoDB

        table.put_item(
            Item=processed_event
        )


        # Save raw event to S3

        s3.put_object(

            Bucket=BUCKET_NAME,

            Key=f"raw/{datetime.utcnow()}.json",

            Body=json.dumps(body)

        )


    return {

        "statusCode":200,

        "body":"Processed successfully"

    }