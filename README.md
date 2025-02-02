# Galaxy-Chess

## Beschreibung
Das Schach-KI-Projekt kombiniert klassisches Schach mit galaktischen Elementen und bringt das Spiel in neue Dimensionen. Spieler treten gegen eine herausfordernde KI an, die mit strategischem Können und futuristischem Flair begeistert.

---

## Installation und Start des Spiels

### Voraussetzungen
- **Python-Version:** Das Projekt läuft mit **Python 3.10.12**. Bitte sicherstellen, dass die Python-Version korrekt installiert ist.
- **Bibliotheken:** 
  - `pygame` (für die grafische Oberfläche und Spiellogik)
  - `stockfish` (für die Integration und Strategie der KI)
- **Stockfish:** Installieren Sie eine kompatible Version der Stockfish-Engine (Pfad entsprechend den Betriebssystem-Anweisungen einrichten).

### Installierte Bibliotheken
Stellen Sie sicher, dass alle erforderlichen Bibliotheken installiert sind. Die Installation erfolgt über `pip`:
```bash
pip install pygame
pip install stockfish
```

### Projekt initialisieren
1. **Repository klonen:** Starten Sie ein Terminal und führen Sie folgendes aus:
   ```bash
   git clone https://github.com/SuperHueseyin/Galaxy-Chess.git
   cd Galaxy-Chess
   ```
---

## Startanleitung

### Programm ausführen
1. Wechseln Sie in das Projektverzeichnis.
2. Führen Sie das Programm mit folgendem Befehl aus:
   ```bash
   python main.py
   ```
3. Das Spiel startet in einem grafischen Fenster. Folgen Sie den Anweisungen, um gegen die KI anzutreten.

---

## Allgemeine Hinweise
- **Plattform-Support:** Dies ist ein plattformübergreifendes Projekt, das auf Windows und Linux läuft. Für den KI-Pfad (`Stockfish`) gibt es separate Pfade für die jeweilige Plattform.
- **Stockfish einrichten:** 
  - Für Ubuntu:
    ```python
    Stockfish(path="stockfish/linux/stockfish-ubuntu-x86-64", parameters={"Threads": 2, "Skill Level": 10})
    ```
  - Für Windows:
    ```python
    Stockfish(path="stockfish/win/stockfish-windows-x86-64-sse41-popcnt.exe", parameters={"Threads": 2, "Skill Level": 10})
    ```
- **Spielmodus:** Das Spiel wechselt zwischen menschlichem Spieler und KI. Der Spieler wählt vor Beginn seine Farbe (weiß/schwarz).

---

## Hinweise zur Softwarearchitektur
- **KI-Integration:** Die KI basiert auf der Stockfish-Engine und liefert herausfordernde Schachzüge.
- **Spiellogik:** Alle Spielfunktionen, einschließlich Validierung von Zügen, Rendering des Schachbretts und Umwandlung ins FEN-Format sind benutzerdefiniert implementiert.

Freuen Sie sich auf ein spannendes Spielerelebnis!
