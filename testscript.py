import os
import sys
import json
import time
import uuid
import requests

import cv2
import numpy as np
import pandas as pd

from loguru import logger
from flask import Flask, abort, jsonify, request, g

from app.parser.pytesseract import parse_image


def extract(fname):

    df = parse_image(fname, debug=False)
    url = "http://127.0.0.1:5000/api/v1/extract/"
    data = df.to_dict("records")
    files = [("file", open(fname, "rb"))]

    logger.info(f"Hitting API at {url}")
    logger.info(f"File = {fname}")

    response = requests.request("POST", url, files=files)
    logger.debug(f"Response = \n{response.json()}")
    response = response.json()


def main():
    fname = sys.argv[-1]
    extract(fname)


if __name__ == "__main__":
    main()
