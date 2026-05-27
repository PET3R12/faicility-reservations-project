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
- Przykładowe użycie aplikacji jest w pliku `main.py` - trzeba go uruchomić

## Testy:
Raport w formacie html możan utworzyć komendą:
```bash
uv run pytest tests/ --cov=src --cov-report=html
```
lub przez uv:
```bash
pytest tests/ --cov=src --cov-report=html
```

