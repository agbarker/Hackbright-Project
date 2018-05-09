"""Tests for Music Class app"""

import unittest

from server import app, session
from model import db, connect_to_db, example_data


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

    def test_student_register_page(self):
        """Can students see registration form?"""

        result = self.client.get('/student-register')
        self.assertIn("Enter Class Registration Code", result.data)




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
        # import pdb; pdb.set_trace()


    def test_student_register(self):
        """Can students register?"""

        student_info = {'class-code': "ABC", 'username': "bjones", 'password': "password", 'fname': "Brad", 'lname': "Jones"}

        result = self.client.post("/student-register", data=student_info, follow_redirects=True)

        test_student = Student.query.get(client.session["student_id"])

        self.assertIn("Brad Jones", result_url)



    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()



if __name__ == "__main__":
    unittest.main()
