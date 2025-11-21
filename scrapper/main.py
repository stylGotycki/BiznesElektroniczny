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
        Konstuktor.

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
        
    def to_dict(self) -> dict:
        """
        Zwraca obiekt jako słownik.

        Returns:
            dict: Obiekt jako słownik.
        """
        
        return {
            "name": self.name,
            "images": self.images,
            "price": self.price,
            "manufacturer": self.manufacturer,
            "description": self.description
        }
    
    def scrape_product_details(self, images_dir: str):
        """
        Scrapping informacji o produkcie. Następnie aktualizacja obiektu i zapis zdjęć we wskazanym katalogu.

        Args:
            images_dir (str): Nazwa katalogu, w którym będą zapisane zdjęcia produktu.
        """
        
        full_url = f"https://iklamki.pl/pl/produkty/{self.link}"
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        description_element = soup.find('div', class_='product-description', itemprop='description')
        if description_element:
            paragraphs = description_element.find_all('p')
            self.description = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        else:
            self.description = ["Brak opisu"]
                
        # print(description_element)
        # print(self.description)

    
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


def main():
    # now only for testing purposes :P
    product = ProductView(
        name = 'for now empty',
        link = '2764-uchwyt-meblowy-viefe-rille-55mm-stal-szlachetna.html', # for now hardcoded
        images = [],
        price = 21.37,
        manufacturer = 'for now empty'
    )
    
    product.scrape_product_details('for now empty')


if __name__ == "__main__":
    main()