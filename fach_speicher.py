import connect

class FachSpeicher:

    def __init__(self):
        self.conn = connect.DBUtil().getExternalConnection()
        self.conn.jconn.setAutoCommit(False)
        self.complete = None

    def add_course(self, course):
        """Neuer Kurs hinzufügen"""

        check_duplicates_curs = self.conn.cursor()
        create_course_curs = self.conn.cursor()
        select_course_curs = self.conn.cursor()

        if not course.schluessel and not course.schluessel.isspace():
            course.schluessel = "NULL"

        #Benutzer darf nicht derselbe Kursname benutzen
        check_duplicates = """SELECT * FROM kurs WHERE name=? AND ersteller=?"""
        check_duplicates_curs.execute(check_duplicates, (course.name, course.ersteller))
        duplicate = check_duplicates_curs.fetchall()
        print(len(duplicate))

        check_duplicates_curs.close()

        if len(duplicate) == 0:

            create_course_query = """INSERT INTO kurs(name, beschreibungstext, 
            einschreibeschluessel, freiePlaetze, ersteller) VALUES (?, ?, ?, ?, ?)"""
            create_course_curs.execute(create_course_query, (course.name, course.beschreibung, 
                                   course.schluessel, course.freie_plaetze, course.ersteller))
            create_course_curs.close()

            select_course_query = """SELECT kurs.kid FROM kurs JOIN benutzer 
            ON kurs.ersteller=benutzer.bnummer WHERE kurs.name=? AND kurs.ersteller=?"""
            select_course_curs.execute(select_course_query, (course.name, course.ersteller))
            course_id = select_course_curs.fetchall() #Get the KID for the course just created

            select_course_curs.close()
            
            return course_id[0][0] #Value as a tuple (num,)

        else:
            return None

        # name, bid, free_spots, desc, enroll_key
        # Do nothing if we have duplicates
            
        

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


