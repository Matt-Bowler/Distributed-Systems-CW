import logging
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def image_gen_upload(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')


@app.blob_trigger(arg_name="myblob", path="images",
                               connection="37924e_STORAGE") 
def image_compression(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
