import os
import base64

API_KEY = 'BJK9VTGMIKT6JG655I8NVFIJK7S74ZUJ'
API_URL = 'http://localhost:8080/api'

HEADERS = {
    'Authorization': f'Basic {base64.b64encode( f"{API_KEY}:".encode() ).decode()}'
}