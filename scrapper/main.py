import json
import requests
from bs4 import BeautifulSoup, NavigableString
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

IMAGES_DIR = '../scrapper_results/images'
PRODUCTS_JSON = '../scrapper_results/json/products.json'
CATEGORIES_JSON = '../scrapper_results/json/categories.json'


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


class Product:
    """
    Widok produktu na stronie.
    """
    
    def __init__(self, link: str, category: Category):
        """
        Konstuktor.

        Args:
            link (str): Link do produktu.
            category (Category): Kategoria produktu.
        """
        
        self.name = None
        self.link = link
        self.images = []
        self.price = None
        self.brand = None
        self.description = None
        self.category = category
        
        
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
            "manufacturer": self.brand,
            "description": self.description
        }
    
    
    def scrape(self, images_dir: str) -> bool:
        """
        Scrapping informacji o produkcie. Następnie aktualizacja obiektu i zapis zdjęć we wskazanym katalogu.

        Args:
            images_dir (str): Nazwa katalogu, w którym będą zapisane zdjęcia produktu.
        
        Returns:
            bool: Sukces lub porażka
        """
        
        response = requests.get(self.link)
        soup = BeautifulSoup(response.text, 'html.parser')
                
        self._find_and_set_rest(soup)
        self._find_and_set_description(soup)
        self._find_and_set_images(soup, images_dir)
    
    
    def _find_and_set_rest(self, soup: BeautifulSoup) -> None:
        """
        Wyłuskuje nazwę, cenę i brand.
        
        Args:
            soup (BeautifulSoup): Kontekst HTML.
        """

        name = soup.find('h1', class_='h1 product-name', attrs={'itemprop': 'name'})
        price = soup.find('span', attrs={'itemprop': 'price'})
        brand_li = soup.find('li', attrs={'itemprop': 'brand'})
        brand = brand_li.find('a')
        price_float = float(price.text.replace("\xa0", "").replace("zł", "").strip().replace(",", "."))

        self.name = name.text
        self.price = price_float
        self.brand = brand.text
        
        
    def _find_and_set_description(self, soup: BeautifulSoup) -> None:
        """
        Wyłuskanie opisu produktu.
        
        Args:
            soup (BeautifulSoup): Kontekst pliku HTML.
        """
        
        description_element = soup.find('div', class_='product-description', itemprop='description')
        if description_element:
            paragraphs = description_element.find_all('p')
            if paragraphs:
                self.description = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
            else:
                self.description = ["Brak opisu!"]
        else:
            self.description = ["Brak opisu"]
    
     
    def _find_and_set_images(self, soup: BeautifulSoup, images_dir: str) -> None:
        """
        Wyłuskanie obrazów produktu. 

        Args:
            soup (BeautifulSoup): Kontekst pliku HTML.
            images_dir (str): Nazwa katalogu, w którym będą zapisane zdjęcia produktu.
        """
        
        gallery_element = soup.find('ul', class_='product-images js-qv-product-images')
        if not gallery_element:
            print('No gallery! aborting')
        
        gallery_items = gallery_element.find_all('img')
        if not gallery_items:
            print('No gallery items! aborting')
        
        
        for idx, item in enumerate(gallery_items):
            images = {
                'large': item['data-image-large-src'],    
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


def scrape_pages_count(link) -> int:
    html = get_html_with_requests(link)
    soup = BeautifulSoup(html, 'html.parser')

    ul_element = soup.find('ul', class_='page-list clearfix text-sm-center')
    
    # TODO: I'm not sure about this solution : P
    pages_count_info = int(ul_element.find_all('li')[-2].text)
    
    return pages_count_info


def is_page_404_or_empty(soup: BeautifulSoup) -> bool:
    """
    Sprawdza czy to strona 404 lub pusta sekcja (np. brak produktów danej kategorii).
    
    Args:
        soup (BeautifulSoup): Kontekst HTML.

    Returns:
        bool: Flaga.
    """
    
    page_not_found_element = soup.find('section', class_='page-content page-not-found')
    
    if page_not_found_element:
        return True
    return False
    
    
# WARNING: executing this function takes some time
def scrape_products_from_category(category: Category) -> list[Product]:
    """
    Scrapping produktów względem kategorii.

    Args:
        category (Category): Kategoria produktu.

    Returns:
        list[Product]: Lista produktów.
    """
    link = category.link
    pages_count = scrape_pages_count(link)
    
    products = []
    
    # FIXME: I decided that it's better to limit data scrapping to 48 elements per category.
    for page in range(1, min(4, pages_count+1)):
    # for page in range(1, 2): # TODO: only for tests
        html = get_html_with_requests(f"{link}?page={page}")
        soup = BeautifulSoup(html, 'html.parser')

        if is_page_404_or_empty(soup):
            print(f'{category=} is empty.')
            continue
            
        products_element = soup.find_all('article', class_='product-miniature js-product-miniature')

        if not products_element:
            print(f'{category=} products page not found.')
            continue

        for product_element in products_element:
            product_link = product_element.find('a')['href']

            if not product_element:
                print(f'{category=} product element not found.')
                continue
                
            product = Product(
                link=product_link,
                category=category
            )
            
            product.scrape(IMAGES_DIR)

            products.append(product)
    
            
    return products
            

def save_products_to_json(products: list[Product]):
    with open(PRODUCTS_JSON, 'w', encoding='utf-8') as f:
        json.dump([p.to_dict() for p in products], f, indent=4, ensure_ascii=False)
    

def save_categories_to_json(categories: list[Category]):
    with open(CATEGORIES_JSON, 'w', encoding='utf-8') as f:
        json.dump([c.to_dict() for c in categories], f, indent=4, ensure_ascii=False)
    

# TODO: refactor :D
def main():    
    url = "https://iklamki.pl/pl/"
    html = get_html_with_requests(url)
    categories = scrape_categories(html)
    
    save_categories_to_json(categories)
    
    # flattening of structure
    all_subcats = [
        sub
        for category in categories
        for sub in (category.subcategories or [category])
    ]
        
    products = []    
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_cat = {
            executor.submit(scrape_products_from_category, cat): cat
            for cat in all_subcats
        }

        for future in as_completed(future_to_cat):
            cat = future_to_cat[future]
            try:
                scraped = future.result()
                products.extend(scraped)
                print(f"Scraped {len(scraped)} products from {cat.name}")
            except Exception as e:
                print(f"Error scraping {cat.name}: {e}")
    
    
    save_products_to_json(products)
        

if __name__ == "__main__":
    main()