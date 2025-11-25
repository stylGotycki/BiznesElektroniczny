import requests
import xml.etree.ElementTree as ET
import random

from config import API_KEY, API_URL, HEADERS


def get_product_ids():
    url = f"{API_URL}/products?display=[id]"
    r = requests.get(url, auth=(API_KEY, ""))
    root = ET.fromstring(r.text)

    product_ids = []
    for prod in root.findall(".//product"):
        id_node = prod.find("id")
        if id_node is not None and id_node.text:
            product_ids.append(int(id_node.text))

    return product_ids


def get_full_product(product_id):
    url = f"{API_URL}/products/{product_id}"
    r = requests.get(url, auth=(API_KEY, ""))
    return ET.fromstring(r.text)


def build_update_xml(product_id, weight):
    full_xml = get_full_product(product_id)
    product = full_xml.find("product")

    price = product.find("price").text
    tax_group = product.find("id_tax_rules_group").text

    name = product.find("name")
    link_rewrite = product.find("link_rewrite")

    update_root = ET.Element("prestashop", {
        "xmlns:xlink": "http://www.w3.org/1999/xlink"
    })

    update_product = ET.SubElement(update_root, "product")

    ET.SubElement(update_product, "id").text = str(product_id)
    ET.SubElement(update_product, "price").text = price
    ET.SubElement(update_product, "id_tax_rules_group").text = tax_group
    ET.SubElement(update_product, "weight").text = str(weight)

    name_copy = ET.SubElement(update_product, "name")
    name_copy.extend(list(name))

    lr_copy = ET.SubElement(update_product, "link_rewrite")
    lr_copy.extend(list(link_rewrite))

    return ET.tostring(update_root, encoding="utf-8")


def update_product_weight(product_id, weight):
    xml_data = build_update_xml(product_id, weight)

    url = f"{API_URL}/products/{product_id}"
    r = requests.put(
        url,
        auth=(API_KEY, ""),
        data=xml_data,
        headers={"Content-Type": "application/xml"}
    )

    print(f"[{r.status_code}] Updated product {product_id} → {weight} kg")
    if r.status_code >= 300:
        print(r.text)

    return r.status_code


def main():
    product_ids = get_product_ids()
    print("Found products:", product_ids)

    # first product → 100 kg
    update_product_weight(product_ids[0], 100.0)

    # remaining products → random weight
    for pid in product_ids[1:]:
        random_weight = round(random.uniform(0.01, 0.7), 2)
        update_product_weight(pid, random_weight)


if __name__ == "__main__":
    main()
