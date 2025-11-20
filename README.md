# Biznes Elektroniczny — Projekt PrestaShop - Studio Klameczek

Ten projekt uruchamia platformę **PrestaShop** przy użyciu **Docker Compose**.  
Zawiera kontener z PrestaShop oraz kontener z bazą danych **MariaDB**.             
Członkowie grupy :   
Tamara Mruk 197584              
Filip Domaszk    
Konrad Pawłowski     
Filip Mikulski       

-------------------------------------------------------------------------------------

## Struktura

BiznesElektroniczny/     
├── docker-compose.yml     # konfiguracja dockera            
├── .gitignore                    
├── prestashop/            # pliki prestashop              
├── prestashop_dump.sql    # sql dump                
└── README.md          


--------------------------------------------------------------------------------------

## Uruchomienie

### 1. Wymagania
- docker
- docker compose

### 2. Uprawnienia
```
chown -R www-data:www-data /var/www/html/
chmod -R 755 /var/www/html/
```


### 3. Uruchomienie kontenerow
```
docker compose up
```

### 4. Odpalanie strony
klient : http://localhost:8080     
admin : http://localhost:8080/adminxxxx  
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

## Stuff
readme do poprawy
