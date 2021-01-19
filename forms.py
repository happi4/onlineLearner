from flask_wtf import FlaskForm
from wtforms.fields import html5 as h5fields
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea, html5 as h5widgets

class AddCourseForm(FlaskForm):
    """
    To add a new course to the database
    """
    name = StringField("Name", validators=[DataRequired()])
    key = StringField("Einschreibeschluessel")
    spaces = h5fields.IntegerField("Anzahl freie Plätze", 
        widget=h5widgets.NumberInput(min=1, max=100, step=1), validators=[DataRequired()])
    desc = StringField("Beschreibungstext", widget=TextArea())
    submit = SubmitField("Erstellen")

class CourseForm(FlaskForm):
    """
    To display courses in the homepage
    """
    course_name_sub = SubmitField()
    creator_name = HiddenField()
    spaces = HiddenField()
    course_id = HiddenField()
    creator_id = HiddenField()
    desc = HiddenField()
    key = HiddenField()
    course_name = HiddenField()

class EnrollmentForm(CourseForm):
    """
    To enroll into a course
    """
    key = PasswordField("Einschreibeschlüssel")
    submit = SubmitField("Einschreiben")
    status = HiddenField()

class CourseDetailForm(CourseForm):
    """
    To display details of courses in register page
    """
    course_name = HiddenField()
    creator_name = HiddenField()
    spaces = HiddenField()
    course_id = HiddenField()
    creator_id = HiddenField()
    desc = HiddenField()
    key = HiddenField()
    submit = SubmitField()
    status = HiddenField() #Stores the current state 

class ExercisesForm(FlaskForm):
    course_name = HiddenField()
    ex_name = SubmitField()
    ex_name_hidden = HiddenField()
    ex_id = HiddenField()
    submission = HiddenField()
    score = HiddenField()
    course_id = HiddenField()
    status = HiddenField()

class ExerciseSubmissionForm(CourseForm):
    course_name = HiddenField()
    course_id = HiddenField()
    ex_name = HiddenField()
    ex_id = HiddenField()
    sub_text = StringField("Abgabetext", widget=TextArea())
    user_id = HiddenField()
    submit = SubmitField("Einreichen")
