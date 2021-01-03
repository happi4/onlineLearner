from flask import Flask, request, render_template, redirect, url_for, flash
import dao.connect
import threading
import csv
import re
import beans.fach
import dao.application_dao
from beans import fach


app = Flask(__name__, template_folder='template')
app.secret_key = b'hdgsJ%82/"*dbh#'


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

    meine_kurse = user_store.get_my_courses(bid)
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

    #Einschreibeschlüssel, wenn vorhanden. Wird benutzt zu prüfen, ob ein Schlüssel stimmt
    reg_key = info_store.get_key(kname, ersteller) 

    #course owner
    owner = info_store.get_course_owner(kname) 
    #print(owner)

    desc = info_store.get_course_details(kname, ersteller)

    # Read details for above data from database 

    #course id
    kid = info_store.get_kid(kname, ersteller)

    #print(ersteller)
    #print(kid)
    #print(bid)

    #check resgistrstion status. Returns True or False
    registered = info_store.is_registered(bid, kid)

    #print(bid, kid)
    #print(registered)

    exercises = None

    #Get exercises for kid retieved
    exercises = info_store.get_ex_list(kid, int(bid))

    # TODO: Different view for ersteller


    return render_template("view_course.html", bid=bid, kname=kname, desc=desc, fp=fp, 
    ersteller=ersteller, schluessel=reg_key, owner=owner, exercises=exercises, 
    registered=registered, kid=kid)


@app.route('/<bid>/new_enroll', methods=['POST', 'GET'])
def new_enroll(bid):
    kname = request.form.get("kname")
    ersteller = request.form.get("ersteller")


    return render_template('new_enroll.html', bid=bid, kname=kname, ersteller=ersteller)


@app.route('/<bid>/new_assignment', methods=['POST', 'GET'])
def new_assignment(bid):

    store_submission = dao.application_dao.ApplicationDao()
        
    kid = request.form.get('kid')

    anummer = request.form.get('anummer')

    kname = request.form.get('kname')

    ex_name = request.form.get('ex_name')


    #TODO: decription
    #desc = store_submission.get_ex_details(kid, anummer)


    #print(bid, kid, anummer)

    #Submissions should be done only once: TODO: Is defective
    #is_duplicate = store_submission.submission_exists(bid, kid, anummer)

    #print(is_duplicate) TODO

    return render_template('new_assignment.html', kname=kname, ex_name=ex_name)


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
