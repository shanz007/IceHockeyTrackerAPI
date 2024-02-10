import re

from flask import request

def is_valid_email(email):
    # Regular expression pattern for matching email addresses
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Match the email address against the pattern
    if re.match(pattern, email):
        return True
    else:
        return False