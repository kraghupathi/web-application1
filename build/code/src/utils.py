
# module to hold all utilities/helper functions

import json

import re

def is_alphabetic_string(value):
    if re.search('[^a-zA-Z. ]+', value):
        return False
    else:
        return True

def is_email(value):
    if re.search('[^@]+@[^@]+\.[^@]+', value):
        return True
    else:
        return False
