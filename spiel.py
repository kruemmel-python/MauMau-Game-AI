import random
import tensorflow as tf

class Karte:
    def __init__(self, farbe, wert):
        self.farbe = farbe
        self.wert = wert

    def __str__(self):
        return f"{self.farbe} {self.wert}"

class Deck:
    def __init__(self):
        self.karten = []
        farben = ['Herz', 'Karo', 'Pik', 'Kreuz']
        werte = ['7', '8', '9', '10', 'Bube', 'Dame', 'König', 'Ass']
        for farbe in farben:
            for wert in werte:
                self.karten.append(Karte(farbe, wert))
        random.shuffle(self.karten)

    def ziehe_karte(self):
        return self.karten.pop() if self.karten else None

class MauMau:
    def __init__(self, model, spieler_anzahl):
        self.deck = Deck()
        self.ablagestapel = [self.deck.ziehe_karte()]
        self.spieler_hand = []
        self.ki_hand = []
        self.model = model
        self.spieler_anzahl = spieler_anzahl
        self.karten_verteilen()
        self.spezial_karte_gelegt = False
        self.farbe_wunsch = None
        self.ki_muss_aussetzen = False

    def karten_verteilen(self):
        if self.spieler_anzahl in [2, 6]:
            karten_pro_spieler = 7
        elif self.spieler_anzahl in [3, 7]:
            karten_pro_spieler = 6
        else:
            karten_pro_spieler = 5
        
        self.spieler_hand = [self.deck.ziehe_karte() for _ in range(karten_pro_spieler)]
        self.ki_hand = [self.deck.ziehe_karte() for _ in range(karten_pro_spieler)]

    def mische_ablagestapel(self):
        if len(self.ablagestapel) > 1:
            letzte_karte = self.ablagestapel.pop()  # Die letzte abgelegte Karte bleibt auf dem Ablagestapel
            random.shuffle(self.ablagestapel)  # Mische den Rest des Ablagestapels
            self.deck.karten = self.ablagestapel  # Mache den Ablagestapel zum neuen Ziehstapel
            self.ablagestapel = [letzte_karte]  # Lege die letzte Karte wieder auf den Ablagestapel
            print("Der Ablagestapel wurde neu gemischt und als Ziehstapel verwendet.")
        else:
            print("Keine Karten mehr zum Mischen vorhanden!")

    def ziehe_karte(self):
        if not self.deck.karten:
            self.mische_ablagestapel()

        if self.deck.karten:
            return self.deck.ziehe_karte()
        else:
            return None

    def zug_moeglich(self, karte):
        # Bube-Regel: Bube kann auf jede Karte gelegt werden
        if karte.wert == 'Bube':
            return True
        
        # Wenn ein Farbwechsel durch einen Buben erwünscht ist, überprüfe die gewünschte Farbe
        if self.farbe_wunsch:
            return karte.farbe == self.farbe_wunsch
        
        # Normale Regel: Karte kann gespielt werden, wenn Farbe oder Wert übereinstimmen
        return (karte.farbe == self.ablagestapel[-1].farbe or 
                karte.wert == self.ablagestapel[-1].wert)

    def spezial_regeln(self, karte, ist_spieler):
        if karte.wert == '7':
            for _ in range(2):
                gezogene_karte = self.ziehe_karte()
                if gezogene_karte:
                    if ist_spieler:
                        self.ki_hand.append(gezogene_karte)
                    else:
                        self.spieler_hand.append(gezogene_karte)
            print(f"Zwei Karten wurden von {'der KI' if ist_spieler else 'dir'} gezogen.")
        elif karte.wert == '8':
            if ist_spieler:
                print("Die KI setzt aus.")
                self.ki_muss_aussetzen = True
            else:
                print("Du musst aussetzen.")
        elif karte.wert == 'Bube':
            neue_farbe = input("Wähle eine neue Farbe (Herz, Karo, Pik, Kreuz): ")
            self.farbe_wunsch = neue_farbe
            print(f"Farbwunsch: {self.farbe_wunsch}")
        else:
            # Wenn keine Spezialregel angewendet wird, wird der Farbwechsel zurückgesetzt
            self.farbe_wunsch = None
    
    def spieler_zug(self, mau_check=True):
        while True:
            print("Deine Handkarten:")
            for idx, karte in enumerate(self.spieler_hand):
                print(f"{idx}: {karte}")
            auswahl = input("Wähle eine Karte zum Spielen (Nummer) oder ziehe eine Karte (z): ")
            if auswahl == 'z':
                gezogene_karte = self.ziehe_karte()
                if gezogene_karte:
                    self.spieler_hand.append(gezogene_karte)
                    print(f"Du hast {gezogene_karte} gezogen.")
                else:
                    print("Keine Karten mehr im Deck und keine Möglichkeit mehr zu ziehen!")
                    self.beende_spiel()
                return
            else:
                try:
                    idx = int(auswahl)
                    gewaehlte_karte = self.spieler_hand[idx]
                    if self.zug_moeglich(gewaehlte_karte):
                        self.spieler_hand.remove(gewaehlte_karte)
                        self.ablagestapel.append(gewaehlte_karte)
                        print(f"Du spielst {gewaehlte_karte}.")
                        self.spezial_regeln(gewaehlte_karte, True)
                        if mau_check and len(self.spieler_hand) == 1:
                            print("Mau!")
                        if mau_check and not self.spieler_hand:
                            print("Mau Mau! Du hast gewonnen!")
                            self.beende_spiel()
                        return
                    else:
                        print("Diese Karte kann nicht gespielt werden. Wähle eine andere.")
                except (ValueError, IndexError):
                    print("Ungültige Auswahl. Versuche es erneut.")

    def ki_zug(self):
        if self.ki_muss_aussetzen:
            print("KI setzt aus.")
            self.ki_muss_aussetzen = False
            return

        moegliche_zuege = [karte for karte in self.ki_hand if self.zug_moeglich(karte)]
        
        if moegliche_zuege:
            gewaehlte_karte = random.choice(moegliche_zuege)
            self.ki_hand.remove(gewaehlte_karte)
            self.ablagestapel.append(gewaehlte_karte)
            print(f"KI spielt: {gewaehlte_karte}")
            self.spezial_regeln(gewaehlte_karte, False)
            if len(self.ki_hand) == 1:
                print("KI sagt Mau!")
            if not self.ki_hand:
                print("KI sagt Mau Mau! Die KI hat gewonnen!")
                self.beende_spiel()
        else:
            gezogene_karte = self.ziehe_karte()
            if gezogene_karte:
                self.ki_hand.append(gezogene_karte)
                print(f"KI zieht: {gezogene_karte}")
            else:
                print("Keine Karten mehr im Deck und keine Möglichkeit mehr zu ziehen!")
                self.beende_spiel()

    def beende_spiel(self):
        print("Das Spiel ist beendet.")
        spieler_punkte = self.punkte_berechnen(self.spieler_hand)
        ki_punkte = self.punkte_berechnen(self.ki_hand)
        print(f"Deine Punkte: {spieler_punkte}")
        print(f"KI-Punkte: {ki_punkte}")
        if spieler_punkte < ki_punkte:
            print("Du hast gewonnen!")
        elif spieler_punkte > ki_punkte:
            print("Die KI hat gewonnen!")
        else:
            print("Unentschieden!")
        exit()

    def punkte_berechnen(self, hand):
        punkte = 0
        werte = {'7': 7, '8': 8, '9': 9, '10': 10, 'Bube': 20, 'Dame': 10, 'König': 10, 'Ass': 11}
        for karte in hand:
            punkte += werte.get(karte.wert, 0)
        return punkte

    def spiel_starten(self):
        while self.spieler_hand and self.ki_hand:
            print(f"\nAblagestapel: {self.ablagestapel[-1]}")
            print(f"KI hat {len(self.ki_hand)} Karten.\n")

            self.spieler_zug()
            if not self.spieler_hand:
                return

            self.ki_zug()
            if not self.ki_hand:
                return

if __name__ == "__main__":
    model = tf.keras.models.load_model('mau_mau_ki_model.keras')
    spiel = MauMau(model, spieler_anzahl=2)  # Beispiel mit 2 Spielern
    spiel.spiel_starten()
