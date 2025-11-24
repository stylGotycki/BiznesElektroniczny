import os
import base64

API_KEY = '1G6GWMMGQVDUCJP9EKXEB6X252YSIG13'
API_URL = 'http://localhost:8080/api'

HEADERS = {
    'Authorization': f'Basic {base64.b64encode( f"{API_KEY}:".encode() ).decode()}'
}