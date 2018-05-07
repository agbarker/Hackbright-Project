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
