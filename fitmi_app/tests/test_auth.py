import unittest
import werkzeug # Import werkzeug to inspect
from app import app, db
from app.models import User

class AuthTests(unittest.TestCase):

    def setUp(self):
        print(f"AuthTests: Werkzeug imported: {werkzeug}")
        print(f"AuthTests: Werkzeug version: {hasattr(werkzeug, '__version__') and werkzeug.__version__ or 'NOT FOUND'}")
        print(f"AuthTests: Werkzeug file: {hasattr(werkzeug, '__file__') and werkzeug.__file__ or 'NOT FOUND'}")
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing forms
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory SQLite for tests
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def register_user(self, username, email, password):
        return self.client.post('/register', data=dict(
            username=username,
            email=email,
            password=password,
            confirm_password=password
        ), follow_redirects=True)

    def login_user(self, email, password):
        return self.client.post('/login', data=dict(
            email=email,
            password=password
        ), follow_redirects=True)

    def logout_user(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_01_register_page_loads(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create an Account', response.data)

    def test_02_successful_registration(self):
        response = self.register_user('testuser1', 'test1@example.com', 'password123')
        self.assertEqual(response.status_code, 200) # Should redirect to login
        self.assertIn(b'Congratulations, you are now a registered user!', response.data)
        user = User.query.filter_by(email='test1@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser1')

    def test_03_duplicate_username_registration(self):
        self.register_user('testuser2', 'test2@example.com', 'password123')
        response = self.register_user('testuser2', 'test3@example.com', 'password123')
        self.assertEqual(response.status_code, 200) # Stays on register page
        self.assertIn(b'That username is taken.', response.data)

    def test_04_duplicate_email_registration(self):
        self.register_user('testuser4', 'test4@example.com', 'password123')
        response = self.register_user('testuser5', 'test4@example.com', 'password123')
        self.assertEqual(response.status_code, 200) # Stays on register page
        self.assertIn(b'That email is already registered.', response.data)

    def test_05_login_page_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_06_successful_login_logout(self):
        self.register_user('loginuser', 'login@example.com', 'password123')

        # Test login
        response_login = self.login_user('login@example.com', 'password123')
        self.assertEqual(response_login.status_code, 200) # Redirects to dashboard
        self.assertIn(b'Dashboard', response_login.data) # Check for dashboard content
        self.assertIn(b'Login successful!', response_login.data)
        self.assertIn(b'Welcome, loginuser!', response_login.data)


        # Test access to protected page (dashboard)
        response_dashboard = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response_dashboard.status_code, 200)
        self.assertIn(b'Welcome, loginuser!', response_dashboard.data)

        # Test logout
        response_logout = self.logout_user()
        self.assertEqual(response_logout.status_code, 200) # Redirects to index
        self.assertIn(b'You have been logged out.', response_logout.data)
        self.assertIn(b'Hello, FitMi!', response_logout.data) # Back on index

        # Test dashboard is protected after logout
        response_dashboard_after_logout = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response_dashboard_after_logout.status_code, 200) # Redirects to login
        self.assertIn(b'Please log in to access this page.', response_dashboard_after_logout.data) # Flash message from Flask-Login

    def test_07_login_invalid_credentials(self):
        self.register_user('creduser', 'cred@example.com', 'password123')
        response = self.login_user('cred@example.com', 'wrongpassword')
        self.assertEqual(response.status_code, 200) # Stays on login page
        self.assertIn(b'Login Unsuccessful. Please check email and password', response.data)

    def test_08_login_nonexistent_user(self):
        response = self.login_user('noexist@example.com', 'password123')
        self.assertEqual(response.status_code, 200) # Stays on login page
        self.assertIn(b'Login Unsuccessful. Please check email and password', response.data)

if __name__ == '__main__':
    unittest.main()
