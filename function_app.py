import logging
import azure.functions as func

app = func.FunctionApp()

from image_gen_upload import img_gen_upload
from image_compression import img_comp

app.register_functions(img_gen_upload) 
app.register_functions(img_comp) 

