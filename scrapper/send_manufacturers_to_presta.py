from config import API_KEY, API_URL, HEADERS
import requests
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET


MANUFACTURER_CACHE = Path("manufacturers_ids.json")


def load_manufacturer_cache():
    if MANUFACTURER_CACHE.exists():
        return json.loads(MANUFACTURER_CACHE.read_text())
    return {}

def save_manufacturer_cache(cache):
    MANUFACTURER_CACHE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))


def get_or_create_manufacturer(name):
    cache = load_manufacturer_cache()

    if name in cache:
        return cache[name]

    r = requests.get(f"{API_URL}/manufacturers", auth=(API_KEY, ""))
    if r.status_code != 200:
        print(r.text)
        raise Exception("Cannot read manufacturers list")

    root = ET.fromstring(r.text)
    existing_ids = [int(node.attrib["id"]) for node in root.findall(".//manufacturer")]

    for mid in existing_ids:
        rc = requests.get(f"{API_URL}/manufacturers/{mid}", auth=(API_KEY, ""))
        if rc.status_code != 200:
            continue

        rc_xml = ET.fromstring(rc.text)
        m_name = rc_xml.find(".//name").text

        if m_name == name:
            cache[name] = mid
            save_manufacturer_cache(cache)
            return mid

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<prestashop xmlns:xlink="http://www.w3.org/1999/xlink">
  <manufacturer>
    <active>1</active>
    <name>{name}</name>
  </manufacturer>
</prestashop>
"""

    r = requests.post(
        f"{API_URL}/manufacturers",
        data=xml.encode("utf-8"),
        headers={"Content-Type": "application/xml"},
        auth=(API_KEY, "")
    )

    if r.status_code not in (200, 201):
        print(r.text)
        raise Exception(f"Failed to create manufacturer {name}")

    created = ET.fromstring(r.text)
    new_id = int(created.find(".//id").text)

    cache[name] = new_id
    save_manufacturer_cache(cache)
    return new_id


def upload_manufacturers():
    with open("../scrapper_results/json/manufacturers.json", "r", encoding="utf-8") as f:
        manufacturers = json.load(f)

    for m in manufacturers:
        mid = get_or_create_manufacturer(m["name"])
        print(f"Manufacturer: {m['name']} -> ID {mid}")


def delete_all_manufacturers():
    r = requests.get(f"{API_URL}/manufacturers", auth=(API_KEY, ""))
    if r.status_code != 200:
        print(r.text)
        raise Exception("Cannot read manufacturers list")

    root = ET.fromstring(r.text)
    manufacturer_ids = [int(n.attrib["id"]) for n in root.findall(".//manufacturer")]

    print("Found manufacturers:", manufacturer_ids)

    for mid in manufacturer_ids:
        print(f"Deleting manufacturer {mid}...")
        dr = requests.delete(f"{API_URL}/manufacturers/{mid}", auth=(API_KEY, ""))

        if dr.status_code in (200, 204):
            print(f"Deleted {mid}")
        else:
            print(f"Failed deleting {mid}: {dr.status_code} – {dr.text}")

    print("Done deleting manufacturers.")


delete_all_manufacturers()
      
# upload_manufacturers()