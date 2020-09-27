import os
import sys
import time
import cv2

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pytesseract
from pytesseract import Output

from PIL import Image


def parse_image(file_name: str, debug: bool = True) -> pd.DataFrame:
    """
    Converts image to dataframe

    Args:
        ``file_name``: file_name of image

    Return
        ``df``: pd.DataFrame
            dataframe of text from image
    """
    if not file_name:
        return pd.DataFrame([])

    image = cv2.imread(file_name)

    if debug:
        img = Image.open(file_name).copy()
        img.show()

    try:
        extracted_data = pytesseract.image_to_data(image, output_type=Output.DICT)
    except Exception as e:
        logger.error(f"Error on pytesseract : {e}")

    # possible keys
    # ['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num', 'left', 'top', 'width', 'height', 'conf', 'text'])

    data = []
    for i in range(len(extracted_data["text"])):
        if int(extracted_data["conf"][i]) > 60:
            tmp_data = {
                "level": extracted_data["level"][i],
                "page_num": extracted_data["page_num"][i],
                "block_num": extracted_data["block_num"][i],
                "par_num": extracted_data["par_num"][i],
                "line_num": extracted_data["line_num"][i],
                "word_num": extracted_data["word_num"][i],
                "x0": extracted_data["left"][i],
                "y0": extracted_data["top"][i],
                "x2": extracted_data["width"][i],
                "y2": extracted_data["height"][i],
                "Text": extracted_data["text"][i],
                "conf": extracted_data["conf"][i],
            }
            data.append(tmp_data)

    if data:
        df = pd.DataFrame(data)
        # TODO:
        # Once data is extracted, there may be unwanted datas as well so make sure these datas are also eliminated during the post processing stage.
        # make function in utils/ clean_dataframe(df)-> df

    return df
