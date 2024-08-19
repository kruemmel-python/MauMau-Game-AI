
# MauMau-Game-AI

Dieses Projekt simuliert das Kartenspiel Mau Mau, bei dem eine Künstliche Intelligenz (KI) gegen einen menschlichen Spieler antritt. Das Projekt besteht aus drei Hauptkomponenten:

1. **Daten generieren**: Simulation von Mau-Mau-Spielen und Aufzeichnung der Züge in CSV-Dateien.
2. **Modell trainieren**: Erstellung und Training eines neuronalen Netzwerks basierend auf den simulierten Spieldaten.
3. **Gegen die KI spielen**: Spielen gegen die trainierte KI.

## Inhaltsverzeichnis

1. [Überblick](#überblick)
2. [Installation](#installation)
3. [Daten generieren (`generieren.py`)](#daten-generieren-generierenpy)
4. [Modell trainieren (`training.py`)](#modell-trainieren-trainingpy)
5. [Gegen die KI spielen (`spiel.py`)](#gegen-die-ki-spielen-spielpy)
6. [Zusammenfassung](#zusammenfassung)

## Überblick

Dieses Projekt verfolgt das Ziel, eine KI zu entwickeln, die das Kartenspiel Mau Mau spielt. Es verwendet maschinelles Lernen, um aus simulierten Spielen zu lernen und die optimale Spielstrategie zu entwickeln.

## Installation

1. **Klonen des Repositories:**
   ```bash
   git clone https://github.com/kruemmel-python/MauMau-Game-AI.git
   cd mau-mau-ki
   ```

2. **Installieren der Abhängigkeiten:**
   Erstelle eine virtuelle Umgebung und installiere die benötigten Python-Pakete:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Erstellen des `spielstaende`-Verzeichnisses:**
   ```bash
   mkdir spielstaende
   ```

## Daten generieren (`generieren.py`)

### Beschreibung

Das Skript `generieren.py` simuliert Tausende von Mau-Mau-Spielen zwischen zwei zufällig agierenden Spielern und speichert die Spieldaten in CSV-Dateien.

### Funktionsweise

- **Karte Klasse**: Definiert eine einzelne Karte mit den Attributen `farbe` und `wert`.
- **Deck Klasse**: Erstellt ein Kartendeck, mischt es und ermöglicht das Ziehen von Karten.
- **MauMau Klasse**: Simuliert ein vollständiges Mau-Mau-Spiel zwischen einem Spieler und einer KI:
  - **zufalls_ki_zug**: Die KI führt einen zufälligen Zug aus, entweder durch das Spielen einer passenden Karte oder durch Ziehen einer Karte.
  - **spielzug_aufzeichnen**: Speichert die Züge des Spiels in einem Datenarray.
  - **spiel_starten**: Führt das Spiel aus, bis ein Spieler gewinnt oder die maximale Anzahl von Zügen erreicht ist.
  - **daten_speichern**: Speichert die Spieldaten in CSV-Dateien.

### Verwendung

```bash
python generieren.py
```
Dieses Skript generiert 10.000 Spiele und speichert die Spieldaten als CSV-Dateien im Verzeichnis `spielstaende`.

## Modell trainieren (`training.py`)

### Beschreibung

Das Skript `training.py` lädt die generierten Spieldaten, bereitet sie für das Training vor, erstellt ein neuronales Netzwerk und trainiert dieses Modell.

### Funktionsweise

- **lade_daten**: Lädt alle CSV-Dateien aus dem Verzeichnis `spielstaende` und kombiniert sie zu einem DataFrame.
- **verarbeite_daten**: Wandelt die Karteninformationen in numerische Werte um und bereitet die Daten für das Modelltraining vor.
- **trainiere_modell**: Erstellt ein neuronales Netzwerk und trainiert es mit den verarbeiteten Daten. Verwendet einen Learning Rate Scheduler, um die Lernrate dynamisch anzupassen.

### Verwendung

```bash
python training.py
```
Dieses Skript lädt die generierten Spieldaten, trainiert das Modell und speichert es als `mau_mau_ki_model.keras`.

## Gegen die KI spielen (`spiel.py`)

### Beschreibung

Das Skript `spiel.py` lädt das trainierte Modell und ermöglicht es einem menschlichen Spieler, gegen die KI in einem Mau-Mau-Spiel anzutreten.

### Funktionsweise

- **Karte, Deck, MauMau Klassen**: Enthalten die Spielmechaniken und Regeln:
  - **7er-Regel**: Der Gegner muss zwei Karten ziehen, wenn eine 7 gespielt wird.
  - **8er-Regel**: Der Gegner muss eine Runde aussetzen, wenn eine 8 gespielt wird.
  - **Buben-Regel**: Der Spieler, der einen Buben legt, darf eine neue Farbe bestimmen.
- **spieler_zug und ki_zug**: Steuern die Züge des menschlichen Spielers und der KI.
- **beende_spiel**: Berechnet die Punkte und bestimmt den Gewinner des Spiels.

### Verwendung

```bash
python spiel.py
```
Dies startet ein Mau-Mau-Spiel gegen die KI.

## Zusammenfassung

Dieses Projekt bietet eine umfassende Simulation und KI-basierte Implementierung des Kartenspiels Mau Mau. Es umfasst die Datenaufzeichnung, das Training eines neuronalen Netzwerks und die Möglichkeit, gegen eine KI anzutreten. Durch die Simulation und das Modelltraining können verschiedene Strategien und Spielmechaniken untersucht und optimiert werden.

