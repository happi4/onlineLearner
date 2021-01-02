from flask import Flask, request, render_template, redirect, url_for
import dao.connect
import threading
import csv
import re
import beans.fach
import dao.application_dao
from beans import fach


app = Flask(__name__, template_folder='template')


def csv_reader(path):
    with open(path, "r") as csvfile:
        tmp = {}
        reader = csv.reader(csvfile, delimiter='=')
        for line in reader:
            tmp[line[0]] = line[1]
    return tmp

config = csv_reader("properties.settings")


@app.route("/<bid>/", methods=['GET', 'POST'])
@app.route("/<bid>", methods=['GET', 'POST'])
def index(bid):
    """Erste Seite der Webseite: """
    user_store = dao.application_dao.ApplicationDao() 

    meine_kurse = user_store.get_courses(bid)
    verf_kurse = user_store.get_all_other_courses(bid)

    #result = False
    #if request.method == "POST":
        # Form data
        #name = request.form['course_name'] 
        #enroll_key = request.form.get('schluessel')
        #free_spots = request.form.get('freie_plaetze')  
        #desc = request.form.get('btext')
        
        #print(name, bid, enroll_key, free_spots, desc)
        
        #new_course = fach.Kurs(name, bid, free_spots, desc, enroll_key)
        
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


@app.route("/<bid>/new_course", methods=['POST', 'GET'])
def new_course(bid):
    return render_template("new_course.html", bid=bid)


@app.route("/<bid>/view_course", methods=['POST', 'GET'])
def view_course(bid):
    info_store = dao.application_dao.ApplicationDao()
    kname = str(request.form.get("kname"))
    ersteller = str(request.form.get("ersteller"))
    fp = request.form.get("fp")

    #print(bid)

    #Einschreibeschlüssel, wenn vorhanden
    reg_key = info_store.get_key(kname, ersteller) 

    #course owner
    owner = info_store.get_course_owner(kname) 

    desc = info_store.get_course_details(kname, ersteller)

    # Read details for above data from database 

    #course id
    kid = info_store.get_kid(kname, ersteller)
    print(kid)

    #Get exercises for kid retieved
    exercises = info_store.get_ex_list(kid)

    # TODO: Different view for ersteller


    return render_template("view_course.html", bid=bid, kname=kname, desc=desc, fp=fp, 
    ersteller=ersteller, schluessel=reg_key, owner=owner, exercises=exercises)


@app.route('/<bid>/new_enroll', methods=['POST', 'GET'])
def new_enroll(bid):
    kname = request.form.get("kname")
    ersteller = request.form.get("ersteller")


    return render_template('new_enroll.html', bid=bid, kname=kname, ersteller=ersteller)


@app.route('/onlineLearner', methods=['GET'])
def onlineLearn():

    try:
        dbExists = dao.connect.DBUtil().checkDatabaseExistsExternal()
        if dbExists:
            db2exists = 'vorhanden! Supi!'
        else:
            db2exists = 'nicht vorhanden :-('
    except Exception as e:
        print(e)

    return render_template('onlineLearner.html', db2exists=db2exists, db2name="onlineLearner")





if __name__ == "__main__":
    port = int("9" + re.match(r"([a-z]+)([0-9]+)", config["username"], re.I).groups()[1])
    app.run(host='0.0.0.0', port=port, debug=True)
