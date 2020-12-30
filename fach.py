import benutzer

class Kurs:
    def __init__(self, name, ersteller, freie_plaetze, beschreibung, schluessel=None):
        self.name = name 
        self.beschreibung = beschreibung
        self.schluessel = schluessel
        self.freie_plaetze = freie_plaetze
        self.ersteller = ersteller
        self.aufgaben = [] #speichert Aufgaben für einen Kurs
    

    class Aufgabe:
        def __init__(self, name, beschreibung):
            self._anummer = None
            self.name = name
            self.beschreibung = beschreibung
            self.abgabe = []

        def set_anummer(self, anummer):
            self._anummer = anummer

        def get_anummer(self):
            if self._anummer != None:
                return self._anummer
            else:
                return "Keine Aufgabenummer für diese Aufgabe verfügbar"
