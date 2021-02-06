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

    def add_course(self, course):
        """Neuer Kurs hinzufügen"""

        #check_duplicates_curs = self.conn.cursor()
        #create_course_curs = self.conn.cursor()
        #select_course_curs = self.conn.cursor()

        #if not course.schluessel and not course.schluessel.isspace():
        #    course.schluessel = "NULL"

        #Benutzer darf nicht derselbe Kursname benutzen
        #check_duplicates = """SELECT * FROM kurs WHERE name=? AND ersteller=?"""
        #check_duplicates_curs.execute(check_duplicates, (course.name, course.ersteller))
        #duplicate = check_duplicates_curs.fetchall()

        #print("type of duplicate row: " + type(duplicate))

        #print(len(duplicate))

        #check_duplicates_curs.close()

        #if len(duplicate) == 0:

        #    create_course_query = """INSERT INTO kurs(name, beschreibungstext,
        #    einschreibeschluessel, freiePlaetze, ersteller) VALUES (?, ?, ?, ?, ?)"""
        #    create_course_curs.execute(create_course_query, (course.name, course.beschreibung,
        #                           course.schluessel, course.freie_plaetze, course.ersteller))
        #    create_course_curs.close()

        #    select_course_query = """SELECT kurs.kid FROM kurs JOIN benutzer
        #    ON kurs.ersteller=benutzer.bnummer WHERE kurs.name=? AND kurs.ersteller=?"""
        #    select_course_curs.execute(select_course_query, (course.name, course.ersteller))
        #    course_id = select_course_curs.fetchall() #Get the KID for the course just created

        #    select_course_curs.close()

        #    return course_id[0][0] #Value as a tuple (num,)

        #else:
        #    return None



    # Course creation
        def create_course(self, name, desc, free_spots, creator, reg_key=None):
        """Kurs erstellen"""

        #self.conn.autocommit = False

        create_course = self.pencil.gen_wlock()

        create_course_curs = self.conn.cursor()

        exception = None

        create_course_query_with_key = """insert into kurs(name, beschreibungstext, 
        ersteller, freieplaetze, einschreibeschluessel) values(?, ?, ?, ?, ?)"""

        create_course_query_without_key = """insert into kurs(name, beschreibungstext, 
            ersteller, freieplaetze) values(?, ?, ?, ?)"""

        if reg_key is None or reg_key == "":
            create_course.acquire()
            try:
                create_course_curs.execute(create_course_query_without_key, (name,
                                                                             desc, creator, free_spots))
            except Exception as e:
                print(e)
                exception = e
                self.conn.rollback()
            finally:
                self.conn.commit()
                create_course.release()

        else:
            create_course.acquire()
            try:
                create_course_curs.execute(create_course_query_with_key, (name, desc,
                                                                          creator, free_spots, reg_key))
            except Exception as e:
                print(e)
                exception = e
                self.conn.rollback()
            finally:
                self.conn.commit()
                create_course.release()

        #with create_course:
        #    create_course_curs.execute(
        #        create_course_query_without_key, (
        #            name, desc, creator, free_spots
        #        )
        #    )
        #create_course_curs.close()

        #return create_course_curs.rowcount

        if exception:
            return False
        else:
            return True


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
        kid = None
        get_kid_query = """select kid from kurs where name=? and ersteller=? """

        with kid_lock:
            get_kid_curs.execute(get_kid_query, (kname, bnummer))
            kid = get_kid_curs.fetchone()[0]
        get_kid_curs.close()

        # freie Platz prüfen
        get_fp_curs = self.conn.cursor()
        fp_lock = self.pencil.gen_rlock()
        fp = None
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
                            register_curs.execute(
                                register_query, (bnummer, kid))
                            row_count = register_curs.rowcount
                        register_curs.close()

                        check_exists_curs.close()

                        #TODO: Decrement count on free places

                        if row_count == 1:
                            return True

                else:  # keine schlüssel vorhanden
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

    @app.route("/<bid>", methods=['GET', 'POST'])
