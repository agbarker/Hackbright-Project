"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import datetime
from sqlalchemy import func

from model import connect_to_db, db, Teacher, Classroom, Student, Group, StudentGroup, Music, ListeningSurvey, GroupSurvey, ClassroomSurvey, StudentSurvey, Instrument, InstrumentType, ClassroomInstrumentType, Composer, Period, ComposerPeriod, Avatar
from server import app


def load_teachers(teachers_filename):
    """Load teachers into database."""

    print "Teacher"

    for i, row in enumerate(open(teachers_filename)):
        username, password, fname, lname = row.split("|")

        teacher = Teacher(username=username, password=password, fname=fname, lname=lname)

        db.session.add(teacher)

        if i % 10 == 0:
            print i

    db.session.commit()


def load_classrooms(classrooms_filename):
    """Load classrooms."""

    print "Classroom"

    for i, row in enumerate(open(classrooms_filename)):
        row = row.rstrip()

        teacher_id, registration_code, name, type_class, survey_goal = row.split("|")

        classroom = Classroom(teacher_id=teacher_id, registration_code=registration_code, name=name, type_class=type_class, survey_goal=survey_goal)

        db.session.add(classroom)

        if i % 10 == 0:
            print i

    db.session.commit()

def load_avatars(avatars_filename):
    """Load avatars."""

    print "Avatar"

    for i, row in enumerate(open(avatars_filename)):
        row = row.rstrip()

        avatar_src = row

        avatar = Avatar(avatar_src=avatar_src)

        db.session.add(avatar)

        if i % 10 == 0:
            print i

    db.session.commit()


def load_students(students_filename):
    """Load students."""

    print "Student"

    for i, row in enumerate(open(students_filename)):
        row = row.rstrip()

        username, password, fname, lname, class_id = row.split("|")

        student = Student(username=username, password=password, fname=fname, lname=lname, class_id=class_id, avatar_id=i+1)

        db.session.add(student)

        if i % 10 == 0:
            print i

    db.session.commit()


def load_instrument_types(instrument_types_filename):
    """Load instrument types."""

    print "InstrumentType"

    for i, row in enumerate(open(instrument_types_filename)):
        row = row.rstrip()

        name, family, key = row.split("|")

        instrument_type = InstrumentType(name=name, family=family, key=key)

        db.session.add(instrument_type)

        if i % 10 == 0:
            print i

    
    db.session.commit()


def load_classroom_instrument_types(classroom_instrument_types_filename):
    """Load classroom_instrument_types."""

    print "ClassroomInstrumentType"


    for i, row in enumerate(open(classroom_instrument_types_filename)):
        row = row.rstrip()

        instrument_id, class_id = row.split(" | ")

        classroom_instrument_type = ClassroomInstrumentType(instrument_id=instrument_id, class_id=class_id)

        db.session.add(classroom_instrument_type)

        if i % 10 == 0:
            print i

    db.session.commit()


def load_instruments(instruments_filename):
    """Load instruments."""

    print "Instrument"

    for i, row in enumerate(open(instruments_filename)):
        row = row.rstrip()

        serial_number, student_id, instrument_name, teacher_id, maker, model, year_manufactured, repair, repair_note = row.split("|")

        instrument = Instrument(serial_number=serial_number, student_id=student_id, instrument_name=instrument_name, teacher_id=teacher_id, maker=maker, model=model, year_manufactured=year_manufactured, repair=repair, repair_note=repair_note)

        db.session.add(instrument)

        if i % 10 == 0:
            print i

    db.session.commit()


def load_composers(composers_filename):
    """Load composers."""

    print "Composer"

    for i, row in enumerate(open(composers_filename)):
        row = row.rstrip()

        name, bdate, ddate, country, period = row.split("|")
        bdate = int(bdate)
        ddate = int(ddate)

        composer = Composer(name=name, bdate=bdate, ddate=ddate, country=country)

        db.session.add(composer)

        period_tokens = period.split("/")

        for item in period_tokens:

            all_periods = Period.query.all()
            periods=[]
            for period in all_periods:
                periods.append(period.name)


            if item not in periods:
                new_period = Period(name=item)
                db.session.add(new_period)

            new_composer_period = ComposerPeriod(period_id=item, composer_id=composer.name)
            db.session.add(new_composer_period)


        if i % 10 == 0:
            print i

    db.session.commit()


def load_music(music_filename):
    """Load music."""

    print "Music"

    for i, row in enumerate(open(music_filename)):
        row = row.rstrip()

        # print row

        name, youtube_id, composer, ensemble = row.split("|")

        music = Music(name=name, youtube_id=youtube_id, composer_id=composer, ensemble=ensemble)


        db.session.add(music)


        if i % 10 == 0:
            print i

    db.session.commit()


def create_surveys():
    """Creates surveys from music files."""

    all_music = Music.query.all()

    for piece in all_music:
        new_survey = ListeningSurvey(music_id=piece.music_id)
        db.session.add(new_survey)

    db.session.commit()







def set_val_student_id():
    """Set value for the next student_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Student.student_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('students_student_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_teacher_id():
    """Set value for the next teacher_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Teacher.teacher_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('teachers_teacher_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_class_id():
    """Set value for the next class_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Classroom.class_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('classrooms_class_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


# def set_val_survey_id():
#     """Set value for the next survey_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(ListeningSurvey.survey_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('surveys_survey_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


def set_val_classroom_instrument_type_id():
    """Set value for the next classroom_instrument_type_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(ClassroomInstrumentType.classroom_instrument_type_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('classroom_instrument_type_instrument_type_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()







if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_teachers("seed_data/teacher_seed.txt")
    load_classrooms("seed_data/classroom_seed.txt")
    load_avatars("seed_data/avatar_seed.txt")
    load_students("seed_data/student_seed.txt")
    load_instrument_types("seed_data/instrument_types_seed.txt")
    load_classroom_instrument_types("seed_data/classroom_instrument_type_seed.txt")
    load_instruments("seed_data/instrument_seed.txt")
    load_composers("seed_data/composers_seed.txt")
    load_music("seed_data/music_seed_actual.txt")
    create_surveys()
    set_val_student_id()
    set_val_teacher_id()
    set_val_class_id()
    # set_val_survey_id()
    set_val_classroom_instrument_type_id


    
