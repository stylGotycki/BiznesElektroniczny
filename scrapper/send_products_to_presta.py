from config import API_KEY, API_URL, HEADERS
import requests
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from random import randint

CATEGORY_CACHE = Path("category_ids.json")
MANUFACTURER_CACHE = Path("manufacturers_ids.json")


def slugify(text):
    t = text.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


def load_category_cache():
    if CATEGORY_CACHE.exists():
        return json.loads(CATEGORY_CACHE.read_text())
    return {}


def load_manufacturer_cache():
    if MANUFACTURER_CACHE.exists():
        return json.loads(MANUFACTURER_CACHE.read_text())
    return {}


category_cache = load_category_cache()
manufacturer_cache = load_manufacturer_cache()


def generate_description(description: list) -> str:
    output: str = ''
    for line in description:
        output += f"<p>{line}</p>"
    return output


def get_or_create_product(product, category_cache, manufacturer_cache):
    category_id = category_cache[product["category"]]
    
    if product["manufacturer"] not in manufacturer_cache:
        print(f"Manufacturer {product['manufacturer']} not found!")
        return
    
    manufacturer_id = manufacturer_cache[product["manufacturer"]]

    name = escape(product["name"])
    slug = escape(slugify(name))
    price = product["price"]
    description = generate_description(product["description"]) if product["description"] else "Brak opisu!"
    description_short = product["description"][0] if product["description"] else "Brak opisu!"

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
  <product>
    <id_category_default>{category_id}</id_category_default>
    <id_manufacturer>{manufacturer_id}</id_manufacturer>
    <id_tax_rules_group>1</id_tax_rules_group>
    <active>1</active>
    <reference>{slug[:60]}</reference>
    <show_price>1</show_price>
    <available_for_order>1</available_for_order>
    <state>1</state>
    <minimal_quantity>1</minimal_quantity>
    <indexed>1</indexed>
    <price>{price}</price>
    <name><language id="1">{name}</language></name>
    <description_short><language id="1">{description_short[:750]}</language></description_short>
    <description><language id="1">{description}</language></description>
    <link_rewrite><language id="1">{slug}</language></link_rewrite>
    <visibility>both</visibility>
    <associations>
      <categories>
        <category><id>{category_id}</id></category>
      </categories>
    </associations>
    <meta_title>{name[:32]}</meta_title>
    <meta_description>{name[:32]}</meta_description>
    <meta_keywords>{name[:32]}</meta_keywords>
  </product>
</prestashop>
"""

    r = requests.post(
        f"{API_URL}/products",
        data=xml.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        auth=(API_KEY, "")
    )

    if r.status_code not in (200, 201):
        print(r.text)
        raise Exception(f"Failed to create product {name}")

    created = ET.fromstring(r.text)
    product_id = int(created.find(".//id").text)
    return product_id


def upload_product_images(product_id, images_folder, image_files):
    for img in image_files:
        with open(f"{images_folder}/{img}", "rb") as f:
            files = {"image": f}
            r = requests.post(
                f"{API_URL}/images/products/{product_id}",
                files=files,
                auth=(API_KEY, "")
            )
        if r.status_code not in (200, 201):
            print(r.text)
            print(f"Failed to upload {img} for product {product_id}")
            

def upload_products_and_images():
    with open("../scrapper_results/json/products.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    
    for prod in products:
        pid = get_or_create_product(prod, category_cache, manufacturer_cache)
        if pid is None:
            print(f"Skipping product {prod['name']} because it was not created")
            continue
        
        print(f"Created product {prod['name']} -> ID {pid}")

        upload_product_images(pid, "../scrapper_results/images", prod["images"])
        set_product_quantity(pid, randint(0, 10))
        

def set_product_quantity(product_id, quantity):
    params = {
        "filter[id_product]": product_id,
        "display": "full"
    }
    r_stock = requests.get(f"{API_URL}/stock_availables", params=params, auth=(API_KEY, ""), verify=False)
    # print(r_stock.text)
    root = ET.fromstring(r_stock.text)
    stock_id = str(root.find(".//stock_available/id").text)
    id_shop = str(root.find(".//stock_available/id_shop").text)
    id_product_attribute = str(root.find(".//stock_available/id_product_attribute").text)
    id_shop_group = str(root.find(".//stock_available/id_shop_group").text)
    depends_on_stock = str(root.find(".//stock_available/depends_on_stock").text)
    location = str(root.find(".//stock_available/location").text)
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
  <stock_available>
    <id>{stock_id}</id>
    <id_product>{product_id}</id_product>
    <id_product_attribute>{id_product_attribute}</id_product_attribute>
    <quantity>{quantity}</quantity>
    <id_shop>{id_shop}</id_shop>
    <id_shop_group>{id_shop_group}</id_shop_group>
    <location>{location}</location>
    <depends_on_stock>{depends_on_stock}</depends_on_stock>
    <out_of_stock>0</out_of_stock>
  </stock_available>
</prestashop>
"""
    r = requests.put(
        f"{API_URL}/stock_availables",
        data=xml.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        auth=(API_KEY, "")
    )
    if r.status_code not in (200, 201):
        print("Failed to set stock:", r.text)
    else:
        print(f"Stock set for product {product_id} -> {quantity}")
        


def delete_all_products_and_images():
    """
    Usuwa wszystkie produkty i obrazki w PrestaShopie przez Webservice.
    """

    r = requests.get(f"{API_URL}/products?display=[id]", auth=(API_KEY, ""))
    if r.status_code != 200:
        print("Failed to fetch products:", r.text)
        return

    root = ET.fromstring(r.text)
    product_ids = [int(node.find("id").text) for node in root.findall(".//product")]
    print(f"Found {len(product_ids)} products.")


    for pid in product_ids:
        # Delete product images first
        rimg = requests.get(f"{API_URL}/images/products/{pid}", auth=(API_KEY, ""))
        if rimg.status_code == 200:
            img_root = ET.fromstring(rimg.text)
            image_ids = [int(img.attrib["id"]) for img in img_root.findall(".//image")]
            for img_id in image_ids:
                rdel_img = requests.delete(f"{API_URL}/images/products/{pid}/{img_id}", auth=(API_KEY, ""))
                if rdel_img.status_code in (200, 204):
                    print(f"Deleted image {img_id} of product {pid}")
                else:
                    print(f"Failed to delete image {img_id} of product {pid}: {rdel_img.text}")

        # Delete the product
        rdel_prod = requests.delete(f"{API_URL}/products/{pid}", auth=(API_KEY, ""))
        if rdel_prod.status_code in (200, 204):
            print(f"Deleted product {pid}")
        else:
            print(f"Failed to delete product {pid}: {rdel_prod.text}")

    print("All products and images have been deleted.")


delete_all_products_and_images()

upload_products_and_images()