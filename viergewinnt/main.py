from typing import List
from random import randint

# Unser Spielfeld hat 7 Spalten und 6 Zeilen, daraus ergibt sich die Anzahl der Zellen
"""SPALTEN = 7
ZEILEN = 6
ZELLEN = SPALTEN * ZEILEN
# Die Richtungen dienen dazu, zu überprüfen, ob ein Spieler (in eine bestimmte Richtung) gewonnen hat.

# pos2Index geben wir eine Position(Key-Spalte, Zeile) und für diese Position vergeben wir einen
# Value (Index der betroffenen Quads)
pos2Index = defaultdict(list)
"""

ZAEHLER = 0
REIHE = 5
RICHTUNGEN = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]


class Spielfeld:
    def __init__(self):
        self.__felder = [[".", ".", ".", ".", ".", ".", "."],
                         [".", ".", ".", ".", ".", ".", "."],
                         [".", ".", ".", ".", ".", ".", "."],
                         [".", ".", ".", ".", ".", ".", "."],
                         [".", ".", ".", ".", ".", ".", "."],
                         [".", ".", ".", ".", ".", ".", "."]]
        self.__letzteSpalte = None
        self.__letzteReihe = None

    def getFelder(self) -> List:
        return self.__felder

    def setFelder(self, spalte: int):
        global REIHE
        self.__letzteSpalte = spalte
        geworfen = False
        for liste in reversed(self.__felder):
            if not geworfen:
                if liste[spalte] == ".":
                    if ZAEHLER % 2 == 0:
                        self.__felder[REIHE][spalte] = 'X'
                    else:
                        self.__felder[REIHE][spalte] = '0'
                    self.__letzteReihe = REIHE
                    geworfen = True
                elif liste[spalte] != ".":
                    REIHE -= 1
                    self.__letzteReihe = REIHE

    def getLetzteReihe(self) -> int:
        return self.__letzteReihe

    def getLetzteSpalte(self) -> int:
        return self.__letzteSpalte


class GUI:
    """

    """
    def __init__(self):
        pass

    def printSpielfeld(self, feld: Spielfeld):
        for liste in feld.getFelder():
            print(liste[0], liste[1], liste[2], liste[3], liste[4], liste[5], liste[6])

    def getSpielmodus(self) -> int:
        gueltigeModi = [1, 2]
        spielmodus = 0
        while spielmodus not in gueltigeModi:
            spielmodus = int(input(f'Willst du gegen einen Menschen (1) oder einen Computer (2) spielen?'))
            if spielmodus not in gueltigeModi:
                print(f'FALSCHE EINGABE! Willst du gegen einen Menschen (1) oder einen Computer (2) spielen?')
                continue
        return spielmodus

    def erfasseSpielzug(self):
        global ZAEHLER
        spalte = 0
        gueltige_spalten = [1, 2, 3, 4, 5, 6, 7]
        while spalte not in gueltige_spalten:
            spalte = int(input(f'In welche Spalte möchtest du werfen?'))
            if spalte not in gueltige_spalten:
                print("FALSCHE EINGABE! Wähle eine Spalte von 1 - 7")
            else:
                ZAEHLER += 1
                return spalte - 1


class Spielmodus:
    def __init__(self, spielmodus: int):
        if spielmodus == 1 or spielmodus == 2:
            self.__spielmodus = spielmodus
        else:
            raise ValueError("Falsche Eingabe! Gib 1 ein, wenn du gegen einen Mensch spielen willst oder 2,"
                             "wenn du gegen einen Computergegner spielen willst.")

    def __repr__(self):
        return f"Spielmodus: {self.__spielmodus}"

    @property
    def spielmodus(self):
        return self.__spielmodus

    @spielmodus.setter
    def spielmodus(self, value):
        self.__spielmodus = value

    def spielzug(self, gui: GUI) -> int:
        if self.__spielmodus == 1:
            spalte = gui.erfasseSpielzug()
            return spalte
        elif self.__spielmodus == 2:
            spalte = randint(0, 6)
            return spalte


class Spielregeln:
    def __init__(self):
        pass

    def volleSpalte(self, feld: Spielfeld, spalte: int) -> bool:
        spielfeld = feld.getFelder()
        if spielfeld[0][spalte] != ".":
            print("Spielzug nicht möglich. Spalte voll.")
            return False
        else:
            return True

    def voll(self) -> bool:
        if ZAEHLER < 42:
            return False
        else:
            return True

    def gewonnen(self, feld: Spielfeld) -> bool:
        spielfeld = feld.getFelder()
        #stein = 'O' if ZAEHLER % 2 == 0 else 'X'
        zeile = feld.getLetzteReihe()
        spalte = feld.getLetzteSpalte()
        for i in range(8):
                vier_in_einer_reihe = True
                for j in range(4):
                    spaltenpostion = spalte + RICHTUNGEN[i][0] * j
                    zeilenposition = zeile + RICHTUNGEN[i][1] * j
                    if spielfeld[zeile][spalte] == spielfeld[zeilenposition][spaltenpostion]:
                        continue
                    vier_in_einer_reihe = False
                    break
                if vier_in_einer_reihe:
                    return True

