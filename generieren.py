import random
import csv
import os

class Karte:
    def __init__(self, farbe, wert):
        self.farbe = farbe
        self.wert = wert

    def __str__(self):
        return f"{self.farbe} {self.wert}"

class Deck:
    def __init__(self):
        self.karten = []
        self.farben = ['Herz', 'Karo', 'Pik', 'Kreuz']
        self.werte = ['7', '8', '9', '10', 'Bube', 'Dame', 'König', 'Ass']
        for farbe in self.farben:
            for wert in self.werte:
                self.karten.append(Karte(farbe, wert))
        random.shuffle(self.karten)

    def ziehe_karte(self):
        return self.karten.pop() if self.karten else None

    def numerische_zu_karte(self, nummer):
        if nummer == -1:
            return None
        farbe_index = nummer // 8
        wert_index = nummer % 8
        return Karte(self.farben[farbe_index], self.werte[wert_index])

    def karte_zu_numerisch(self, karte):
        farben = {'Herz': 0, 'Karo': 1, 'Pik': 2, 'Kreuz': 3}
        werte = {'7': 0, '8': 1, '9': 2, '10': 3, 'Bube': 4, 'Dame': 5, 'König': 6, 'Ass': 7}
        return farben[karte.farbe] * 8 + werte[karte.wert]

class MauMau:
    def __init__(self):
        self.deck = Deck()
        self.ablagestapel = [self.deck.ziehe_karte()]
        self.spieler_hand = [self.deck.ziehe_karte() for _ in range(7)]
        self.ki_hand = [self.deck.ziehe_karte() for _ in range(7)]
        self.zuege = []
        self.max_hand_laenge = 7  # Stellt sicher, dass die Handlänge konsistent ist

    def zufalls_ki_zug(self, hand):
        moegliche_zuege = [karte for karte in hand if karte.farbe == self.ablagestapel[-1].farbe or karte.wert == self.ablagestapel[-1].wert]
        if moegliche_zuege:
            gewaehlte_karte = random.choice(moegliche_zuege)
            hand.remove(gewaehlte_karte)
            self.ablagestapel.append(gewaehlte_karte)
            return gewaehlte_karte
        else:
            gezogene_karte = self.deck.ziehe_karte()
            if gezogene_karte:
                hand.append(gezogene_karte)
            return gezogene_karte

    def konvertiere_hand_zu_text(self, numerische_hand):
        return [str(self.deck.numerische_zu_karte(nummer)) for nummer in numerische_hand if nummer != -1]

    def spielzug_aufzeichnen(self, spieler, hand, gezogene_karte):
        numerische_hand = [self.deck.karte_zu_numerisch(karte) for karte in hand]
        text_hand = ','.join(self.konvertiere_hand_zu_text(numerische_hand))
        ablage = str(self.ablagestapel[-1])
        if gezogene_karte:
            zug = f'ziehen {gezogene_karte}'
        else:
            zug = f'spielen {self.ablagestapel[-1]}'

        self.zuege.append([spieler, text_hand, ablage, zug])

    def spiel_starten(self):
        max_zuege = 100  # Maximal erlaubte Züge pro Spiel, um Endlosschleifen zu verhindern
        zaehler = 0
        while self.spieler_hand and self.ki_hand and zaehler < max_zuege:
            # Spielerzug
            gezogene_karte = self.zufalls_ki_zug(self.spieler_hand)
            self.spielzug_aufzeichnen('Spieler', self.spieler_hand, gezogene_karte)
            
            if not self.spieler_hand:
                break

            # KI-Zug
            gezogene_karte = self.zufalls_ki_zug(self.ki_hand)
            self.spielzug_aufzeichnen('KI', self.ki_hand, gezogene_karte)

            zaehler += 1

    def daten_speichern(self, datei_name):
        # Überprüfen, ob der Ordner existiert, falls nicht, wird er erstellt
        if not os.path.exists('spielstaende'):
            os.makedirs('spielstaende')

        # Speichern der CSV-Datei im Unterordner 'spielstaende'
        pfad = os.path.join('spielstaende', datei_name)
        with open(pfad, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Spieler', 'Hand', 'Ablagestapel', 'Aktion'])
            writer.writerows(self.zuege)

if __name__ == "__main__":
    anzahl_spiele = 10000  # Anzahl der Spiele, die simuliert werden sollen
    for i in range(anzahl_spiele):
        spiel = MauMau()
        spiel.spiel_starten()
        spiel.daten_speichern(f'spiel_daten_{i}.csv')
