import requests
import random
import time
import uuid
from datetime import datetime


API_URL = "http://127.0.0.1:8000/events"


DEVICE_ID = str(uuid.uuid4())



def generate_sensor_data():

    """
    Simulates an IoT temperature sensor
    """

    if random.random() < 0.95:

        temperature = random.gauss(
            35,
            3
        )

        pressure = random.gauss(
            1010,
            5
        )

        vibration = random.gauss(
            2,
            0.5
        )


    else:

        # Simulated equipment failure

        temperature = random.uniform(
            80,
            130
        )

        pressure = random.uniform(
            700,
            850
        )

        vibration = random.uniform(
            8,
            15
        )


    return {

        "device_id": DEVICE_ID,

        "timestamp":
        datetime.utcnow().isoformat(),

        "temperature":
        temperature,

        "pressure":
        pressure,

        "vibration":
        vibration

    }




while True:


    sensor_data = generate_sensor_data()


    try:

        response = requests.post(
            API_URL,
            json=sensor_data
        )


        print(
            "Sent:",
            sensor_data
        )


        print(
            "Response:",
            response.json()
        )


    except Exception as e:

        print(
            "Error:",
            e
        )


    time.sleep(5)