import os
import textwrap

import starkbank

# Replace 'private_key_string' with your actual private key string
string_to_convert = os.getenv("PRIVATE_KEY")

# Remove leading and trailing lines
string_to_convert = string_to_convert.replace('-----BEGIN EC PRIVATE KEY-----\\n', '')
string_to_convert = string_to_convert.replace('\\n-----END EC PRIVATE KEY-----', '')

# Remove newline characters
string_to_convert = string_to_convert.replace('\\n', '')

# Wrap the string in 64-character lines (for readability)
string_to_convert = textwrap.wrap(string_to_convert, 64)

# Insert newline characters at appropriate positions
converted_string = '\n'.join(string_to_convert)

# Add the leading and trailing lines
pem_key = '-----BEGIN EC PRIVATE KEY-----\n' + converted_string + '\n-----END EC PRIVATE KEY-----'

project = starkbank.Project(
    environment="sandbox",
    id="6264161537359872",
    private_key=pem_key
)
