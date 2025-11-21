import os
import base64

# TODO
API_KEY = 'INSERT_API_KEY_HERE'
API_URL = 'INSERT_API_URL_HERE'

HEADERS = {
    'Authorization': f'Basic {base64.b64encode( f"{API_KEY}:".encode() ).decode()}'
}