import dao.connect 
from readerwriterlock import rwlock
import traceback

class ApplicationDao:

    def __init__(self):
        self.conn = dao.connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None
        self.pencil = rwlock.RWLockFair()

    def get_courses(self, bid):
        """Kurse eines bestimmten Benutzer zurückgeben"""

        course_curs = self.conn.cursor()

        courses_squery = """select kurs.name, benutzer.name, kurs.freieplaetze from kurs 
        join benutzer on kurs.ersteller=benutzer.bnummer where ersteller=?"""

        course_curs.execute(courses_squery, bid)
        res = course_curs.fetchall()

        course_curs.close()
        
        return res


    def get_all_courses(self):
        """Verfügbare Kurse zurückgeben"""

        all_courses_curs = self.conn.cursor()

        all_courses_query = """select kurs.name, benutzer.name, kurs.freieplaetze from kurs 
        join benutzer on kurs.ersteller=benutzer.bnummer where kurs.freieplaetze > 0"""

        all_courses_curs.execute(all_courses_query)
        res = all_courses_curs.fetchall()

        all_courses_curs.close()

        return res


    def add_course(self, course):
        """Neuer Kurs hinzufügen"""



    #TODO: Break this method down
    def enroll(self, kname, bnummer, schluessel=None):
        """Ein benutzer schreibt sich ein"""

        row_count = 0
        register_lock = self.pencil.gen_wlock
        register_curs = self.conn.cursor()
        register_query = """insert into einschreiben (bnummer, kid) values(?, ?)"""

        # kid lesen
        get_kid_curs = self.conn.cursor()
        kid_lock = self.pencil.gen_rlock()
        kid=None
        get_kid_query = """select kid from kurs where name=? and ersteller=? """

        with kid_lock:    
            get_kid_curs.execute(get_kid_query, (kname, bnummer))
            kid = get_kid_curs.fetchone()[0]
        get_kid_curs.close()

        # freie Platz prüfen
        get_fp_curs = self.conn.cursor()
        fp_lock = self.pencil.gen_rlock()
        fp=None
        get_fp_query = """select 'True' from kurs where kid=? and freieplaetze>0"""
        if kid is not None:
            with fp_lock:
                get_fp_curs.execute(get_fp_query, (kid,))
                fp = get_fp_curs.fetchone()[0]
            get_fp_curs.close()

        # Anzahl der plaetze ist groesser als 0. Nur eine Kurseinschreibung pro Benutzer zulässig
        if fp == "True":
            check_exists_lock = self.pencil.gen_rlock()
            check_exists_curs = self.conn.cursor()
            check_exists_query = """select * from einschreiben where kid=? and bnummer=?"""

            with check_exists_lock:
                check_exists_curs.execute(check_exists_query, (kid, bnummer))

            #Keine einschreibung schon vorhanden für den kid und benutzer
            if check_exists_curs.rowcount == None or check_exists_curs.rowcount == -1:
                if schluessel is not None:
                    key = None
                    key_lock = self.pencil.gen_rlock()
                    key_curs = self.conn.cursor()
                    key_query = """select einschriebeschluessel from kurs where kid=? and 
                    ersteller=?"""
                    with key_lock:
                        key_curs.execute(key_query, (kid, bnummer))
                        key = key_curs.fetchone()[0]
                        self.conn.commit()  # Read before a write
                    key_curs.close()
                    
                    if key is not None and schluessel == key:
                        #register_lock = self.pencil.gen_wlock
                        #register_curs = self.conn.cursor()
                        #register_query = """insert into einschreiben (bnummer, kid) 
                        #values(?, ?)"""
                        
                        #register_lock.acquire()
                        with register_lock:
                            register_curs.execute(register_query, (bnummer, kid))
                            row_count = register_curs.rowcount
                        register_curs.close()

                        check_exists_curs.close()

                        #TODO: Decrement count on free places

                        if row_count == 1:
                            return True

                else: #keine schlüssel vorhanden
                    with register_lock:
                        register_curs.execute(register_query, (bnummer, kid))
                        row_count = register_curs.rowcount
                    register_curs.close()

                    check_exists_curs.close()

                    #TODO: Decrement count on free places

                    if row_count == 1:
                        return True 

            check_exists_curs.close()
        return False
            
                    







                    





            
            

        

        




    def completion(self):
        self.complete = True

    def close(self):
        if self.conn is not None:
            try:
                if self.complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                print(e)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    print(e)
