"""Music Classroom."""
import xml.etree.cElementTree as ET
import xlsxwriter

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from datetime import datetime

import json
import os
import requests
from flask import request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

import random

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

from model import connect_to_db, db, Teacher, Classroom, Student, Group, StudentGroup, Music, ListeningSurvey, GroupSurvey, ClassroomSurvey, StudentSurvey, Instrument, InstrumentType, ClassroomInstrumentType


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


#Raises error if Jinja2 fails
app.jinja_env.undefined = StrictUndefined






@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")



@app.route('/student-register', methods=['GET'])
def student_register_form():
    """Show form for user signup."""

    return render_template("student_register_form.html")


@app.route('/student-register', methods=['POST'])
def student_register_process():
    """Process registration."""

    # Get form variables
    class_code = request.form["class-code"]

    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]

    username = fname[0].lower() + lname.lower()

    #Query to get classroom object from registration code
    class_query_object = Classroom.query.filter_by(registration_code=class_code).one()

    if class_query_object is None:
        #Flash registration denial
        flash("Class does not exist.  Please check your registration code.")

        #Redirect back to student register page
        return redirect("/student-register")
    else:
        #Create new student object
        new_student = Student(username=username, password=password, fname=fname, lname=lname, class_id=class_query_object.class_id)

        #Add to database and commit
        db.session.add(new_student)
        db.session.commit()

        #Flash registration confirmation, log student in, and redirect to student profile
        flash("Student {} {} added.".format(fname, lname))
        session["student_id"] = new_student.student_id
        return redirect("/students/{}".format(session['student_id']))


@app.route('/teacher-register', methods=['GET'])
def teacher_register_form():
    """Show form for user signup."""

    return render_template("teacher_register_form.html")    


@app.route('/teacher-register', methods=['POST'])
def teacher_register_process():
    """Process registration."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]

    # Create new teacher object
    new_teacher = Teacher(username=username, password=password, fname=fname, lname=lname)

    # Add teacher to database
    db.session.add(new_teacher)
    db.session.commit()

    #flash confirmation, log teacher in, redirect to teacher profile
    flash("Teacher {} {} added.".format(fname, lname))
    session["teacher_id"] = new_teacher.teacher_id
    return redirect("/teachers/{}".format(session["teacher_id"]))


@app.route('/create-class', methods=['GET'])
def create_class_form():
    """Show form for class creation."""  

    return render_template("create_class_form.html")


@app.route('/create-class', methods=['POST'])
def create_class_process():
    """Creates a classroom."""

    #Get variables from form
    teacher_id = session["teacher_id"]
    registration_code = request.form["registration_code"]
    name = request.form["name"]
    type_class = request.form["type_class"]

    #Create classroom object
    new_class = Classroom(teacher_id=teacher_id, registration_code=registration_code, name=name, type_class=type_class)

    #Add classroom to session
    db.session.add(new_class)
    db.session.commit()

    #Flash confirmation and redirect to class profile
    flash("Class successfully created.")
    return redirect("/classes/{}".format(new_class.class_id))


@app.route('/teacher-login', methods=['GET'])
def teacher_login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/teacher-login', methods=['POST'])
def teacher_login_process():
    """Process login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    #query teacher database
    teacher = Teacher.query.filter_by(username=username).first()

    #check if teacher exists
    if not teacher:
        flash("No such user")
        return redirect("/teacher-login")

    #check if password is correct
    if teacher.password != password:
        flash("Incorrect password")
        return redirect("/teacher-login")

    #add teacher to session
    session["teacher_id"] = teacher.teacher_id

    #flash confirmation, redirect to profile
    flash("Logged in")
    return redirect("/teachers/{}".format(teacher.teacher_id))


@app.route('/student-login', methods=['GET'])
def student_login_form():
    """Show login form."""

    return render_template("student_login_form.html")


