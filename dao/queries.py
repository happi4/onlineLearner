
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
exercises = """select distinct aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000)), 
        cast(avg(cast(bewerten.note as decimal(2, 1))) as decimal(2, 1)) from
        benutzer join einschreiben on einschreiben.bnummer=benutzer.bnummer 
        join kurs on einschreiben.kid=kurs.kid 
        join aufgabe on aufgabe.kid=kurs.kid 
        left join einreichen on einreichen.anummer=aufgabe.anummer
        and einreichen.bnummer=benutzer.bnummer and einreichen.kid=kurs.kid
        left join abgabe on abgabe.aid=einreichen.aid
        left join bewerten on bewerten.aid=abgabe.aid
        where kurs.kid=? and benutzer.bnummer=?
        group by aufgabe.anummer, aufgabe.name, 
        cast(abgabe.abgabetext as varchar(1000))
        order by aufgabe.name, aufgabe.anummer, 
        cast(abgabe.abgabetext as varchar(1000))"""

# Einreichen
sub_text = """insert into abgabe(abgabetext) values(?)"""
aid = """select aid from abgabe where cast(abgabetext as varchar(1000))=?"""
submission_ref = """insert into einreichen (bnummer, kid, anummer, aid) values(?, ?, ?, ?)"""


#Löschen
delete1 = """delete from bewerten where bewerten.aid in 
        (select abgabe.aid from abgabe join einreichen on einreichen.aid=abgabe.aid where einreichen.kid=?)"""
delete2 = """delete from abgabe where abgabe.aid in (select einreichen.aid from einreichen where einreichen.kid=?)"""
delete3 = """delete from aufgabe where kid=?"""
delete4 = """delete from einschreiben where einschreiben.kid=?"""
delete5 = """delete from kurs where kid=?"""
