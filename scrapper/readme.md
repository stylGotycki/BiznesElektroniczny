# Scrapper

Prosty scrapper, który ściąga dane produktów, włącznie ze zdjęciami.


## Odpalanie: 

Trzeba sobie zrobić foldery:

```
/scrapper-results
/scrapper-results/images
/scrapper-results/json
```

Trzeba odpalić sobie virtual env i pobrać biblioteki:

```
. /venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

Jak narazie nie zapisuje wyników w repo - jak to przetestuję to wrzucę tę zipbombę. 

Jak narazie obsługuje zapis do jsona. Zapis do presty będę robił dzisiaj jak wstanę (piszę to o 22.XI.2025 3:22)

P.S. trzeba chwilkę poczekać.

## todo

(delete this section later)
- [x] download categories data
    - [x] single category
    - [x] with subcategories

- [x] download products data
    - [x] single product
    - [x] assigning category 
    - [x] pagination
    - [x] images in png


- [x] save scrapped data to json

- [ ] post scrapped data to prestashop
    