class DasSpiel:
    """
    Erstellt das Spiel.
    """

    def __init__(self):
        self.__feld = Spielfeld()
        self.__gui = GUI()
        self.__spielregeln = Spielregeln()
        self.spieler1 = Spielmodus(2)
        self.spieler2 = Spielmodus(2)

    def spielStart(self):
        spielmodus_spieler1 = self.__gui.getSpielmodus()
        self.spieler1.spielmodus = spielmodus_spieler1
        spielmodus_spieler2 = self.__gui.getSpielmodus()
        self.spieler2.spielmodus = spielmodus_spieler2
        self.__winner = None
        self.__gui.printSpielfeld(self.__feld)
        while True:
            ueberpruefe_spielzug_spieler1 = False
            spielzug_spieler_1 = None
            while not ueberpruefe_spielzug_spieler1:
                spielzug_spieler_1 = self.spieler1.spielzug(self.__gui)
                ueberpruefe_spielzug_spieler1 = self.__spielregeln.volleSpalte(self.__feld, spielzug_spieler_1)

            self.__feld.setFelder(spielzug_spieler_1)
            self.__gui.printSpielfeld(self.__feld)
            if self.__spielregeln.voll():
                print("Das Spielfeld ist voll. UNENTSCHIEDEN!")
                break
            if self.__spielregeln.gewonnen(self.__feld):
                print("Spieler 1 hat gewonnen!")
                break

            ueberpruefe_spielzug_spieler2 = False
            spielzug_spieler_2 = None
            while not ueberpruefe_spielzug_spieler2:
                spielzug_spieler_2 = self.spieler2.spielzug(self.__gui)
                ueberpruefe_spielzug_spieler2 = self.__spielregeln.volleSpalte(self.__feld, spielzug_spieler_2)

            self.__feld.setFelder(spielzug_spieler_2)
            self.__gui.printSpielfeld(self.__feld)
            if self.__spielregeln.voll():
                print("Das Spielfeld ist voll. UNENTSCHIEDEN!")
                break
            if self.__spielregeln.gewonnen(self.__feld):
                print("Spieler 2 hat gewonnen!")
                break


if __name__ == '__main__':
    game = DasSpiel()
    game.spielStart()


class Ki:
    def __init__(self):
        pass