@app.route('/student-login', methods=['POST'])
def student_login_process():
    """Process login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    #query student database
    student = Student.query.filter_by(username=username).first()

    #check if student exists
    if not student:
        flash("No such user")
        return redirect("/student-login")

    #check if password is correct
    if student.password != password:
        flash("Incorrect password")
        return redirect("/student-login")

    #add student to session
    session["student_id"] = student.student_id

    #flash confirmation, redirect to profile
    flash("Logged in.")
    if student.password == "password":
        flash("Your password is still the automatic password.  Please change as soon as possible.")
    return redirect("/students/{}".format(student.student_id))


@app.route('/logout')
def logout():
    """Log out."""

    #account for both types of users.  They shouldn't be able to see a Log Out if they are not logged in, but just in case?
    if "student_id" in session:
        del session["student_id"]
    elif "teacher_id" in session:
        del session["teacher_id"]
    else:
        return redirect("/")

    #flash confirmation, redirect to homepage
    flash("Logged Out.")
    return redirect("/")


@app.route("/students/<int:student_id>")
def student_detail(student_id):
    """Show info about student, student profile page."""
    student = Student.query.get(student_id)


    if "teacher_id" in session:
        #create filtering objects and lists
        teacher = Teacher.query.get(session["teacher_id"])
        classroom_list = Classroom.query.filter_by(teacher_id=teacher.teacher_id).all()

        students_by_teacher_list = []

        for classroom in classroom_list:
            class_students = Student.query.filter_by(class_id=classroom.class_id).all()
            students_by_teacher_list.extend(class_students)



        if student in students_by_teacher_list:
            instruments = Instrument.query.filter_by(student_id=student_id).all()
            surveys = StudentSurvey.query.filter_by(student_id=student_id).all()

            return render_template("student_profile.html", student=student, instruments=instruments, surveys=surveys)
        else:
            flash("not your student")
            return redirect("/")

    elif "student_id" in session:

        #check if student is logged in and is that student.
        if "student_id" in session and student_id == session["student_id"]:
            instruments = Instrument.query.filter_by(student_id=student_id).all()
            surveys = StudentSurvey.query.filter_by(student_id=student_id).all()

            return render_template("student_profile.html", student=student, instruments=instruments, surveys=surveys)

    else:
        flash("You must be logged in to access")
        return redirect('/')

    # instruments = Instrument.query.filter_by(student_id=student_id).all()

    # return render_template("student_profile.html", student=student, instruments=instruments)


@app.route("/teachers/<int:teacher_id>")
def teacher_detail(teacher_id):
    """Show info about teacher, teacher profile."""

    #check if teacher_id above is in session
    if teacher_id != session["teacher_id"]:
        flash("You must be logged in to access this page.")
        return redirect("/")

    #query teacher based on teacher_id
    teacher = Teacher.query.get(teacher_id)

    #display HTML page based on that teacher
    return render_template("teacher_profile.html", teacher=teacher)


@app.route("/change-password", methods=['GET'])
def change_password_form():
    """Displays change password form."""

    return render_template("change_password.html")


@app.route("/change-password", methods=['POST'])
def change_password():
    """Allows user to change password after confirmation."""

    #get variables from form
    old_password = request.form["old_password"]
    new_password1 = request.form["new_password1"]
    new_password2 = request.form["new_password2"]

    #check that newpassword1 == new password2
    if new_password1 != new_password2:
        flash("New password does not match confirmation, try again.")
        return redirect("/change-password")


    if "teacher_id" in session:
        user = Teacher.query.get(session["teacher_id"])
    else:
        user = Student.query.get(session["student_id"])

    if user.password == old_password:
        user.password = new_password1
        db.session.commit()
        flash("Password successfully changed!")
        return redirect("/")
    else:
        flash("Current password incorrect, please try again.")
        return redirect("/change-password")


@app.route("/classes", methods=['GET'])
def teacher_view_classes():
    """Displays list of all teacher classes"""

    my_classes = Classroom.query.filter_by(teacher_id = session["teacher_id"]).all()

    return render_template("view_classes.html", my_classes=my_classes)


@app.route("/classes/<int:class_id>", methods=['GET'])
def classroom_profile_page(class_id):
    """Displays classroom profile."""

    classroom = Classroom.query.get(class_id)
    students = Student.query.filter_by(class_id=class_id)
    classroominstrumenttype = ClassroomInstrumentType.query.filter_by(class_id=class_id)
    instruments = []
    for item in classroominstrumenttype:
        instruments.append(item.instrument)

    return render_template("class_profile.html", classroom=classroom, students=students, instruments=instruments)


@app.route("/teacher-add-student/<int:class_id>", methods=['GET'])
def display_teacher_add_student_form(class_id):
    """Allows teacher to add a student."""

    return render_template("teacher_add_student_form.html", class_id=class_id)



@app.route("/teacher-add-student/<int:class_id>", methods=['POST'])
def teacher_add_student(class_id):
    """Teacher adds student."""


    fname = request.form["fname"]
    lname = request.form["lname"]

    username = fname[0].lower() + lname.lower()
    password = 'password'

    #Create new student object
    new_student = Student(username=username, password=password, fname=fname, lname=lname, class_id=class_id)

    #Add to database and commit
    db.session.add(new_student)
    db.session.commit()

    #Flash registration confirmation, log student in, and redirect to student profile
    flash("Student {} {} added.".format(fname, lname))
    flash("Student username = {}, password = password".format(username))
    flash("Please tell student to change their password the first time they log in.")
    return redirect("/classes")




@app.route("/instrument-checkin", methods=['GET'])
def instrument_checkin_form():
    """Show form for instrument checkin."""

    instrument_types_object = InstrumentType.query.all()
    # serial_numbers_object = Instrument.
    instrument_types = []
    serial_numbers = []
    for instrument_type in instrument_types_object:
        instrument_types.append(instrument_type.name)


    return render_template("instrument_checkin_form.html", instrument_types=instrument_types)


@app.route("/instrument-checkin", methods=['POST'])
def instrument_checkin_process():
    """Strip student_id from instrument."""

    #get variables from form
    serial_number = request.form["serial_number"]

    instrument = Instrument.query.get(serial_number)

    #update instrument.student_id = Null

    instrument.student_id = None
    db.session.commit()
    flash("Instrument Successfully checked in.")
    return redirect("/instrument-checkin")


@app.route("/instrument-checkout", methods=['GET'])
def instrument_checkout_form():
    """Show form for instrument checkout."""

    teacher = Teacher.query.get(session['teacher_id'])

    #get instrument types belonging to teacher, put in list
    instrument_types = teacher.get_instrument_types_by_teacher()

    instruments_by_number = {}
    for instrument_type in instrument_types:
        inst_st = str(instrument_type)
        all_of_type = Instrument.query.filter_by(teacher_id=teacher.teacher_id).filter_by(instrument_name=instrument_type).all()

        all_insts_list = []
        for instrument in all_of_type:
            if instrument.student_id is None:
                all_insts_list.append(instrument.serial_number)

        instruments_by_number[inst_st] = all_insts_list

    instruments_by_number_json = json.dumps(instruments_by_number)

    #get students belonging to teacher, fname and lname
    students = teacher.get_students_by_teacher()
    students_fname = []
    students_lname = []

    for student in students:
        students_fname.append(student.fname)
        students_lname.append(student.lname)

    return render_template("instrument_checkout_form.html", instrument_types=instrument_types, serial_number_dict=instruments_by_number_json, students_fname=students_fname, students_lname=students_lname)


@app.route("/instrument-checkout", methods=['POST'])
def instrument_checkout_process():
    """Strip student_id from instrument."""

    #get variables from form
    serial_number = request.form["serial_number"]
    fname = request.form["fname"]
    lname = request.form["lname"]

    #find instrument by serial number
    instrument = Instrument.query.get(serial_number)

    #find student by name CURRENTLY ASSUMING ALL STUDENTS ARE UNIQUE... FIX IN AJAX?
    student = Student.query.filter_by(lname=lname).filter_by(fname=fname).one()

    #update instrument student
    instrument.student = student

    db.session.commit()
    flash("Instrument Successfully checked out.")
    return redirect("/instrument-checkout")


@app.route("/instrument-inventory", methods=['GET'])
def instrument_inventory():
    """Displays an inventory of instruments sorted by type."""

    my_instruments = Instrument.query.filter_by(teacher_id=session["teacher_id"]).all()

    my_instruments = sorted(my_instruments, key=lambda instrument:instrument.instrument_name)

    return render_template("instrument_inventory.html", my_instruments=my_instruments)



@app.route("/add-instrument-type", methods=['GET'])
def add_instrument_type_form():
    """Displays add instrument type form."""

    return render_template("add_instrument_type_form.html")


@app.route("/add-instrument-type", methods=['POST'])
def add_instrument_type():
    """Adds instrument type."""

    name = request.form["instrument_name"]
    family = request.form["family"]

    new_instrument = InstrumentType(name=name, family=family)

    db.session.add(new_instrument)
    db.session.commit()
    flash("Instrument successfully added.")
    return redirect("/add-instrument-type")


@app.route("/add-instrument-to-class", methods=['GET'])
def add_instrument_to_class_form(class_id):
    """Displays add instrument type to class form."""





#     instrument_name = request.form["name"]

#     classroom = request.form["classroom"]

#     if instrument_name in InstrumentType.query.:
#         if classroom in 

    return redirect('/')



@app.route("/add-instrument-to-class", methods=['POST'])
def add_instrument_to_class():
    """Adds instrument type to class."""

    classroom = Classroom.query.get(class_id)

    instrument_name = request.form["name"]

    family = request.form["family"]



    pass



@app.route("/add-instrument-to-inventory", methods=['GET'])
def display_add_instrument_to_inventory():
    """Displays instrument to inventory form."""

    teacher = Teacher.query.get(session['teacher_id'])

    instruments = teacher.get_instrument_types_by_teacher()

    return render_template('add_instrument.html', instruments=instruments)


@app.route("/add-instrument-to-inventory", methods=['POST'])
def add_instrument_to_inventory():

    serial_number = request.form["serial_number"]
    instrument_name = request.form["instrument_type"]
    teacher_id = session["teacher_id"]
    maker = request.form["maker"]
    model = request.form["model"]
    year_manufactured = request.form["year"]

    new_instrument = Instrument(serial_number=serial_number, instrument_name=instrument_name, teacher_id=teacher_id, maker=maker, model=model, year_manufactured=year_manufactured)

    db.session.add(new_instrument)
    db.session.commit()

    flash('Instrument added.')
    return redirect('/instrument-inventory')



@app.route("/create-group", methods=['GET'])
def create_group_form():
    """Displays create group form"""

    return render_template("create_group_form.html")


@app.route("/create-group", methods=['POST'])
def create_group_process():
    """Creates group."""

    #get form variables
    class_id = request.form["class_id"]
    name = request.form["name"]

    #create new group object
    new_group = Group(class_id=class_id, name=name)

    #add new group to session and commit
    db.session.add(new_group)
    db.session.commit()

    #flash confirmation and redirect to add another group
    flash("New Group successfully created.")
    return redirect("/create-group")


@app.route("/add-student-to-group", methods=['GET'])
def add_student_to_group_form():
    """Displays add student to group form."""

    teacher = Teacher.query.get(session["teacher_id"])
    students = teacher.get_students_by_teacher()
    groups = teacher.get_groups_by_teacher()
    classrooms = Classroom.query.filter_by(teacher_id=teacher.teacher_id).all()

    return render_template("add_student_to_group_form.html", students=students, groups=groups, classrooms=classrooms)


@app.route("/add-student-to-group", methods=['POST'])
def add_student_to_group():
    """Adds student to group."""




    #get form variables
    student_id = int(request.form["student"])
    group_id = int(request.form["group"])

    add_student_to_group(student_id, group_id)

    flash("Student successfully added!")
    return redirect("/add-student-to-group")


@app.route("/resources")
def display_resources():

    return render_template("resources.html")


@app.route('/upload-resource', methods=['GET'])
def upload_file_form():

    return render_template("upload_resources.html")


@app.route('/upload-resource', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/survey', methods=['GET'])
def display_all_surveys():
    """Displays list of all surveys."""

    my_surveys = ListeningSurvey.query.all()

    return render_template("view_surveys_table.html", my_surveys=my_surveys)




@app.route('/survey/<survey_id>', methods=['GET'])
def display_survey(survey_id):
    """Displays individual survey."""

    music_id = ListeningSurvey.query.get(survey_id).music_id

    music_src = Music.query.get(music_id).mp3_src


    return render_template("survey.html", music_src=music_src, survey_id=survey_id)


@app.route('/survey/<survey_id>', methods=['POST'])
def complete_survey(survey_id):
    """Changes student id in student surveys to marked completed."""

    student_comment = request.form['student_comment']
    student_id = session['student_id']

    current_survey = StudentSurvey.query.filter_by(student_id=student_id).filter_by(survey_id=survey_id).first()

    if not current_survey:
        create_student_survey(student_id, survey_id, student_comment)

        flash("Assignment completed!")
        return redirect("/survey")

    else:
        flash("You've already completed this assignment!")
        return redirect("/survey")

@app.route('/my-classmates')
def show_classmates():
    """Shows student's friends and peers completions."""

    #get students in class
    my_class = Student.query.get(session["student_id"]).class_id
    my_classmates = Student.query.filter_by(class_id=my_class).all()

    names_list = []
    survey_numbers = []
    for classmate in my_classmates:
        full_name = str(classmate.fname) + " " + str(classmate.lname)
        names_list.append(full_name)
        survey_numbers.append(str(classmate.get_number_of_completed_surveys()))

    surveys = []
    for student in my_classmates:

        their_surveys = student.get_completed_surveys()
        surveys.extend(their_surveys)


    #display classmates
    return render_template("my_classmates.html", my_classmates=my_classmates, surveys=surveys, names_list=names_list, survey_numbers=survey_numbers)



