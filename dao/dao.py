import dao.connect 
from readerwriterlock import rwlock
import traceback
import dao.queries as queries

# Import the module and import hooks
#import jpype
#import jpype.imports
#from jpype import JByte, JInt, JString, JException, JObject

# Start the jvm so we can access java 
#jpype.startJVM(jpype.getDefaultJVMPath())

# Import a java class
#import java.sql.Timestamp
#from java.lang import String
#import java.lang
#import java.util
# Use it to create an object
#print(java.sql.Timestamp(1515628800*1000))

# SQL Queries


class Dao:
    """Data Access Object"""

    def __init__(self): # Done
        self.conn = dao.connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None
        #self.pencil = rwlock.RWLockFair()

    def get_my_courses(self, bid): # Done
        """Kurse eines bestimmten Benutzer zurückgeben"""
        course_curs = self.conn.cursor()
        res = [] 
        try:
            course_curs.execute(queries.my_courses, (bid,))
            res = course_curs.fetchall()
        except Exception as e:
            print(e)
            self.conn.rollback()
        finally:
            course_curs.close()
        return sorted(res)


    def get_available_courses(self, bid): # Done
        """Verfügbare Kurse zurückgeben"""
        all_other_courses_curs = self.conn.cursor()
        res = []
        try:
            all_other_courses_curs.execute(queries.available_courses, (bid,))
            res = all_other_courses_curs.fetchall()
            self.completion()
        except Exception as e:
            print(e)
        finally:
            all_other_courses_curs.close()
            self.close()
        return sorted(res)


    def add_course(self, name, desc, spaces, creator, key=None): # Done
        """Kurs erstellen"""
        add_course_curs = self.conn.cursor()
        error = None
        try:
            if key == None or str(key).isspace():
                add_course_curs.execute(queries.add_course_no_key, 
                    (name, desc, creator, spaces))
            else:
                add_course_curs.execute(queries.add_course_with_key,
                    (name, desc, creator, spaces, key))
            self.completion()
        except Exception as e:
            error = e
            #self.conn.rollback()
        finally:
            add_course_curs.close()
            self.close()
        return error

    def is_registered(self, bid, kid): # Done
        """Prüfen, ob ein Benutzer registriert ist"""
        reg_curs = self.conn.cursor()
        try:
            reg_curs.execute(queries.is_reg, (bid, kid))
            reg = reg_curs.fetchall()
            #self.completion()
        except Exception as e:
            return e
        finally:
            reg_curs.close()
            #self.close()
        if len(reg) == 0:
            return False
        else:
            return True

    def get_course_details(self, kid): # Done
        """Beschreibung eines Kurses zurückliefern"""
        course_details_curs = self.conn.cursor()
        try:
            course_details_curs.execute(queries.course_details, (kid,))
            res = course_details_curs.fetchone()
            #self.completion()
        except Exception as e:
            return e
        finally:
            course_details_curs.close()
            #self.close()
        return res

    def get_exercises(self, kid, bid): #no commit, TODO
        """Aufgaben und zugehörige Abgaben (wenn vorhanden) zurückliefern"""
        ex_list_curs = self.conn.cursor()
        res = []
        try:
            ex_list_curs.execute(queries.exercises, (kid, bid, kid, bid))
            res = ex_list_curs.fetchall()
            #self.completion()
        except Exception as e:
            print(e)
        finally:
            ex_list_curs.close()
        return res


    def get_ex_details(self, kid, anummer): #  Done
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


    def get_key(self, kname, ersteller):  # No longer used
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

 
    def get_course_owner(self, kname):  # No longer used
        """Id des Erstellers eines Kurses zurückliefern. wir gehen davon aus, dass
        jede Benutzer nur einen Kurs derselben Namen erstellen kann"""

        owner_curs = self.conn.cursor()
        owner_query = """select ersteller from kurs where name=?"""
        owner_curs.execute(owner_query, (kname,))
        owner = owner_curs.fetchone()[0]

        #print(owner)

        return owner

    def get_course_key(self, kid):  # Query to be added to queries
        """Einschreibeschlüssel für einen Kurs zurückliefern"""
        get_key_query = """select einschreibeschluessel from kurs where kid=?"""
        get_key_curs = self.conn.cursor()

        get_key_curs.execute(get_key_query, (kid,))
        res = get_key_curs.fetchone()
        return res[0]


    def add_to_locked_course(self, bnummer, kid, key=None): # Query to be added to queries
        """
        Ein Benutzer schreibt sich ein, der Kurs enthält einen Schlüssel
        """

        add_to_course_curs = self.conn.cursor()

        print(key, self.get_course_key(kid))

        if (key == self.get_course_key(kid)):
            try:
                add_to_course_curs.execute(queries.add_to_course, (bnummer, kid))
                self.completion()
            except Exception as e:
                print(e)
                self.conn.rollback()
                return None
            finally:
                add_to_course_curs.close()
                self.close()
            return True
        else:
            return False
        
    def add_to_course(self, bnummer, kid):
        """
        Ein Benutzer schreibt sich ein, der Kurs enthält keinen Schlüssel
        """
        add_to_course_curs = self.conn.cursor()
        try:
            add_to_course_curs.execute(queries.add_to_course, (bnummer, kid))
            self.completion()
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            add_to_course_curs.close()
            self.close()
        return True



    def submission_exists(self, bid, kid, anummer): # No longer used
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

    def add_sub_text(self, text): # Done
        """Abgabe in Datenbank hinzufügen"""
        sub_text_curs = self.conn.cursor()

        try:
            sub_text_curs.execute(queries.sub_text, (text,))
            self.conn.commit
        except Exception as e:
            return False
            self.conn.rollback()
        finally:
            sub_text_curs.close()
            #self.close()
        return True

    def get_aid(self, text): # Done
        """Aufgabe id zurückliefern"""
        aid_curs = self.conn.cursor()
        res = None
        try:
            aid_curs.execute(queries.aid, (text,))
            res = aid_curs.fetchone()[0]
            #self.conn.commit()
            #self.completion()
            return res
        except Exception as e:
            #self.conn.rollback()
            #return None
            pass
        finally:
            aid_curs.close()

    def add_sub_ref(self, bid, kid, anummer, aid): # Done
        """Eine Abgabe in die Tabelle Einreichen einfügen"""
        sub_ref_curs = self.conn.cursor()
        #res = False
        try:
            if aid is not None:
                sub_ref_curs.execute(queries.submission_ref, (bid, kid, anummer, aid))
                #res = sub_ref_curs.fetchone()
                self.conn.commit()
                #self.completion()
            return True
        except Exception as e:
            #self.conn.rollback()
            return e
        finally:
            sub_ref_curs.close()
            #self.close()

    def delete_course(self, kid):
        """
        Löscht einen Kurs aus den Datenbank
        """
        del_curs = self.conn.cursor()
        try:
            del_curs.execute(queries.delete1, (kid,))
            del_curs.execute(queries.delete2, (kid,))
            del_curs.execute(queries.delete3, (kid,))
            del_curs.execute(queries.delete4, (kid,))
            del_curs.execute(queries.delete5, (kid,))
            self.completion()
            return True
        except Exception as e:
            self.conn.rollback()
            return e
        finally:
            del_curs.close()
            self.close()



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
