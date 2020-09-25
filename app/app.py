import os
import json
import time
import uuid

import cv2

from loguru import logger
from flask import Flask, abort, jsonify, request, g



app = Flask(__name__)
logger.info("starting server . . .")

# if the path does not exists make one
if not os.path.exists("tmp"):
    os.makedirs("tmp")



@app.route("/api/v1/extract/", methods=["POST"])
def extract():
    return "Hello, from server"



if __name__ == "__main__":
    app.run()