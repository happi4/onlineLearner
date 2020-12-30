import dao

class FachSpeicher:

    def __init__(self):
        self.conn = dao.connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None


#def einreichen(self, agbage): #TODO

    def check_first(self, bnummer, kid):
        """Prüfen, ob ein Tupel ein Benutzer schon eingeschriben ist"""

        #results = []

        first_reg_curs = self.conn.cursor()

        first_reg_query = """SELECT kid FROM einschreiben WHERE bnummer=? AND kid=?"""
        first_reg_curs.execute(first_reg_query, (bnummer, kid))
        res = first_reg_curs.fetchall()

        first_reg_curs.close()

        #results.append(res)

        self.conn.commit()

        if res is None:  # Fix
            return True
        else:
            return False


    def space_available(self, kid):
        """Prüfen, ob Platz frei ist"""

        query_free_places_curs = self.conn.cursor()

        rows = []
        query_free_places = "SELECT freieplaetze FROM kurs WHERE kid=?"
        query_free_places_curs.execute(query_free_places, (kid,))
        free_places = query_free_places_curs.fetchone()

        #print(free_places)

        rows.append = free_places[0][2]
        #free_places = free_places[0][0]

        query_free_places_curs.close()

        type(free_places)
        #print(free_places)

        #if free_places > 0:
        if rows > 0:
            return free_places
        else:
            return 0

    def register(self, bnummer, kid):
        register_curs = self.conn.cursor()

        register_query = """INSERT INTO einschreiben(bnummer, kid) VALUES(?, ?)"""
        register_curs.execute(register_query, (bnummer, kid))  # Fix

        register_curs.close()

    def einschreiben(self, bnummer, kid, schluessel=None):
        """Benutzer einschreiben"""

        try:

            update_count_curs = self.conn.cursor()

            if self.space_available(kid) > 0:
                if self.check_first(bnummer, kid) == True:
                    self.register(bnummer, kid)

                    update_count_query = """UPDATE kurs SET freieplaetze=freieplaetze-1 WHERE kid=?"""
                    update_count_curs.execute(update_count_query, (kid))

            update_count_curs.close()

            self.completion = True
            self.conn.close()

        except Exception as e:
            #connection.abort()
            print(e)
