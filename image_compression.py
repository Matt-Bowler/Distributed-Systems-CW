import azure.functions as func
import logging

img_comp = func.Blueprint()

@img_comp.blob_trigger(arg_name="myblob", path="images", connection="AzureWebJobsStorage") 
def image_compression(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")