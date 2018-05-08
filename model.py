from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


#####################################################################
# Model definitions

class Teacher(db.Model):
    """Teacher user of website."""

    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Teacher fname={} lname={}>".format(self.fname, self.lname)


class Classroom(db.Model):
    """Classroom group of website."""

    __tablename__ = "classrooms"

    class_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    registration_code = db.Column(db.String(64))
    name = db.Column(db.String(64))
    type_class = db.Column(db.String(64))

    # Define relationship to teacher
    teacher = db.relationship("Teacher", backref=db.backref("classrooms", order_by=class_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Class name={} belongs to Teacher teacher_id={}>".format(self.name, self.teacher_id)


class Student(db.Model):
    """Student user of classroom website."""

    __tablename__ = "students"

    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))
    instrument = db.Column(db.String(64))
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'))

    # Define relationship to classroom
    classroom = db.relationship("Classroom", backref=db.backref("students", order_by=student_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Student fname={} lname={} in Classroom class_id={}>".format(self.fname, self.lname, self.class_id)


class Group(db.Model):
    """Groups within each class."""

    __tablename__ = "groups"

    group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'))
    name = db.Column(db.String(64))

    # Define relationship to classroom
    classroom = db.relationship("Classroom", backref=db.backref("groups", order_by=group_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Group name={} is in Classroom class_id={}>".format(self.name, self.class_id)


class StudentGroup(db.Model):
    """Relational database between Students and Groups."""

    __tablename__ = "student-group"

    student_group_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))

    # Define relationship to students
    student = db.relationship("Student", backref=db.backref("student-group", order_by=student_group_id))

    # Define relationship to groups
    group = db.relationship("Group", backref=db.backref("student-group", order_by=student_group_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Student student_id={} is in Group group_id={}>".format(self.student_id, self.group_id)


class Music(db.Model):
    """Music file objects."""

    __tablename__ = "music"

    music_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(64))
    score_src = db.Column(db.String(256))
    mp3_src = db.Column(db.String(256))
    composer = db.Column(db.String(64))
    ensemble = db.Column(db.String(64))
    midi_src = db.Column(db.String(256))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Piece name={} is composed by composer={}>".format(self.name, self.composer)


class Listening_Survey(db.Model):
    """Listening surveys (not yet assigned)."""

    __tablename__ = "surveys"

    survey_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.music_id'))

    # Define relationship to music
    music = db.relationship("Music", backref=db.backref("surveys", order_by=survey_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Survey survey_id={} uses Music music_id={}>".format(self.survey_id, self.music_id)


class GroupSurvey(db.Model):
    """Relational database between Groups and Listening Surveys."""

    __tablename__ = "group-survey"

    group_survey_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'))

    # Define relationship to surveys
    survey = db.relationship("Listening_Survey", backref=db.backref("group-survey", order_by=group_survey_id))

    # Define relationship to groups
    group = db.relationship("Group", backref=db.backref("group-survey", order_by=group_survey_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Survey survey_id={} is assigned to Group group_id={}>".format(self.survey_id, self.group_id)


class ClassroomSurvey(db.Model):
    """Relational database between Classes and Surveys."""

    __tablename__ = "class-survey"

    class_survey_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'))

    # Define relationship to surveys
    survey = db.relationship("Listening_Survey", backref=db.backref("class-survey", order_by=class_survey_id))

    # Define relationship to classrooms
    classroomm = db.relationship("Classroom", backref=db.backref("class-survey", order_by=class_survey_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Survey survey_id={} is assigned to Classroom class_id={}>".format(self.survey_id, self.class_id)


class StudentSurvey(db.Model):
    """Relational database between Students and Surveys."""

    __tablename__ = "student-survey"

    assigned_listening_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.survey_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    completed_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    student_comment = db.Column(db.Text, nullable=True)

    # Define relationship to surveys
    survey = db.relationship("Listening_Survey", backref=db.backref("student-survey", order_by=assigned_listening_id))

    # Define relationship to classrooms
    student = db.relationship("Student", backref=db.backref("student-survey", order_by=assigned_listening_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Survey survey_id={} is assigned to Student student_id={}>".format(self.survey_id, self.student_id)



#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///musicClass'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."