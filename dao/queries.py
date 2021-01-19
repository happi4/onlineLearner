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


# Meine Kurse
my_courses = """select kurs.name, benutzer.name, kurs.freieplaetze, kurs.kid, 
            kurs.ersteller, cast(kurs.beschreibungstext as varchar(1000)), 
            kurs.einschreibeschluessel from benutzer 
            join kurs on kurs.ersteller=benutzer.bnummer join einschreiben 
            on einschreiben.kid=kurs.kid where einschreiben.bnummer=?"""

# Verfügbare Kurse
available_courses = """(select kurs.name, benutzer.name,  
                    kurs.freieplaetze, kurs.kid, kurs.ersteller, 
                    cast(kurs.beschreibungstext as varchar(1000)), 
                    kurs.einschreibeschluessel from benutzer join kurs 
                    on kurs.ersteller=benutzer.bnummer 
                    left join einschreiben on einschreiben.kid=kurs.kid 
                    where kurs.freieplaetze > 0) 
                    minus 
                    select kurs.name, benutzer.name, kurs.freieplaetze, kurs.kid,
                    kurs.ersteller, cast(kurs.beschreibungstext as varchar(1000)),
                    kurs.einschreibeschluessel from benutzer join kurs 
                    on kurs.ersteller=benutzer.bnummer join einschreiben
                    on einschreiben.kid=kurs.kid where einschreiben.bnummer=?"""

# Kurs Erstellen 
add_course_with_key = """insert into kurs(name, beschreibungstext, 
                        ersteller, freieplaetze, einschreibeschluessel) 
                        values(?, ?, ?, ?, ?)"""

add_course_no_key = """insert into kurs(name, beschreibungstext, 
                        ersteller, freieplaetze) values(?, ?, ?, ?)"""

# Registriert?
is_reg = """select * from einschreiben where bnummer=? and kid=?"""

#Einschreiben
add_to_course = """insert into einschreiben(bnummer, kid) values(?, ?)"""

# Details des Kurses
course_details = """select kurs.name, benutzer.name, kurs.freieplaetze, kurs.kid, 
                    kurs.ersteller, cast(beschreibungstext as varchar(3200)), 
                    kurs.einschreibeschluessel 
                    from kurs join benutzer on kurs.ersteller=benutzer.bnummer 
                    where kurs.kid=?"""


# Aufgaben
exercises_test1 = """select aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000)), 
        cast(avg(cast(bewerten.note as decimal(2,1))) as decimal(2,1)) from kurs 
        join aufgabe on aufgabe.kid=kurs.kid left join einreichen 
        on einreichen.anummer=aufgabe.anummer left join abgabe 
        on abgabe.aid=einreichen.aid left join bewerten on bewerten.aid=abgabe.aid 
        where kurs.kid=? and einreichen.bnummer=? group by aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer
        order by aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), aufgabe.anummer"""

exercises_original = """select aufgabe.anummer, aufgabe.name,
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

sub_text = """insert into abgabe(abgabetext) values(?)"""

aid = """select aid from abgabe where cast(abgabetext as varchar(1000))=?"""

submission_ref = """insert into einreichen (bnummer, kid, anummer, aid) values(?, ?, ?, ?)"""

exercises_test2 = """select aufgabe.anummer, aufgabe.name, cast(abgabe.abgabetext as varchar(1000)), 
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


exercises_test3 = """(select distinct aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000))
        from benutzer 
        join einschreiben on einschreiben.bnummer=benutzer.bnummer 
        join kurs on einschreiben.kid=kurs.kid 
        join aufgabe on kurs.kid=aufgabe.kid 
        left join einreichen on einreichen.anummer=aufgabe.anummer
        left join abgabe on abgabe.aid=einreichen.aid
        where kurs.kid=? and benutzer.bnummer=? and einreichen.bnummer=benutzer.bnummer
        order by aufgabe.name, aufgabe.anummer) 
        union 
        (select distinct aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000))
        from benutzer """ #TODO

exercises = """(select aufgabe.anummer, aufgabe.name,
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
        union 
        (select aufgabe.anummer, aufgabe.name, 'Noch keine Abgabe', 
        'Noch keine Bewertung' from aufgabe
	join kurs on aufgabe.kid = kurs.kid
        join einschreiben on kurs.kid=einschreiben.kid
        join benutzer on benutzer.bnummer=einschreiben.bnummer 
        left join einreichen on benutzer.bnummer=einreichen.bnummer
        where aufgabe.anummer not in (select anummer from einreichen) 
        and kurs.kid=? and benutzer.bnummer=?)""" #TODO: Second part of the Union


#Löschen

delete1 = """delete from bewerten where bewerten.aid in 
        (select abgabe.aid from abgabe join einreichen on einreichen.aid=abgabe.aid where einreichen.kid=?)"""
delete2 = """delete from abgabe where abgabe.aid in (select einreichen.aid from einreichen where einreichen.kid=?)"""
delete3 = """delete from aufgabe where kid=?"""
delete4 = """delete from einschreiben where einschreiben.kid=?"""
delete5 = """delete from kurs where kid=?"""
