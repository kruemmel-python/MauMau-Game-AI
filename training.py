import os
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# 1. Daten laden
def lade_daten(verzeichnis):
    daten = []
    for datei in os.listdir(verzeichnis):
        if datei.endswith('.csv'):
            pfad = os.path.join(verzeichnis, datei)
            df = pd.read_csv(pfad, encoding='latin1')  # Encoding explizit setzen
            daten.append(df)
    return pd.concat(daten, ignore_index=True)

# 2. Feature-Engineering
def verarbeite_daten(daten):
    farben = {'Herz': 0, 'Karo': 1, 'Pik': 2, 'Kreuz': 3}
    werte = {'7': 0, '8': 1, '9': 2, '10': 3, 'Bube': 4, 'Dame': 5, 'König': 6, 'Ass': 7}

    def karte_zu_numerisch(karte):
        if pd.isna(karte) or not karte:
            return -1  # Für gezogene Karten oder fehlende Karten
        farbe, wert = karte.split()
        return farben[farbe] * 8 + werte[wert]

    daten['Hand'] = daten['Hand'].fillna('').astype(str)
    daten['Hand'] = daten['Hand'].apply(lambda hand: [karte_zu_numerisch(k) for k in hand.split(',')])
    daten['Ablagestapel'] = daten['Ablagestapel'].apply(karte_zu_numerisch)

    max_hand_laenge = daten['Hand'].apply(len).max()
    daten['Hand'] = daten['Hand'].apply(lambda hand: hand + [-1] * (max_hand_laenge - len(hand)))

    daten['Aktion'] = daten['Aktion'].apply(lambda aktion: 1 if 'spielen' in aktion else 0)

    X = daten[['Hand', 'Ablagestapel']]
    y = daten['Aktion']

    X = np.array([np.array(h + [a]) for h, a in zip(X['Hand'], X['Ablagestapel'])])

    return X, y

# 3. Modellierung und Training
def trainiere_modell(X, y, epochs=10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_train = X_train / np.max(X_train)
    X_test = X_test / np.max(X_test)

    if os.path.exists('mau_mau_ki_model.keras'):
        print("Bestehendes Modell wird geladen...")
        model = tf.keras.models.load_model('mau_mau_ki_model.keras')
    else:
        print("Neues Modell wird erstellt...")
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Learning Rate Scheduler hinzufügen
    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',  # Überwache die Validierungsverluste
        factor=0.5,          # Reduziere die Lernrate um den Faktor 0.5
        patience=3,          # Warte 3 Epochen, bevor die Lernrate reduziert wird
        min_lr=1e-6,         # Setze eine minimale Lernrate
        verbose=1            # Ausgabe, wenn die Lernrate reduziert wird
    )

    model.fit(
        X_train, y_train,
        epochs=epochs,
        validation_data=(X_test, y_test),
        callbacks=[lr_scheduler]  # Scheduler zu den Callbacks hinzufügen
    )

    model.save('mau_mau_ki_model.keras')

    return model

if __name__ == "__main__":
    daten = lade_daten('spielstaende')
    X, y = verarbeite_daten(daten)
    model = trainiere_modell(X, y, epochs=40)  # Beispiel mit 60 Epochen

    print("Training abgeschlossen und Modell gespeichert.")
