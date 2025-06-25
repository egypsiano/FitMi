import unittest
from app import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    def test_main_page(self):
        # Send a GET request to the '/' route
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, FitMi!", response.data)
        self.assertIn(b"Welcome to your new fitness tracking application.", response.data)

if __name__ == "__main__":
    unittest.main()
