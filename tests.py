"""Tests for Music Class app"""

import unittest

from server import app, session
from model import connect_to_db, db, Teacher, Classroom, Student, Group, StudentGroup, Music, ListeningSurvey, GroupSurvey, ClassroomSurvey, StudentSurvey, Instrument, InstrumentType, ClassroomInstrumentType, example_data


class ServerTests(unittest.TestCase):
    """Tests for music class site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn("Music Class App", result.data)

    def test_teacher_register_page(self):
        """Can teachers see registration form?"""

        result = self.client.get('/teacher-register')
        self.assertIn("Teachers Register", result.data)

    def test_student_register_page(self):
        """Can students see registration form?"""

        result = self.client.get('/student-register')
        self.assertIn("Enter Class Registration Code", result.data)

    def test_student_log_in_page(self):
        """Can student see log in page?"""

        result = self.client.get('/student-login')
        self.assertIn("Student Login", result.data)





class MusicClassTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()


    def test_teacher_register(self):
        """Can teachers register?"""

        teacher_info = {'username': "wdisney", 'password': "password", 'fname': "Walt", 'lname': "Disney"}
        result = self.client.post("/teacher-register", data=teacher_info, follow_redirects=True)
        self.assertIn("Walt Disney", result.data)


    def test_teacher_create_class(self):
        """Can teacher create a class?"""

        import pdb; pdb.set_trace()

        new_teacher = Teacher(username="wdisney", password="password", fname="Walt", lname="Disney")
        db.session.add(new_teacher)
        db.session.commit()

        teacher_id = Teacher.query.filter_by(username='wdisney').one().teacher_id

        with app.test_client() as c:
            with c.session_transaction() as sess:
                sess['teacher_id'] = teacher_id

        create_class_info = {'registration code': "999", 'name': "6th Period Band", 'type_class': "marching_band"}
        result=self.client.post("/create-class", data=create_class_info, follow_redirects=True)
        self.assertIn("6th Period Band", result.data)


    def test_student_register(self):
        """Can students register?"""

        student_info = {'class-code': "ABC", 'username': "bjones", 'password': "password", 'fname': "Brad", 'lname': "Jones"}
        result = self.client.post("/student-register", data=student_info, follow_redirects=True)
        self.assertIn("Brad Jones", result.data)





    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()



if __name__ == "__main__":
    unittest.main()
