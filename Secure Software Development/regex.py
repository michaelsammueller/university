import re

# Regex to match UK postcodes
def validate_postcode(postcode):
    # Max length of UK postcode
    max_length = 8
    # Check if postcode is too long
    if len(postcode) > max_length:
        return False
    
    # Assign regex to variable 'postcode_regex'
    postcode_regex = r'[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}'
    # Check if postcode matches regex
    is_valid = re.match(postcode_regex, postcode)
    # Return True if postcode is valid, False otherwise
    return bool(is_valid)

# Test 1
# print(validate_postcode("M1 1AA")) # True
# print(validate_postcode("M60 1NW")) # True
# print(validate_postcode("CR2 6XH")) # True
# print(validate_postcode("DN55 1PT")) # True
# print(validate_postcode("W1A 1HQ")) # True
# print(validate_postcode("EC1A 1BB")) # True
# print(validate_postcode("SW1A 2AA")) # True
# print(validate_postcode("M3 6AAA8AC")) # False
# print(validate_postcode("M3 1BB")) # True
