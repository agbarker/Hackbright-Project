"""Music Classroom."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Teacher, Classroom, Student, Group, StudentGroup, Music, Listening_Survey, GroupSurvey, ClassroomSurvey, StudentSurvey


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

    return render_template("student_code_check.html")


@app.route('/student-register', methods=['POST'])
def student_register_process():
    """Process registration."""

    # Get form variables
    class_code = request.form["class-code"]




    password = request.form["password"]
    age = int(request.form["age"])
    zipcode = request.form["zipcode"]

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User {} added.".format(email))
    return redirect("/users/{}".format(new_user.user_id))








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

    new_user = Teacher(username=username, password=password, fname=fname, lname=lname)

    db.session.add(new_user)
    db.session.commit()

    flash("User {} added.".format(username))
    return redirect("/")
#    return redirect("/users/{}".format(new_user.user_id))


@app.route('/create-class', methods=['GET'])
def create_class_form():
	"""Show form for class creation."""


	available_instruments = ["flute", "oboe", "clarinet", "bass clarinet", "alto sax", "tenor sax", "bari sax", "trumpet", "coronet", "french horn", "mellophone", "trombone", "tuba", "percussion"]

	return render_template("create_class_form.html", available_instruments=available_instruments)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
