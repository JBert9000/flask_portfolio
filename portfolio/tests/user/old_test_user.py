import unittest
from portfolio import db, create_app
from portfolio.users.routes import users
from portfolio.config import Config


app = create_app()

TEST_DB = 'test.db'

class TestUser(unittest.TestCase):

# Setup and Teardown

    def setUp(self):
        Config['TESTING'] = True
        Config['WTF_CSRF_ENABLED'] = False
        Config['DEBUG'] = False
        Config['SQLALCHEMY_DATABASE_URI'] = 'sqli'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        print('Done test.')

# Tests

    def test_register(self):
        response = self.app.get(users.route("/register/"))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
