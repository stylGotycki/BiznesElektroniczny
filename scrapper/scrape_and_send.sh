#!/bin/bash


# scrape data
python3 main.py

# upload to presta
python3 send_categories_to_presta.py
python3 send_manufacturers_to_presta.py
python3 send_products_to_presta.py