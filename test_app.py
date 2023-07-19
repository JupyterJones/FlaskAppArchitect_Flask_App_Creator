import unittest
from StoryMaker.app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome to StoryMaker</h1>', response.data)

    def test_access_database_route(self):
        response = self.app.get('/access_database')
        self.assertEqual(response.status_code, 200)
        # Add more assertions to check the response data for this route

    # Add more test methods to cover other routes and functionalities

if __name__ == '__main__':
    unittest.main()

