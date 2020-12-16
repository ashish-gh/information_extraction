import re
import os
import time

import pandas as pd
import numpy as np
from loguru import logger

from ..util.utils import extract_mobile_number




def extractor(df: pd.DataFrame) -> dict:
    """
    Extract date and email address from dataframe using regular expression

    Args:
        ``df``: dataframe
            dataframe obtained from image ocr
    Returns:
            {
                "date":
                        {
                            "text" : ,
                            "bbox" : [x0, y0, x2, y2]
                        } ,

                "email" :
                    {
                        "text" :
                        "bbox": [x0, y0, x2, y2]
                    }
            }
    """
    data = []
    empty_dummy = {
        "date": {"text": None, "bbox": None},
        "email": {"text": None, "bbox": None},
    }

    if df.empty:
        return data.append(empty_dummy)

    # possible date and emial patterns
    email_pattern = r"(^[a-zA-Z0-9_.+-]+[@.][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    date_pattern = [
        r"([12]\d{3}[-/.](0[1-9]|1[0-2])[-/.](0[1-9]|[12]\d|3[01]))",
        r"(\d{2}[-/.]\d{2}[-/.]\d{4})",
    ]
    mobile_number_pattern = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                    [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{3,4})'''

    
    for row in df.itertuples():
        # check if matches with date pattern
        for dp in date_pattern:
            date_match = re.match(dp, row.Text)
            if date_match:
                logger.debug(f'Date match : {date_match}')
                d = {
                    "date": {
                        "text": date_match[0],
                        "bbox": [row.x0, row.y0, row.x2, row.y2],
                    }
                }
                data.append(d)
        # check if matches with email pattern
        email_match = re.match(email_pattern, row.Text)
        if email_match:
            d = {
                "email": {
                    "text": email_match[0],
                    "bbox": [row.x0, row.y0, row.x2, row.y2],
                }
            }
            data.append(d)
        
        # check if matches number pattern
        number_match =  re.findall(re.compile(mobile_number_pattern), row.Text)
        if number_match:
            d = {
                "number": {
                    "text": number_match[0],
                    "bbox": [row.x0, row.y0, row.x2, row.y2],
                }
            }
            data.append(d)
            
    return data