@app.route('/composer-timeline')
def composer_life():

    return render_template('composer_life.html')


@app.route('/groups')
def display_groups():


    teacher = Teacher.query.get(session["teacher_id"])
    my_groups = teacher.get_groups_by_teacher()

    return render_template('view_groups.html', my_groups=my_groups)



@app.route("/groups/<group_id>")
def group_profile(group_id):

    group = Group.query.get(group_id)

    studentgroups = StudentGroup.query.filter_by(group_id=group_id).all()

    students = []

    for studentgroup in studentgroups:
        student = studentgroup.student
        students.append(student)

    return render_template("group_profile.html", group=group, students=students)


@app.route("/test-score")
def test_score():

    return render_template("test_render_xml_page.html")



@app.route("/tuner")
def tuner():

    return render_template("tuner.html")


@app.route("/learn-about")
def learn_about():

    return render_template("learn_about.html")

@app.route("/chord-test")
def chord_test():

    return render_template("chord_radar.html")


@app.route("/vexflow-test")
def test_vex():

    return render_template("vexflow_test.html")

@app.route("/major-scales")
def major_scales():

    return render_template("major_scales.html")


@app.route("/color-test")
def color_scale():

    return render_template("color_test.html")


#####################################################################
# Helper functions

def random_note_generator():
    """Generates random note from list, formatted for Vexflow."""

    notes = ["a", "b", "c", "d", "e", "f", "g"]
    accidentals = ["#", "b", ""]
    length = [""] #fix this

    random_name = random.choice(notes)
    random_acc = random.choice(accidentals)
    random_leng = random.choice(length)

    random_note = [random_name, random_acc, random_leng]

    return random_note


