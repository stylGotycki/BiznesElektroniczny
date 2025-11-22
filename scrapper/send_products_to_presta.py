from config import API_KEY, API_URL, HEADERS
import requests
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

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


def get_or_create_product(product, category_cache, manufacturer_cache):
    category_id = category_cache[product["category"]]
    # TODO: REGUITTI
    manufacturer_id = manufacturer_cache[product["manufacturer"]]

    name = escape(product["name"])
    slug = escape(slugify(name))
    price = product["price"]
    description = product["description"][0] if product["description"] else ""
    description_short = description[:600]

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
  <product>
    <id_category_default>{category_id}</id_category_default>
    <id_manufacturer>{manufacturer_id}</id_manufacturer>
    <active>1</active>
    <price>{price}</price>
    <name><language id="1">{name}</language></name>
    <description_short><language id="1">{description_short}</language></description_short>
    <description><language id="1">{description}</language></description>
    <link_rewrite><language id="1">{slug}</language></link_rewrite>
    <visibility><![CDATA[both]]></visibility>
    <associations>
      <categories>
        <category><id>{category_id}</id></category>
      </categories>
      <stock_availables>
        <stock_available>
          <id>0</id>
          <id_product_attribute>0</id_product_attribute>
          <quantity>10</quantity>
        </stock_available>
      </stock_availables>
    </associations>
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
    """
    images_folder: path to your local images
    image_files: list of filenames
    """
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
        pid = get_or_create_product(prod, load_category_cache(), load_manufacturer_cache())
        print(f"Created product {prod['name']} -> ID {pid}")

        upload_product_images(pid, "../scrapper_results/images", prod["images"])
        



def delete_all_products_and_images():
    """
    Deletes all products and any leftover images in PrestaShop via Webservice.
    """
    # Step 1: Get all product IDs
    r = requests.get(f"{API_URL}/products?display=[id]", auth=(API_KEY, ""))
    if r.status_code != 200:
        print("Failed to fetch products:", r.text)
        return

    root = ET.fromstring(r.text)
    product_ids = [int(node.find("id").text) for node in root.findall(".//product")]
    print(f"Found {len(product_ids)} products.")

    # Step 2: Delete each product and its images
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


# delete_all_products_and_images()


upload_products_and_images()