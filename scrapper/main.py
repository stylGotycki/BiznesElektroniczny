import json
import requests
from bs4 import BeautifulSoup
import os
import re
import time


class ProductView:
    """
    Widok produktu na stronie.
    """
    
    def __init__(self, name: str, link: str, images: list | None, price: float, manufacturer: str):
        """
        Konstuktor

        Args:
            name (str): _description_
            link (str): _description_
            images (list | None): _description_
            price (float): _description_
            manufacturer (str): _description_
        """
        self.name = name
        self.link = link
        self.images = []
        self.price = price
        self.manufacturer = manufacturer
        self.description = None
        
    def to_dict(self):
        return {
            "name": self.name,
            "images": self.images,
            "price": self.price,
            "manufacturer": self.manufacturer,
            "description": self.description
        }
    
    def scrape_product_details():
        pass

    
def get_html_with_requests(url: str):
    """
    Pobierz HTML ze strony za pomocą requests.
    
    Args:
        url (_str_): Adres URL strony.
    """

    response = requests.get(url)
    response.raise_for_status()
    return response.text


class Category:
    pass