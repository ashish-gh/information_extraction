import os
import json
import time
import uuid

import cv2
import numpy as np
import pandas as pd

from loguru import logger
from flask import Flask, abort, jsonify, request, g

from app.parser.pytesseract import parse_image
from app.parser.extractor import extractor



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
        abort_json(400, "IMAGE_MISSING_ON_REQUEST")

    logger.debug(f"Request file names {request.files}")
    file = request.files["file"]

    _, ext = os.path.splitext(os.path.basename(file.filename))
    ext = ext.lower()

    if ext not in ALLOWED_TYPES:
        logger.error(f'UNSUPPORTED_TYPE : {str(ext)}')
        abort(415, "File Type Not Supported")

    fid = uuid.uuid4().hex
    file_name = os.path.join("tmp", fid + ext)
    file.save(file_name)

    logger.info(f"File saved as : {file_name}")
    res = {
        "data": None,
        "message": "no data found",
        "status_code": 404,
        "meta_data": {
            "deltatime": None,
        },
    }

    if file_name:
        try:
            # TODO
            start = time.time()
            df = parse_image(file_name, debug=False)
            if not df.empty:
                data = extractor(df)
                delta = np.around(time.time() - start, 2)
                logger.debug(f"Delta time for extraction : {delta} seconds")
                res = {
                    "data": data,
                    "message": "data found",
                    "status_code": 200,
                    "meta_data": {
                        "deltatime": delta,
                    },
                }

        except Exception as e:
            logger.error(f"dataframe extraction error : {e}")
    return res


if __name__ == "__main__":
    app.run()