@app.route("/<bid>/", methods=['GET', 'POST'])
def index(bid):
    """Erste Seite der Webseite"""
    user_store = dao.application_dao.ApplicationDao()

    meine_kurse = user_store.get_my_courses(bid)
    verf_kurse = user_store.get_all_other_courses(bid)

    #result = False
    if request.method == "POST":
        #Form data
        name = request.form['course_name']
        enroll_key = request.form.get('schluessel')
        free_spots = request.form.get('freie_plaetze')
        desc = request.form.get('btext')  # Bytes for BLOB

        print(name, bid, enroll_key, free_spots, desc)

        new_course = dao.application_dao.ApplicationDao()
        #rows_affected = new_course.create_course(
        #    name, desc, bid, free_spots, enroll_key)

        new_course.add_course(name, desc, bid, free_spots, enroll_key)

        #print(rows_affected)

        #course_store = dao.application_dao.ApplicationDao()

        #course_id = course_store.add_course(new_course) # Muss eine valide kid zurückliefern
        #print(course_id, bid)
        #course_store.completion()
        #course_store.close()

        #if course_id is not None: #Wenn course_id nicht NULL ist, ist es valid #TODO
        #with threading.Lock():
        #user_store.einschreiben(bid, course_id, enroll_key) #Add owner to course, Fix

    #user_store.completion()
    #user_store.close()

    # TODO res=result
    return render_template('index.html', mkurse=meine_kurse, vkurse=verf_kurse, bid=bid)



# From view_course 20210113

    #print(bid)

    #Einschreibeschlüssel, wenn vorhanden. Wird benutzt zu prüfen, ob ein Schlüssel stimmt
    #reg_key = info.get_key(kname, ersteller)

    #course owner
    #owner = info.get_course_owner(kname)
    #print(owner)

    #desc = info.get_course_details(kname, ersteller)

    # Read details for above data from database

    #course id
    #kid = info.get_kid(kname, ersteller)
    #print(ersteller)
    #print(kid)
    #print(bid)
# Aufgaben
#Works partly
exercises_2 = """select aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000)), 
        cast(avg(cast(bewerten.note as decimal(2,1))) as decimal(2,1)) from kurs 
        join aufgabe on aufgabe.kid=kurs.kid left join einreichen 
        on einreichen.anummer=aufgabe.anummer left join abgabe 
        on abgabe.aid=einreichen.aid left join bewerten on bewerten.aid=abgabe.aid 
        where kurs.kid=? and einreichen.bnummer=? group by aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer
        order by aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer"""

#Works partly
exercises_3 = """select aufgabe.anummer, aufgabe.name,
	cast(abgabe.abgabetext as varchar(1000)),
        cast(avg(cast(bewerten.note as decimal(2, 1))) as decimal(2, 1)) from aufgabe
	join kurs on aufgabe.kid = kurs.kid
        join einschreiben on kurs.kid=einschreiben.kid
        join benutzer on benutzer.bnummer=einschreiben.bnummer 
        left join einreichen on benutzer.bnummer=einreichen.bnummer
        left join abgabe on einreichen.aid=abgabe.aid
        left join bewerten on abgabe.aid=bewerten.aid
        where kurs.kid=? and benutzer.bnummer=? and 
        aufgabe.anummer=einreichen.anummer
        group by aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000))
        order by aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer"""

#Returns all exercises
exercises_4 = """select aufgabe.anummer, 
        aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), 
        cast(avg(cast(bewerten.note as decimal(2,1))) as decimal(2,1)) from benutzer
        join einschreiben on benutzer.bnummer=einschreiben.bnummer
        join kurs on kurs.kid=einschreiben.kid
        join aufgabe on aufgabe.kid=kurs.kid 
        left join einreichen on einreichen.anummer=aufgabe.anummer
        left join abgabe on abgabe.aid=einreichen.aid 
        left join bewerten on bewerten.aid=abgabe.aid 
        where kurs.kid=? and benutzer.bnummer=? 
        group by aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer
        order by aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer"""