"""
    def quadPositionen(position, richtung):
        positionen = set()
        spalte, zeile = position
        spaltenrichtung, zeilenrichtung = richtung
        neue_spalte, neue_zeile = spalte + spaltenrichtung * 3, zeile + zeilenrichtung * 3
        if neue_spalte < 0 or neue_spalte >= SPALTEN or neue_zeile < 0 or neue_zeile >= ZEILEN:
            return False
        for i in range(4):
            positionen.add((spalte + spaltenrichtung * i, zeile + zeilenrichtung * i))
        return positionen

    # Diese Funktion ermittelt die Quads
    def quadsErmitteln():
        zaehler = 0
        quads = {}
        bekannte_positionen = set()
        for i in range(ZELLEN):
            for richtung in RICHTUNGEN:
                position = (i % SPALTEN, i // SPALTEN)
                positionen = quadPositionen(position, richtung)
                if not positionen or positionen in bekannte_positionen:
                    continue
                quads[zaehler] = [0, 0]  # Anzahl der gelben[0], roten[1] Steine im Quad
                for position in positionen:
                    pos2Index[position].append([zaehler])
                bekannte_positionen.add(frozenset(positionen))
                # frozenset bewirkt, dass man einem set ein anderes set hinzufügen kann.
                zaehler += 1
        return quads


Die KI hat die folgende Funktionsweise:
Zuerst werden alle gültigen Quads gefunden. D.h. Es werden von allen Positionen(ZELLEN), in alle Richtungen
überprüft, ob es ein mögliches Quad gibt, um zu gewinnen.



def quadPositionen(position, richtung):
    positionen = set()
    spalte, zeile = position
    spaltenrichtung, zeilenrichtung = richtung
    neue_spalte, neue_zeile = spalte + spaltenrichtung * 3, zeile + zeilenrichtung * 3
    if neue_spalte < 0 or neue_spalte >= SPALTEN or neue_zeile < 0 or neue_zeile >= ZEILEN:
        return False
    for i in range(4):
        positionen.add((spalte + spaltenrichtung * i, zeile + zeilenrichtung * i))
    return positionen


# Diese Funktion ermittelt die Quads
def quadsErmitteln():
    zaehler = 0
    quads = {}
    bekannte_positionen = set()
    for i in range(ZELLEN):
        for richtung in RICHTUNGEN:
            position = (i % SPALTEN, i // SPALTEN)
            positionen = quadPositionen(position, richtung)
            if not positionen or positionen in bekannte_positionen:
                continue
            quads[zaehler] = [0, 0]  # Anzahl der gelben[0], roten[1] Steine im Quad
            for position in positionen:
                pos2Index[position].append([zaehler])
            bekannte_positionen.add(frozenset(positionen))
            # frozenset bewirkt, dass man einem set ein anderes set hinzufügen kann.
            zaehler += 1
    return quads


def findeTiefsteZeile(spalte):
    for zeile in reversed(range(ZEILEN)):
        if (spalte, zeile) not in spielfeld:
            return zeile


# Diese Funktion überprüft, ob die eingegebene Spalte gültig ist, der Wert für die Spalte darf 0-6 sein.
def spalteGueltig(spalte):
    if (spalte, 0) in spielfeld:
        return False
    if 0 <= spalte < 7:
        return True


# Diese Funktion gibt das aktuelle Spielfeld aus. Ein '.' steht für ein leeres Feld, in 'O' für einen Stein von
# Spieler 1 und ein 'X' für einen Stein von Spieler2.
def printSpielfeld():
    for i in range(ZELLEN):
        if i % SPALTEN == 0:
            print()
        position = (i % SPALTEN, i // SPALTEN)
        if position in spielfeld:
            print(spielfeld[position], end=' ')
        else:
            print('.', end=' ')
    print()


# Diese Funktion ersetzt die Funktion gewonnen
def steinSetzen(position, spieler):
    sieg = False
    spielfeld[position] = 'O' if spieler else 'X'
    for i in pos2Index[position]:
        quads[i][spieler] += 1
        if quads[i][spieler] == 4:
            sieg = True
    return sieg


# Diese Funktion dient der KI zum Löschen von Zügen die sie durchprobiert
def steinLoeschen(position, spieler):
    del spielfeld[position]
    for i in pos2Index[position]:
        quads[i][spieler] -= 1


# Diese Funktion bewertet das Spielfeld (die gesetzen Steine)
def bewerten():
    score = 0
    for position in spielfeld:
        for i in pos2Index[position]:
            gelbe, rote = quads[i]
            if gelbe > 0 and rote > 0:
                continue
            score += rote * 10
            score -= gelbe * 10
    return score


# Diese Funktion liefert alle möglichen Züge
def zugliste():
    zuege = []
    for spalte in range(SPALTEN):
        if not spalteGueltig(spalte):
            continue
        zeile = findeTiefsteZeile(spalte)
        zuege.append((spalte, zeile))
    return zuege


# Diese Funktion ist für einen echten zweiten Mitspieler bestimmt
def human(spieler):
    while True:
        spalte = int(input('In welche Spalte willst du setzen(0-6)?'))
        if spalteGueltig(spalte):
            break
    zeile = findeTiefsteZeile(spalte)
    sieg = steinSetzen((spalte, zeile), spieler)
    return sieg


# Diese Funktion ist für die KI bestimmt, dieser nimmt den zug mit dem höchsten score
def computer(spieler):
    bewertete_zuege = []
    for zug in zugliste():
        sieg = steinSetzen(zug, spieler)
        score = minimax(7, -999999, 999999, spieler, sieg)
        steinLoeschen(zug, spieler)
        bewertete_zuege.append((score, zug))
    bewertete_zuege.sort(reverse=spieler)
    score, bester_zug = bewertete_zuege[0]
    sieg = steinSetzen(bester_zug, spieler)
    print(bewertete_zuege)
    print(f'Spieler {1 if spieler else 2} setzt {bester_zug} mit der Bewertung {score}')
    return sieg


def minimax(tiefe, alpha, beta, spieler, sieg):
    if sieg:
        return 99999+tiefe if spieler else -99999-tiefe
    if tiefe == 0 or len(spielfeld) == ZELLEN:
        return bewerten()
    spieler = not spieler
    value = -999999 if spieler else 999999
    for zug in zugliste():
        sieg = steinSetzen(zug, spieler)
        score = minimax(tiefe - 1, alpha, beta, spieler, sieg)
        steinLoeschen(zug, spieler)
        if spieler:
            value = max(value, score)
            alpha = max(value, alpha)
        else:
            value = min(value, score)
            beta = min(value, beta)
        if alpha >= beta:
            break
    return value


spieler = True
quads = quadsErmitteln()
while True:
    printSpielfeld()
    if spieler:
        sieg = human(spieler)
    else:
        sieg = human(spieler)
    if sieg:
        printSpielfeld()
        print('GEWONNEN!!!')
        break
    spieler = not spieler

'''
    Der Ablauf des Spiels schaut folgendermaßen aus:
    Zuerst wird das leere Spielfeld ausgegeben.
    Danach wählt der/die erste SpielerIn eine Spalte aus in die er/sie den Stein werfen will.
    Es wird überprüft, ob die Eingabe der Spalte gültig ist. (Werte von 0-6 sind erlaubt.)
    Danach wird überprüft ob, der/die SpielerIn gewonnen hat. (4 Steine in eine bestimmte Richtung.)
    Falls, dass nicht der Fall ist wirft der nächste Spieler einen Stein.
    Es wird wieder die Gültigkeit der Spalte und ob gewonnen wurde überprüft.
    Dies wird solange durchgeführt, bis ein Spieler gewonnen hat oder das Spielfeld voll mit Steinen ist.
    '''
"""
