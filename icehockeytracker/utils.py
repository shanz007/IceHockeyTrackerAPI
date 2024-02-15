import re

from flask import request

def is_valid_email(email):
    """validare email

    Args:
        email (_type_): _description_

    Returns:
        _type_: _description_
    """    
    # Regular expression pattern for matching email addresses
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # Match the email address against the pattern
    if re.match(pattern, email):
        return True
    else:
        return False
    
def is_valid_ssn(ssn, date_of_birth):
    """ Validate provided ssn against the provided date of birth.
    Args:
        ssn (_type_): _description_
        date_of_birth (_type_): _description_

    Returns:
        _type_: _description_
    """    
    # Extracting the components of the SSN
    ssn_components = re.match(r'(\d{2})(\d{2})(\d{2})-(\d{4})', ssn)
    if not ssn_components:
        return False
    
    day, month, year, random = ssn_components.groups()
    
    # Formatting the date of birth
    formatted_dob = date_of_birth.strftime('%d%m%y')
    
    # Checking if the SSN date of birth matches the provided date of birth
    if day+month+year == formatted_dob:
        return True
    else:
        return False