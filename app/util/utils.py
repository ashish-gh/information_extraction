import re
import os
import json
import time
from typing import List, Dict, Tuple




def extract_mobile_number(text: str)->str:
    number = ""
    
    if not text:
        return number

    mobile_number_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                        [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
    phone = re.findall(re.compile(mobile_number_regex), text)
    if phone:
        logger.warning(f'Phone : {phone}')
        number = ''.join(phone[0])    
    return number




def extract_email(text: str)->str:
    
    email = ""
    
    if not text:
        return email
    
    email_regex = r"(^[a-zA-Z0-9_.+-]+[@.][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    email_address = re.findall(re.compile(email_regex),text)
    if email_address:
        email = ''.join(email_address[0])    
    return email



    



