from faker import Faker
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from azure.eventhub.exceptions import EventHubError
import random
import asyncio
import generate.api_medicines as medicines
import datetime
import json
import os
from dotenv import load_dotenv


load_dotenv()
conn_str = os.getenv("CONN_EVENTHUB_NAMESPACE")
event_hub_name = os.getenv("EVENTHUB_TOPIC")

f = Faker()

list_ndc = medicines.product_ndc


def stream_distribution(qty_patients: int) -> str:

    list_id_patient = range(1, qty_patients)

    rd_id_patient = random.choice(list_id_patient)
    rd_ndc = random.choice(list_ndc)
    rd_qty = random.randint(1, 10)

    # Dates
    now = datetime.datetime.now()
    format_date = "%Y-%m-%d"
    date_today = now.strftime(format_date)
    qty_days = random.randint(1, 1050)
    others_dates = datetime.date(
        2020, 1, 1) + datetime.timedelta(days=qty_days, hours=0, minutes=0, seconds=0)
    pick_dates = random.choice(
        [others_dates.strftime(format_date), date_today])

    return {"id_patient": rd_id_patient, "ndc": rd_ndc, "qty": rd_qty,  "date_distribution": pick_dates}


def run_streaming(qty_patients: int, min_to_run: int = 1):

    async def run():
        # Create a producer client to send messages to the event hub.
        # Specify a connection string to your event hubs namespace and
        # the event hub name.

        min = datetime.timedelta(minutes=min_to_run)
        start_time = datetime.datetime.today()
        end_time = datetime.datetime.today() + min

        print(f"It will run during {min_to_run} min")
        while end_time >= datetime.datetime.today():

            await asyncio.sleep(2)

            producer = EventHubProducerClient.from_connection_string(
                conn_str=conn_str, eventhub_name=event_hub_name)
            async with producer:
                # Create a batch.
                event_data_batch = await producer.create_batch()

                streaming_medicines = stream_distribution(qty_patients)

                # Add events to the batch.
                event_data_batch.add(
                    EventData(json.dumps(streaming_medicines)))

                # Send the batch of events to the event hub.
                await producer.send_batch(event_data_batch)
                print(
                    f"Success sent to Azure Eventhub the event {streaming_medicines}")

        else:
            format = "%H:%M:%S"
            print(
                f"Start Time = {start_time.strftime(format)}  e End Time = {end_time.strftime(format)}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


if '__main__' == __name__:
    print(run_streaming(qty_patients=10, min_to_run=0.5))
