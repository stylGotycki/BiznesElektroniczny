import json
import requests
from bs4 import BeautifulSoup, NavigableString
import os
import re
import time

# TODO: relation with category
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
#        self.category = category
        
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
    
    
    def scrape_product_details(self, images_dir: str) -> None:
        """
        Scrapping informacji o produkcie. Następnie aktualizacja obiektu i zapis zdjęć we wskazanym katalogu.

        Args:
            images_dir (str): Nazwa katalogu, w którym będą zapisane zdjęcia produktu.
        """
        
        full_url = f"https://iklamki.pl/pl/produkty/{self.link}"
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        self._find_and_set_description(soup)
        self._find_and_set_images(soup, images_dir)
    
        
    def _find_and_set_description(self, soup: BeautifulSoup) -> None:
        """
        Wyłuskanie opisu produktu.
        
        Args:
            soup (BeautifulSoup): Kontekst pliku HTML.
        """
        
        description_element = soup.find('div', class_='product-description', itemprop='description')
        if description_element:
            paragraphs = description_element.find_all('p')
            self.description = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        else:
            self.description = ["Brak opisu"]
    
     
    # TODO: czy pobierać wszystkie zdjęcia?
    # TODO: large i medium to często to samo - chyba trzeba wywalić jeden z nich
    def _find_and_set_images(self, soup: BeautifulSoup, images_dir: str) -> None:
        """
        Wyłuskanie obrazów produktu. 

        Args:
            soup (BeautifulSoup): Kontekst pliku HTML.
            images_dir (str): Nazwa katalogu, w którym będą zapisane zdjęcia produktu.
        """
        
        gallery_element = soup.find('ul', class_='product-images js-qv-product-images')
        gallery_items = gallery_element.find_all('img')
        
        for idx, item in enumerate(gallery_items):
            images = {
                'large': item['data-image-large-src'],    
                'medium': item['data-image-medium-src'],
                'default': item['src']
            }
            
            for image_size, image_url in images.items():
                formatted_name = f"{image_size}_{sanitize_filename(self.name)}_{idx}.jpg"
                self.images.append(formatted_name)
                save_image(image_url, images_dir, formatted_name)
                
            

def get_html_with_requests(url: str):
    """
    Pobierz HTML ze strony za pomocą requests.
    
    Args:
        url (_str_): Adres URL strony.
    """

    response = requests.get(url)
    response.raise_for_status()
    return response.text


def sanitize_filename(filename):
    """Usuwa niedozwolone znaki w nazwach plików."""
    
    return re.sub(r'[\\/*?:"<>|]', '_', filename)


def save_image(image_url, output_dir, filename):
    """Pobiera obrazek z URL i zapisuje go w podanym katalogu."""
    
    output_path = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Wyrzuca wyjątek w razie błędu HTTP
        with open(output_path, 'wb') as img_file:
            for chunk in response.iter_content(chunk_size=8192):
                img_file.write(chunk)
    except Exception as e:
        print(f"Błąd podczas pobierania obrazka {image_url}: {e}")


class Category:
    """
    Kategoria na stronie.
    """
    
    def __init__(self, name, link, parent_hierarchy=None):
        """
        Konstruktor.

        Args:
            name (str): Nazwa.
            link (str): Link.
            parent_hierarchy (Category, optional): Kategoria nadrzędna. Defaults to None.
        """
        self.name = name
        self.link = link
        self.parent_hierarchy = parent_hierarchy
        self.subcategories = []
        
        
    def add_subcategory(self, subcategory):
        """
        Dodanie podkategorii.
        
        Args:
            subcategory (Category): Kategoria, która jest podkategorią.
        """
        
        self.subcategories.append(subcategory)            


    def to_dict(self) -> dict:
        """
        Zwraca obiekt jako słownik
        
        Returns:
            dict: Obiekt jako słownik.
        """
        
        return {
            "name": self.name,
            "link": self.link,
            "subcategories": [sub.to_dict() for sub in self.subcategories]
        }


def direct_text(element):
    """
    Zwraca tylko tekst, ignorując elementy-dzieci i ich zawartości.
    """
    parts = []
    for child in element.children:
        if isinstance(child, NavigableString):
            text = str(child).strip()
            if text:
                parts.append(text)
    return " ".join(parts).strip()


def scrape_categories(html) -> list[Category]:
    """
    Zwraca kategorie produktów.

    Args:
        html (BeautifulSoup): Konkekst HTML.

    Raises:
        Exception: Jeżeli kontekst HTML nie znajdzie elementu.

    Returns:
        list[Category]: Lista kategorii.
    """
    soup = BeautifulSoup(html, "html.parser")
    top_menu = soup.select_one('ul.top-menu[data-depth="1"]')
    if not top_menu:
        raise RuntimeError("No top menu with data-depth=1 found")

    categories = []

    for li in top_menu.find_all("li", class_="category", recursive=False):
        a = li.find("a", class_="dropdown-item")
        if not a:
            continue
        
        name = direct_text(a) or a.get_text(strip=True)
        link = a.get("href")
        parent = Category(name, link)

        submenu = li.find("ul", attrs={"data-depth": "2"})
        if submenu:
            for sub_li in submenu.find_all("li", class_="category", recursive=False):
                a2 = sub_li.find("a", class_="dropdown-item")
                if not a2:
                    continue
                sub_name = direct_text(a2) or a2.get_text(strip=True)
                sub_link = a2.get("href")
                child = Category(sub_name, sub_link, parent_hierarchy=parent.name)
                parent.add_subcategory(child)

        categories.append(parent)

    return categories


def main():
    url = "https://iklamki.pl/pl/"
    html = get_html_with_requests(url)
    categories = scrape_categories(html)
    
    for cat in categories:
        print(cat.name)
        for sub in cat.subcategories:
            print("   -", sub.name)
    
    # now only for testing purposes :P
    # product = ProductView(
    #     name = 'for now empty',
    #     link = '2764-uchwyt-meblowy-viefe-rille-55mm-stal-szlachetna.html', # for now hardcoded
    #     images = [],
    #     price = 21.37,
    #     manufacturer = 'for now empty'
    # )
    
    # product.scrape_product_details('../scrapper_results/images')



if __name__ == "__main__":
    main()