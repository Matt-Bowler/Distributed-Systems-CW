import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import logging
from datetime import datetime, timezone
import random
from PIL import Image
import io
import uuid

img_gen_upload = func.Blueprint()

def generate_image():
    img_width = random.randint(128, 1920)
    img_height = random.randint(128, 1080)

    img_size = (img_width, img_height)
    image = Image.new("RGB", img_size, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))) 

    img_byte_arr = io.BytesIO()         
    image.save(img_byte_arr, format='PNG')  
    img_byte_arr.seek(0)  
    return img_byte_arr


@img_gen_upload.timer_trigger(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
def image_gen_upload(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function executed at %s', datetime.now(timezone.utc))


    image = generate_image()
    blob_name = f"image_{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H%M%S')}_{str(uuid.uuid4())}.png"

    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.environ["AZURE_STORAGE_CONNECTION_STRING"])
        container_name = "images"

        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            logging.info(f"Container '{container_name}' created.")
        else:
            logging.info(f"Container '{container_name}' already exists.")

        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(image, overwrite=True)

        logging.info(f"Uploaded content to blob: {blob_name}")
    except Exception as e:
        logging.error(f"Failed to upload blob: {e}")