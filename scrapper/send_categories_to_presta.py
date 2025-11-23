from config import API_KEY, API_URL, HEADERS
import requests
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET


CATEGORY_CACHE = Path("category_ids.json")

def slugify(text):
    t = text.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


def load_category_cache():
    if CATEGORY_CACHE.exists():
        return json.loads(CATEGORY_CACHE.read_text())
    return {}


def save_category_cache(cache):
    CATEGORY_CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))



def get_or_create_category(name):
    cache = load_category_cache()

    if name in cache:
        return cache[name]

    # read existing categories
    r = requests.get(
        f"{API_URL}/categories",
        auth=(API_KEY, "")
    )

    if r.status_code != 200:
        print(r.text)
        raise Exception("Cannot read categories")   

    root = ET.fromstring(r.text)
    existing_ids = [int(node.attrib["id"]) for node in root.findall(".//category")]

    for cid in existing_ids:
        rc = requests.get(f"{API_URL}/categories/{cid}", auth=(API_KEY, ""))
        if rc.status_code == 200:
            rc_xml = ET.fromstring(rc.text)
            cat_name = rc_xml.find(".//name/language").text
            if name == cat_name:
                cache[name] = cid
                save_category_cache(cache)
                return cid


    link_rewrite = slugify(name)

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
  <category>
    <id_parent>2</id_parent>
    <active>1</active>
    <name><language id="1">{name}</language></name>
    <link_rewrite><language id="1">{link_rewrite}</language></link_rewrite>
  </category>
</prestashop>
"""

    r = requests.post(
        f"{API_URL}/categories",
        data=xml.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        auth=(API_KEY, "")
    )

    if r.status_code not in (200, 201):
        print(r.text)
        raise Exception(f"Failed to create category {name}")

    # parse ID from response
    created = ET.fromstring(r.text)
    new_id = int(created.find(".//id").text)

    cache[name] = new_id
    save_category_cache(cache)
    return new_id


def upload_categories():
    with open("../scrapper_results/json/categories.json", 'r', encoding='utf-8') as f:
        categories = json.load(f)
    
    for cat in categories:
        cat_id = get_or_create_category(cat['name'])
        print(f"Category: {cat['name']} -> ID {cat_id}")
        
        if cat['subcategories'] is not None:    
            for subcat in cat['subcategories']:
                cat_id2 = get_or_create_category(subcat['name'])
            
                print(f"Category: {subcat['name']} -> ID {cat_id2}")


def delete_all_categories():
    r = requests.get(f"{API_URL}/categories", auth=(API_KEY, ""))
    if r.status_code != 200:
        print(r.text)
        raise Exception("Cannot read categories list")

    root = ET.fromstring(r.text)
    category_ids = [int(node.attrib["id"]) for node in root.findall(".//category")]

    print("Found:", category_ids)

    for cid in category_ids:
        if cid in (1, 2):
            print(f"Skipping category {cid} (root/home)")
            continue
        
        print(f"Deleting category {cid}...")
        dr = requests.delete(f"{API_URL}/categories/{cid}", auth=(API_KEY, ""))
        
        if dr.status_code in (200, 204):
            print(f"Deleted category {cid}")
        else:
            print(f"Failed deleting {cid}: {dr.status_code} – {dr.text}")

    print("Done.")


delete_all_categories()


# it works!
# upload_categories()

