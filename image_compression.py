from datetime import datetime, timezone
import azure.functions as func
import logging
from PIL import Image
from azure.storage.blob import BlobServiceClient
import os
import io
from pathlib import Path

img_comp = func.Blueprint()


def compress_image(download_stream):
    image = Image.open(download_stream)

    image = image.resize((1080, 1350), Image.Resampling.LANCZOS)

    output_stream = io.BytesIO()
    image.save(output_stream, format="JPEG", optimize=True, quality=20)
    output_stream.seek(0)
    return output_stream

def parse_blob_name(blob_name):
    return Path(blob_name).stem


@img_comp.blob_trigger(arg_name="myblob", path="images", connection="AzureWebJobsStorage") 
def image_compression(myblob: func.InputStream):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(os.environ["AZURE_STORAGE_CONNECTION_STRING"])

        compressed_image = compress_image(myblob)
        parsed_blob_name = parse_blob_name(myblob.name)
        logging.info(f"Parsed name: {parsed_blob_name}")
        compressed_blob_name = f"{parsed_blob_name}.jpg"


        container_name = "compressed-images"
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container()
            logging.info(f"Container '{container_name}' created.")
        
        blob_client = container_client.get_blob_client(compressed_blob_name)
        blob_client.upload_blob(compressed_image, overwrite=True)

        logging.info(f"Compressed image uploaded as {compressed_blob_name}")
    except Exception as e:
        logging.error(f"Error compressing image {myblob.name}, details: {e}")