def add_student_to_group(student_id, group_id):
    """Adds student to group.  Helper function."""

    new_student_group = StudentGroup(student_id=student_id, group_id=group_id)
    db.session.add(new_student_group)
    db.session.commit()

    pass


def create_student_survey(student_id, survey_id, student_comment):
    """Creates student-survey relationship.  Helper function."""
    completed_at = datetime.now()

    new_student_survey = StudentSurvey(survey_id=survey_id, student_id=student_id, completed_at=completed_at, student_comment=student_comment)
    db.session.add(new_student_survey)
    db.session.commit()

    pass



def auto_create_by_instrument_family(class_id, family):
    """Create band instrument groups."""

    # new_group = Group.query.filter_by(class_id=class_id).filter_by(name=family).one()

    # if new_group is []:
    #     new_group = Group(class_id=class_id, name=family)
    #     db.session.add(new_group)

    new_group = Group(class_id=class_id, name=family)

    #find students with woodwind instruments
    all_students = Student.query.filter_by(class_id=class_id).all()
    
    for student in all_students:
        all_instruments = Instrument.query.filter_by(student_id=student.student_id).all()
        for instrument in all_instruments:
            if instrument.name.family == family:
                if StudentGroup.query.filter_by(student_id=student.student_id, group_id=new_group.group_id).all() is not []:
                    this_student = StudentGroup(student_id=student.student_id, group_id=new_group.group_id)
                    db.session.add(this_student)

    db.session.commit()


    pass


def export_xml_file():
    """Exports list of students as xml file."""

    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")

    #experimenting with the library for xml -- music files

    tree = ET.ElementTree(root)
    tree.write("filename.xml")

    pass


def export_student_list_xls(teacher_id):
    """Exports list of students in xls format."""

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Student_List.xlsx')
    worksheet = workbook.add_worksheet()

    # Some data we want to write to the worksheet.
    teacher = Teacher.query.get(teacher_id)
    students = teacher.get_students_by_teacher()

    students_list = []

    for student in students:
        student_attributes = [student.fname, student.lname]
        students_list.append(student_attributes)

    students_list = tuple(students_list)
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for fname, lname in (students_list):
        worksheet.write(row, col,     fname)
        worksheet.write(row, col + 1, lname)
        row += 1

    # # Write a total using a formula.
    # worksheet.write(row, 0, 'Total')
    # worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





# def display_student_profile(student_id):
#     """Displays student profile page.  Helper function."""

#         #create list of all instruments checked out to student
#     instruments = Instrument.query.filter_by(student_id=student_id).all()

#     return render_template("student_profile.html", student=student, instruments=instruments)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(host="0.0.0.0")
