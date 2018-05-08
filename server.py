"""Music Classroom."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Teacher, Classroom, Student, Group, StudentGroup, Music, ListeningSurvey, GroupSurvey, ClassroomSurvey, StudentSurvey


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

    #Get vars from form
    username = request.form["username"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]

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

        #Flash registration confirmation and redirect to homepage (later to student profile)

        flash("Student {} {} added.".format(fname, lname))
        return redirect("/")

        # return redirect("/users/{}".format(new_user.user_id))


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

    flash("Teacher {} {} added.".format(fname, lname))
    return redirect("/")
#    return redirect("/users/{}".format(new_user.user_id))


@app.route('/create-class', methods=['GET'])
def create_class_form():
	"""Show form for class creation."""  



    #FIX ME
	return render_template("create_class_form.html")


@app.route('/create-class', methods=['POST'])
def create_class_process():

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

    #Redirect to class profile to choose instruments, etc.
    return redirect("/")


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

    teacher = Teacher.query.filter_by(username=username).first()

    if not teacher:
        flash("No such user")
        return redirect("/teacher-login")

    if teacher.password != password:
        flash("Incorrect password")
        return redirect("/teacher-login")

    session["teacher_id"] = teacher.teacher_id

    flash("Logged in")
    return redirect("/create-class")

    # return redirect("/users/{}".format(user.user_id))


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

    student = Student.query.filter_by(username=username).first()

    if not student:
        flash("No such user")
        return redirect("/student-login")

    if student.password != password:
        flash("Incorrect password")
        return redirect("/student-login")

    session["student_id"] = student.student_id

    flash("Logged in")
    return redirect("/")

    # return redirect("/users/{}".format(user.user_id))


@app.route('/logout')
def logout():
    """Log out."""

    if "student_id" in session:
        del session["student_id"]
    elif "teacher_id" in session:
        del session["teacher_id"]
    else:
        return redirect("/")
    flash("Logged Out.")
    return redirect("/")


@app.route("/students/<int:student_id>")
def student_detail(student_id):
    """Show info about student."""

    student = Student.query.get(student_id)
    return render_template("student_profile.html", student=student)


@app.route("/teachers/<int:teacher_id>")
def teacher_detail(teacher_id):
    """Show info about student."""

    teacher = Teacher.query.get(teacher_id)
    return render_template("teacher_profile.html", teacher=teacher)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
