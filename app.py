from flask import Flask, request, render_template, redirect, url_for, flash
from flask_caching import Cache
import dao.connect
import threading
import csv
import re
import beans.fach
import dao.dao as dao
from beans import fach
import forms

"""For cache"""
configurations = {
    "DEBUG": True, 
    "CACHE_TYPE":  "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}


app = Flask(__name__, template_folder='template')
app.secret_key = b'hdgsJ%82/"*dbh#'
#For cache
app.config.from_mapping(configurations)
cache = Cache(app)


def csv_reader(path):
    with open(path, "r") as csvfile:
        tmp = {}
        reader = csv.reader(csvfile, delimiter='=')
        for line in reader:
            tmp[line[0]] = line[1]
    return tmp

config = csv_reader("properties.settings")


@app.route("/<bid>", methods=['GET', 'POST'])
@app.route("/<bid>/", methods=['GET', 'POST'])
#@cache.memoize()
def index(bid):
    """
    Erste Seite der Webseite
    """
    user = dao.Dao()
    title = "Hauptseite"
    form = forms.CourseForm()
    meine_kurse = user.get_my_courses(bid)
    verf_kurse = user.get_available_courses(bid)

    return render_template('index.html', mkurse=meine_kurse, vkurse=verf_kurse, 
                            bid=bid, title=title, form=form)

@app.route("/<bid>/new_course", methods=['POST', 'GET'])
def new_course(bid):
    """
    Kurs erstellen
    """
    course = dao.Dao()
    title = "Kurs Erstellen"
    #form = forms.AddCourseForm(name = "Klaus")
    form = forms.AddCourseForm()
    if form.validate_on_submit():
        name = str(form.name.data)
        desc = str(form.desc.data)
        spaces = form.spaces.data
        key = str(form.key.data)
        #print(name, desc, spaces, bid, key)
        error = course.add_course(name, desc, spaces, bid, key)
        if error is None:
            flash("Course successfully created")
        else:
            flash("Failed to create course.")
        return redirect(url_for('index', bid=bid))
    return render_template("new_course.html", title=title, bid=bid, form=form)


@app.route("/<bid>/<kid>/view_course", methods=['POST', 'GET'])
#@cache.memoize()
def view_course(bid, kid):
    info = dao.Dao()

    #form_get = forms.CourseForm(request.form) 

    title = "Kurs Details"
    kurs = info.get_course_details(kid)
    form = forms.CourseDetailForm()
    registered = info.is_registered(bid, kid)

    #Get exercises for kid retieved
    form_ex = forms.ExercisesForm()
    exercises = info.get_exercises(kid, bid)

    #print(exercises)
    # form has been posted and submission exists
    if request.form.get("submission"):
        flash("Das neues Einreichen ist nicht möglich")
        return redirect(url_for('view_course', bid=bid, kid=kid))

    #Einschreiben ohne Schlüssel
    if request.method == 'POST' and request.form.get('status') == 'register': #status code for registration
        status = info.add_to_course(bid, kid)  # key is none
        if status == True:
            flash("Enrollment to course successfull")
        elif status == False:
            flash("An error occured while registering")
        return redirect(url_for('view_course', bid=bid, kid=kid))

    return render_template("view_course.html", bid=bid, exercises=exercises, 
    form_ex=form_ex, registered=registered, kid=kid, title=title, form=form, kurs=kurs)


@app.route('/<bid>/<kid>/new_enroll', methods=['POST', 'GET'])
def new_enroll(bid, kid):
    """
    Ein Benutzer schreibt sich ein
    """
    course = dao.Dao()
    form = forms.EnrollmentForm(request.form)
    kname = form.course_name.data
    print(kname, kid)

    # status code
    #if request.method == 'POST' and course.get_course_key(kid) is None and request.form.get('status') == 'register':
        
    if form.validate_on_submit():
        status = course.add_to_locked_course(bid, kid, form.key.data)
        if status == True:
            flash("Enrollment to course successfull")
        elif status == False:
            flash("Enrollment failed because of wrong key")
        elif status == None:
            flash("An error occured")
        return redirect(url_for('view_course', bid=bid, kid=kid))

    return render_template('new_enroll.html', bid=bid, kid=kid, kname=kname, form=form)


@app.route('/<bid>/new_assignment', methods=['POST', 'GET'])
def new_assignment(bid):

    title = "Abgabe Einreichen"

    form_get = forms.ExercisesForm(request.form)
    ex_name = form_get.ex_name_hidden.data
    course_name = form_get.course_name.data
    anummer = form_get.ex_id.data
    kid = form_get.course_id.data

    #print(form_get.ex_id.data)

    form = forms.ExerciseSubmissionForm()
    #form.course_name.data = form_get.course_name.data
    #form.course_id.data = form_get.course_id.data
    #form.user_id.data = bid
    #form.ex_id.data = form_get.ex_id.data

    new_submission = dao.Dao()

    if request.method == "POST" and request.form.get("submit"):

        #print(form.ex_name.data, form.course_name.data, 
        #form.course_id.data, form.user_id.data, form.sub_text.data)
        text = form.sub_text.data
        new_submission.add_sub_text(text) # Insert into abgabe
        aid = new_submission.get_aid(text)
        print(aid)
        kid = form.course_id.data
        anummer = form.ex_id.data
        print(bid, kid, anummer, aid)
        status = new_submission.add_sub_ref(int(bid), int(kid), int(anummer), int(aid)) #TODO
        if status is True:
            flash("Submission has been registered successfully")
        else:
            flash("Failed to submit your work")
        return redirect(url_for("view_course", bid=bid, kid=kid))

        
    #kid = request.form.get('kid')

    #anummer = request.form.get('anummer')

    #kname = request.form.get('kname')

    #ex_name = request.form.get('ex_name')


    #TODO: decription
    #desc = store_submission.get_ex_details(kid, anummer)


    #print(bid, kid, anummer)

    #Submissions should be done only once: TODO: Is defective
    #is_duplicate = store_submission.submission_exists(bid, kid, anummer)

    #print(is_duplicate) TODO

    return render_template('new_assignment.html', ex_name=ex_name, form=form, title=title, 
    course_name=course_name, anummer=anummer, kid=kid)


@app.route('/<bid>/<kid>/delete', methods=['GET', 'POST'])    
def delete(bid, kid):
    """
    Kurs löschen. Nur der Ersteller kann einen Kurs löschen
    """
    user = dao.Dao()
    if request.method == "POST":
        #Delete course
        form_delete = forms.CourseDetailForm(request.form)
        kname = form_delete.course_name.data
        kid = form_delete.course_id.data
        owner = form_delete.creator_id.data
        print(kid, owner)
        if owner == bid:
            #print(kid, owner)
            status = user.delete_course(kid)
            print(status)
            if status == True:
                success = "Deleted course " + kname + " successfully"
                flash(success)
                return redirect(url_for("index", bid=bid))
            else:
                exception = "An error occured while deleting the course" + kname
                return redirect(url_for("view_course", bid=bid, kid=kid))
        else:
            #Kurs Löschen für Nichtersteller
            # status code for deletion
            #if request.method == 'POST' and request.form.get('status') == 'delete':
            failure = "Failed to delete " + kname + \
            " because you are not the course creator!"
            flash(failure)
            return redirect(url_for("view_course", bid=bid, kid=kid))

    



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
    app.add_url_rule(
        '/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))
