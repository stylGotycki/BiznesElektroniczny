# Biznes Elektroniczny — Projekt PrestaShop - Studio Klameczek

Ten projekt uruchamia platformę **PrestaShop** przy użyciu **Docker Compose**.  
Zawiera kontener z PrestaShop oraz kontener z bazą danych **MariaDB**.

-------------------------------------------------------------------------------------

## Struktura

BiznesElektroniczny/     
├── docker-compose.yml     # konfiguracja dockera   
├── .gitignore     
├── prestashop/            # pliki prestashop     
└── README.md     


--------------------------------------------------------------------------------------

## Uruchomienie

### 1. Wymagania
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### 2. Uruchom kontenery
```
docker compose up
```

### 3. Odpalanie strony
klient : http://localhost:8080     
admin : http://localhost:8080/admin989ra7n38     
login : mruktamara64@gmail.com     
pass : klameczkapl321 


## Przydatne komendy

### Sprawdzenie aktywnych kontenerów
```
docker ps
```

### Wyłączenie kontenerów
```
docker stop <container_name_or_id>
```

### Wejście do wnętrza kontenera
```
docker exec -it <container_name_or_id> ls /var/www/html/
```

## Problemy
generalnie dziala to bardzo powolnie i ciezko, wydaje mi sie ze to kwestia docker <-> windows moment, narazie nie wiem co z tym zrobic
moze ktos bardziej ode mnie ogarnia :3
