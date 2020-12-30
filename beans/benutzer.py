class Benutzer:
    def __ini__(self, bid, vorname, nachname, email):
        self.vorname = vorname
        self.nachname = nachname
        self.email = email
        self.bid = bid

    class Abgabe:
        def __init__(self, aid, text):
            self.aid = aid
            self.text = text
            self.noten = []
            self.kommentar = None

        def get_note(self):
            return sum(self.noten)/len(self.noten) # Durchschnittliche Note