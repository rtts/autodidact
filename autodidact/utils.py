import random
import string
import unicodedata

HUMAN_FRIENDLY_CHARS = "234679ABCDEFGHJKLMNPRSTUVWXYZabcdefghijkmnpqrstuvwxyz"

def random_string(length):
    return ''.join(random.choice(HUMAN_FRIENDLY_CHARS) for x in range(length))

def clean(dirty_filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

    # Replace accented characters with unaccented ones
    normalized_filename = unicodedata.normalize('NFKD', dirty_filename).encode('ASCII', 'ignore')

    # Strip out all characters that are not in @valid_chars
    cleaned_filename = ''.join([c for c in normalized_filename if c in valid_chars])

    return cleaned_filename
