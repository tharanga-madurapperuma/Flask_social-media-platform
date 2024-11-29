"""User View tests."""

import os
from unittest import TestCase
from models import db, User

os.environ['DATABASE_URL'] = "postgresql://postgres:Aa2000928#@localhost/warbler-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        User.query.delete()

        self.client = app.test_client()

        self.user = User.signup("testuser", "test@gmail.com", "password", None)
        db.session.commit()


    def test_show_following_logged_in(self):
        """Can a logged-in user see the following page?"""

        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.user.id

            response = c.get(f"/users/{self.user.id}/following")
            self.assertEqual(response.status_code, 200)


    def test_show_following_logged_out(self):
        """Are logged-out users prohibited from seeing the following page?"""

        with self.client as c:
            response = c.get(f"/users/{self.user.id}/following", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("Access unauthorized.", str(response.data))
