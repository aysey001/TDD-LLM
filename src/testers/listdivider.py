
import re

def split_string(s):
    # Split the string into items based on the pattern 'number. '
    items = re.split(r'\d+\.\s', s)
    # The first item is empty because the string starts with a number, so we remove it
    items = items[1:]
    return items


