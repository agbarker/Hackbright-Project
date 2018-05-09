"""Tests for Music Class app"""

import unittest

import server


class ServerTests(unittest.TestCase):
	"""Tests for music class site."""

	def setUp(self):
		"""Code to run before every test."""

		self.client = server.app.test_client()
		server.app.config['TESTING'] = True

	def test_homepage(self):
		"""Can we reach the homepage?"""

		result = self.client.get("/")
		self.assertIn("Music Class App", result.data)


	def test_student_register(self):
		"""Can students see registration form?"""

		result = self.client.get('/student-register')


if __name__ == "__main__":
    unittest.main()