#Fails
exercises = """select aufgabe.anummer, aufgabe.name,
	cast(abgabe.abgabetext as varchar(1000)),
        cast(avg(cast(bewerten.note as decimal(2, 1))) as decimal(2, 1)) 
        from aufgabe
	join kurs on aufgabe.kid = kurs.kid
        left join einreichen 
        on einreichen.kid=aufgabe.kid and einreichen.anummer=aufgabe.anummer
        join abgabe 
        on abgabe.aid=einreichen.aid
        join bewerten on bewerten.aid=abgabe.aid
        where kurs.kid=? and einreichen.bnummer=?
        group by aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000))
        order by aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer)"""

#Fails
exercises_6 = """(select aufgabe.anummer, aufgabe.name,
	cast(abgabe.abgabetext as varchar(1000)),
        cast(avg(cast(bewerten.note as decimal(2, 1))) as decimal(2, 1)) from aufgabe
	join kurs on aufgabe.kid = kurs.kid
        join einschreiben on kurs.kid=einschreiben.kid
        join benutzer on benutzer.bnummer=einschreiben.bnummer 
        left join einreichen on benutzer.bnummer=einreichen.bnummer
        left join abgabe on einreichen.aid=abgabe.aid
        left join bewerten on abgabe.aid=bewerten.aid
        where kurs.kid=? and benutzer.bnummer=? and 
        aufgabe.anummer=einreichen.anummer
        group by aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000))
        order by aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer)
        """  # TODO: Second part of the Union


#Table Names
t_kurs = "kurs"
t_benutzer = "benutzer"
t_einreichen = "einreichen"
t_einschreiben = "einschreiben"
t_aufgabe = "aufgabe"
t_abgabe = "abgabe"
t_bewerten = "bewerten"

#Attribute/Columns
c_bnummer = "bnummer"
c_email = "email"
c_name = "name"
c_kid = "kid"
c_beschreibungstext = "beschreibungstext"
c_einschreibeschluessel = "einschreibeschluessel"
c_freieplaete = "freieplaetze"
c_ersteller = "ersteller"
c_anummer = "anummer"
c_beschreibung = "beschreibung"
c_aid = "aid"
c_abgabetext = "abgabetext"
c_note = "note"
c_kommentar = "kommentar"



# No longer used

    def get_key(self, kname, ersteller):  # Done, No longer used
        """
        Kursschlüssel zurückliefern
        """

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


    def get_ex_details(self, kid, anummer): #  Done, old code
        """
        Details für Aufgaben zurückgeben
        """
        desc_curs = self.conn.cursor()

        ex_details = """select cast(beschreibung as varchar(500)) from aufgabe kid=? and 
        anummer=?"""

        desc_curs.execute(ex_details, (kid, anummer))

        res = desc_curs.fetchone()

        res = res[0]

        if res is None:
            return None
        else:
            return res 

    def get_kid(self, kname, ersteller): # Note used, Done
        """
        KursID eines Kurses zurückliefern
        """
        kid_curs = self.conn.cursor()
    
        kid_curs.execute(queries.kid, (kname, ersteller))
        res = kid_curs.fetchone()
        kid_curs.close()

        if res is None:
            return None
        else:
            #print(res[0])
            return res[0]

    def get_course_owner(self, kname):  # No longer used
        """Id des Erstellers eines Kurses zurückliefern. wir gehen davon aus, dass
        jede Benutzer nur einen Kurs derselben Namen erstellen kann"""

        owner_curs = self.conn.cursor()
        owner_query = """select ersteller from kurs where name=?"""
        owner_curs.execute(owner_query, (kname,))
        owner = owner_curs.fetchone()[0]

        #print(owner)

        return owner


    def get_course_key(self, kid):  # Query to be added to queries. No longer needed
        """
        Einschreibeschlüssel für einen Kurs zurückliefern
        """
        get_key_query = """select einschreibeschluessel from kurs where kid=?"""
        get_key_curs = self.conn.cursor()

        get_key_curs.execute(get_key_query, (kid,))
        res = get_key_curs.fetchone()
        return res[0]

    def submission_exists(self, bid, kid, anummer): # No longer used
        """Prüfen, ob eine Abgabe für ein bnummer, kid und anummer schon existiert"""
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