# Projekt na przedmiot "Przedmiot Fakultatywny"
## **Temat**: System rezerwacji hoteli
## Instalacja zależności:
- zależności można zainstalować na podstawie pliku `requirements.txt` komendą:
```bash
pip install -r requirements.txt
```
 - podczas pisania projektu używałem narzędzia [uv](https://docs.astral.sh/uv/), więc można też zainstalować zależności za pomocą komendy:
 ```bash
 uv sync
 ```
## Aplikacja:
- Główne klasy:
	- `User` 
	- `Reservation`
	- `Facility`
	- `FacilityReview`
- Klasy pośrednie typu: 
	- `Contact`
	- `ReservationManager`
	- `PhoneNumber`
	- Klasy typu `Exception`
- Działanie aplikacji:
	- `User` może tworzyć `Reservations`, które muszą spełniać określone warunki (dany obiekt nie może mieć już rezerwacji w danym przedziale czasowym, nie można zrobić rezerwacji w przeszłości i rezerwacja nie może być dłuższa niż miesiąc)
	- `User` może też dodawać `FacilityReview` dla danego obiektu. Recenzja zawiera ocenę liczbową, która musi być liczbą całkowitą w przedziale od 1 do 5
	- `ReservationManager` sczytuje informacje z `data_reservations.json` i weryfikuje, czy obiekt nie jest zarezerwowany i jeżeli nie jest to dodaje do listy rezerwacji tą rezerwację.
- Przykładowe użycie aplikacji jest w pliku `main.py` - trzeba go uruchomić
	- w pliku `data_reservations.json` jest zapisany wynik wywołania `main.py`
- Aplikacja wypisuje komunikaty przez logi za pomocą biblioteki `loguru`, i zapisuje je w pliku `logs/app.log`

## Testy:
Raport w formacie html można utworzyć komendą:
```bash
uv run pytest tests/ --cov=src --cov-report=html
```
lub przez uv:
```bash
pytest tests/ --cov=src --cov-report=html
```
## Workflows
Dałem testy `black` i `flake8` aby poprawiało format kodu i bot commituje poprawiony jak nie jest