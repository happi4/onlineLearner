import dao.connect 
from readerwriterlock import rwlock
import traceback

class ApplicationDao:

    def __init__(self):
        self.conn = dao.connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None
        self.pencil = rwlock.RWLockFair()

    def get_my_courses(self, bid):
        """Kurse eines bestimmten Benutzer zurückgeben"""

        course_curs = self.conn.cursor()

        #courses_squery = """select kurs.name, benutzer.name, kurs.freieplaetze from kurs 
        #join benutzer on kurs.ersteller=benutzer.bnummer where ersteller=?"""

        #courses_squery = """(select kurs.name, benutzer.name, kurs.freieplaetze from benutzer 
        #join kurs on kurs.ersteller=benutzer.bnummer where kurs.ersteller=?) union 
        #(select kurs.name, benutzer.name, kurs.freieplaetze from benutzer join einschreiben 
        #on benutzer.bnummer=einschreiben.bnummer join kurs on kurs.kid=einschreiben.kid
        #where einschreiben.bnummer=?)"""

        #Only this is necessary
        courses_query = """select kurs.name, benutzer.name, kurs.freieplaetze from benutzer 
        join kurs on kurs.ersteller=benutzer.bnummer join einschreiben on 
        einschreiben.kid=kurs.kid where einschreiben.bnummer=?"""

        course_curs.execute(courses_query, (bid,))
        res = course_curs.fetchall()

        course_curs.close()
        
        return res


    def get_all_other_courses(self, bid):
        """Verfügbare Kurse zurückgeben"""

        all_other_courses_curs = self.conn.cursor()

        #all_courses_query = """select kurs.name, benutzer.name, kurs.freieplaetze from kurs 
        #join benutzer on kurs.ersteller=benutzer.bnummer where kurs.freieplaetze > 0 and 
        #kurs.ersteller!=?"""

        all_other_courses_query = """(select distinct kurs.name, benutzer.name, 
        kurs.freieplaetze from benutzer join kurs on kurs.ersteller=benutzer.bnummer 
        left join einschreiben on einschreiben.kid=kurs.kid) minus 
        (select kurs.name, benutzer.name, kurs.freieplaetze from benutzer 
        join kurs on kurs.ersteller=benutzer.bnummer join einschreiben on 
        einschreiben.kid=kurs.kid where einschreiben.bnummer=?)"""

        all_other_courses_curs.execute(all_other_courses_query, (bid,))
        res = all_other_courses_curs.fetchall()

        all_other_courses_curs.close()

        return res


    def add_course(self, course):
        """Neuer Kurs hinzufügen"""

    def get_course_details(self, kname, ersteller):
        """Beschreibung eines Kurses zurückliefern"""

        course_details_curs = self.conn.cursor()
        course_details_query = """select cast(beschreibungstext as varchar(3200)) from kurs 
        join benutzer on kurs.ersteller=benutzer.bnummer where kurs.name=? and benutzer.name=?"""


        course_details_curs.execute(course_details_query, (kname, ersteller))
        res = course_details_curs.fetchone()
        course_details_curs.close()

        if res is None:
            return None
        else:
            #print(res[0])
            return res[0]
        #desc = res[0]
        #kid = res[1]
        #print(desc, kid)
        #result = [(desc, kid)]

    def get_ex_details(self, kid, anummer): # check tomorow 4.01.2021
        """Details für Aufgaben zurückgeben"""

        desc_curs = self.conn.cursor()
        desc_query = """select cast(beschreibung as varchar(500)) from aufgabe kid=? and 
        anummer=?"""

        desc_curs.execute(desc_query, (kid, anummer))

        res = desc_curs.fetchone()

        res = res[0]

        if res is None:
            return None
        else:
            return res 



    #def get_bnummer()

    def get_kid(self, kname, ersteller): #change to bnummer
        """KursID eines Kurses zurückliefern"""

        kid_curs = self.conn.cursor()
        kid_query = """select kurs.kid from kurs join benutzer 
        on kurs.ersteller=benutzer.bnummer where kurs.name=? and benutzer.name=?"""

        kid_curs.execute(kid_query, (kname, ersteller))
        res = kid_curs.fetchone()
        kid_curs.close()

        if res is None:
            return None
        else:
            #print(res[0])
            return res[0]



    def get_key(self, kname, ersteller):
        """Kursschlüssel zurückliefern"""

        reg_key_curs = self.conn.cursor()
        reg_key_query = """select einschreibeschluessel from kurs join benutzer 
        on kurs.ersteller=benutzer.bnummer where kurs.name=? and benutzer.name=?"""

        reg_key_curs.execute(reg_key_query, (kname, ersteller))
        reg_key = reg_key_curs.fetchone()
        if reg_key is None:
            return None
        else:
            #print(reg_key[0])
            return reg_key[0]
        reg_key_curs.close()

 

    def get_course_owner(self, kname):
        """Id des Erstellers eines Kurses zurückliefern. wir gehen davon aus, dass
        jede Benutzer nur einen Kurs derselben Namen erstellen kann"""

        owner_curs = self.conn.cursor()
        owner_query = """select ersteller from kurs where name=?"""
        owner_curs.execute(owner_query, (kname,))
        owner = owner_curs.fetchone()[0]

        #print(owner)

        return owner


    def is_registered(self, bid, kid):
        """Prüfen, ob ein Benutzer registriert ist"""

        reg_curs = self.conn.cursor()
        reg_query = """select * from einschreiben where bnummer=? and kid=?"""
        reg_curs.execute(reg_query, (bid, kid))
        reg = reg_curs.fetchall()

        #print(len(reg))

        reg_curs.close()

        if len(reg) == 0:
            return False
        else:
            return True



    def get_ex_list(self, kid, bid):

        ex_list_curs = self.conn.cursor()
        ex_list_query = """select distinct aufgabe.anummer, aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), 
        cast(avg(cast(bewerten.note as decimal(2,1))) as decimal(2,1)) from kurs 
        join aufgabe on aufgabe.kid=kurs.kid left join einreichen 
        on einreichen.anummer=aufgabe.anummer right join abgabe 
        on abgabe.aid=einreichen.aid join bewerten on bewerten.aid=abgabe.aid 
        where kurs.kid=? and einreichen.bnummer=? group by aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer
        order by aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer"""

        ex_list_curs.execute(ex_list_query, (kid, bid))

        res = ex_list_curs.fetchall()

        if res is None:
            return False
        else:
            return res
    

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



    def submission_exists(self, bid, kid, anummer):
        """Prüfen, ob eine Abgabe für ein bnummer, kid und anummer schon existiert"""

        #sub_exists_lock = self.pencil.gen_rlock()

        sub_exists = 1

        sub_exists_curs = self.conn.cursor()
        sub_exists_query = """"select count(*) from einreichen where bnummer=? and kid=? and 
        anummer=?"""

        #with sub_exists_lock:
        sub_exists_curs.execute(sub_exists_query, (bid, kid, anummer))
        sub_exists = sub_exists_curs.fetchone()[0]

        sub_exists_curs.close()
        
        print(sub_exists)
        
        if sub_exists == 0:
            return True
        else:
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
