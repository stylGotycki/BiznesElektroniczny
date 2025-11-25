# Biznes Elektroniczny — Projekt PrestaShop - Studio Klameczek

Projekt **Studio Klameczek** to nowoczesny sklep internetowy z akcesoriami do drzwi (klameczki, stopery, szyldy, zamki) stworzony w ramach zajęć z Biznesu Elektronicznego. Sklep oparty jest na platformie **PrestaShop 1.7.8** i uruchamiany w środowisku **Docker/docker-compose**, co zapewnia łatwość wdrożenia i spójność środowiska.

Dane produktowe (1000 produktów) zostały automatycznie pobrane i zaimportowane za pomocą dedykowanego skryptu scrapującego oraz skryptu API REST. Interfejs użytkownika jest zbliżony do sklepu źródłowego i w języku polskim.

---

##  Wersja Oprogramowania

* **Platforma Sklepu:** **PrestaShop 1.7.8**
* **Baza Danych:** **MariaDB 10.4** (w kontenerze Docker)
* **Wersja PHP w kontenerze:** PHP 7.4
* **Narzędzie do Testów Automatycznych:** **Selenium (Python)**
* **Język Scrapera/API Skryptu:** Python 3

---

## Skład Zespołu

| Imię i Nazwisko | Numer Indeksu |
| :--- | :--- |
| Tamara Mruk | 197584 |
| Filip Domaszk | 197624 |
| Konrad Pawłowski | 197823 |
| Filip Mikulski | 198225 |

---

## Struktura Repozytorium

Repozytorium jest zorganizowane zgodnie z wymaganiami projektu. **Wersjonowany jest tylko kod źródłowy.**

BiznesElektroniczny/            
├── .gitignore # Określa zasoby niepodlegające wersjonowaniu (cache, uploady, itd.).          
├── docker-compose.yml # Konfiguracja środowiska Docker/docker-compose.          
├── README.md # Niniejszy plik z opisem projektu i instrukcjami.         
├── prestashop/ # Główny folder z instalacją PrestaShop.       
├── scrapper_results/ # Wyniki scrapowania.       
├── scrapper/ # Kod źródłowy narzędzia do scrapowania danych.      
├── selenium_test/ # Kod źródłowy skryptu do testowania Selenium    
└── prestashop_dump.sql # Eksport ustawień sklepu (umożliwia przywrócenie).         

##  Wymagania i Uruchomienie Sklepu

Sklep wymaga **Docker** oraz **Docker Compose** do uruchomienia. Obsługuje żądania wyłącznie poprzez **HTTPS** (za pomocą samodzielnie wygenerowanego i podpisanego certyfikatu SSL).

### 1. Wymagania Wstępne

* Docker
* Docker Compose

### 2. Uprawnienia (Opcjonalnie)

Przed pierwszym uruchomieniem może być konieczne nadanie odpowiednich uprawnień plikom PrestaShop w folderze `prestashop/`:

```bash
# Uruchom w głównym katalogu projektu, jeśli wystąpią problemy z zapisem
sudo chown -R www-data:www-data prestashop/
sudo chmod -R 755 prestashop/
```
### 3. Uruchomienie kontenerów
```bash
# Uruchomienie kontenerów w tle
docker compose up -d
```

### 4. Załadowanie bazy
```
docker exec -i bizneselektroniczny-db-1 mysql -u prestashop -pprestashop prestashop < prestashop_dump.sql
```

### 5. Dostęp do Sklepu

Klient (Strona Główna)	HTTPS	https://localhost:8080/              
Panel Administracyjny	HTTPS	https://localhost:8080/admin449bvzhnr             
login: mruktamara64@gmail.com           
pass: klameczkipl321         

### 6. Sql dump
```bash
# Opcjonalny sql dump w celu zapisu konfiguracji/produktów
docker exec bizneselektroniczny-db-1 mysqldump -u prestashop -pprestashop prestashop > prestashop_dump.sql
```






























