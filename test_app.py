import unittest
from StoryMaker import MemMaker
class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.MemMaker = MemMaker.test_client()
        MemMaker.testing = True
        # Perform any additional setup here, if needed.

    def tearDown(self):
        pass
        # Perform any necessary cleanup here, if needed.

    def test_index_route(self):
        response = self.MemMaker.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Welcome to StoryMaker</h1>', response.data)

    def test_access_database_route(self):
        response = self.MemMaker.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Access Database</h1>', response.data)
        self.assertIn(b'<table>', response.data)
        # Add more assertions to check other elements in the response data

    # Add more test methods to cover other routes and functionalities
    # For example:
    # def test_add_new_code(self):
    #     # Test adding a new code snippet to the database and check if it MemMakerears in the database.
    #     # Assert that the response redirects to the correct page.

if __name__ == '__main__':
    unittest.main()
