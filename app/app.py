import os
import json
import time
import uuid

import cv2

from loguru import logger
from flask import Flask, abort, jsonify, request, g


from .parser.pytesseract import parse_image



ALLOWED_TYPES = [".jpg", ".png", ".jpeg"]

app = Flask(__name__)
logger.info("starting server . . .")

# if the path does not exists make one
if not os.path.exists("tmp"):
    os.makedirs("tmp")


@app.route("/api/v1/extract/", methods=["POST"])
def extract():
    logger.info("extracting data from image")

    if not request.headers["Content-Type"].startswith("multipart/form-data"):
        abort_json(400, "Content-Type can only be json or form-data")

    if not request.files:
        print("no files")
        abort_json(400, "IMAGE_MISSING_ON_REQUEST")
        
    logger.debug(f"Request file names {request.files}")
    file = request.files["file"]

    _, ext = os.path.splitext(os.path.basename(file.filename))
    ext = ext.lower()

    if ext not in ALLOWED_TYPES:
        print("no allowed types")
        abort(400, "File Type Not Supported", f"Allowed file types are : {ALLOWED_TYPES}")
    
    fid = uuid.uuid4().hex
    file_name = os.path.join("tmp", fid+ext)
    file.save(file_name)

    logger.info(f"File saved as : {file_name}")

    # TODO:
    # 1. call to function to extract data from image
    if file_name:
        try:
            # TODO            
            # First get dataframe for image
            # then create simple extraction part
            df = parse_image(file_name, debug=False)
            if not df.empty:
                for row in df.head().itertuples():
                    print(row)
                    
                # print(df.head())                
        except Exception as e:
            logger.error(f"dataframe extraction error : {e}")
    else:
        print("No file ")
    return "Hello, from server"




if __name__ == "__main__":
    app.run()