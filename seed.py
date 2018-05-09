"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import datetime
from sqlalchemy import func

from model import connect_to_db, db, Teacher, Classroom, Student, Group, StudentGroup, Music, ListeningSurvey, GroupSurvey, ClassroomSurvey, StudentSurvey, Instrument, InstrumentType, ClassroomInstrumentType
from server import app


def load_teacher():
    """Load one teacher into database."""

    print "Teacher"

    teacher = Teacher(username="sbarber", password="password", fname="samuel", lname="barber")
    db.session.add(teacher)
    db.session.commit()


def load_classroom():
    """Load one classroom."""

    print "Classroom"

    classroom = Classroom(teacher_id=1, registration_code="XYZ", name="Beginning Band", type_class="Concert Band/Wind Ensemble")
        
    db.session.add(classroom)
    db.session.commit()


def load_student():
    """Load one student."""

    print "Student"

    student = Student(username="jdoe", password="password", fname="Jane", lname="Doe", class_id=1)

    db.session.add(student)
    db.session.commit()


def load_instrument_type():
    """Load one instrument type."""

    print "InstrumentType"

    instrument_type = InstrumentType(name="Clarinet", family="Woodwind")

    db.session.add(instrument_type)
    db.session.commit()


def load_classroom_instrument_type():
    """Load one classroom_instrument_type."""

    print "ClassroomInstrumentType"

    classroom_instrument_type = ClassroomInstrumentType(instrument_id="Clarinet", class_id=1)

    db.session.add(classroom_instrument_type)
    db.session.commit()


def load_instrument():
    """Load one instrument."""

    print "Instrument"

    instrument = Instrument(serial_number="CL-3456", student_id=1, instrument_name='Clarinet', teacher_id=1, maker="Buffet", model='B12', year_manufactured=2009)

    db.session.add(instrument)
    db.session.commit()


def set_val_student_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Student.student_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('students_student_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_teacher()
    load_classroom()
    load_student()
    load_instrument_type()
    load_classroom_instrument_type()
    load_instrument()
    set_val_student_id()

    # Mimic what we did in the interpreter, and add the Eye and some ratings
    
