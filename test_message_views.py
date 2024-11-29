"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase
from models import db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://postgres:Aa2000928#@localhost/warbler-test"


# Now we can import app
    
from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.user = User.signup("testuser", "test@test.com", "password", None)
        db.session.commit()


    def test_add_message(self):
        """Can a logged-in user add a message?"""

        with self.client as c:
            with c.session_transaction() as session:
                session[CURR_USER_KEY] = self.user.id

            response = c.post("/messages/new", data={"text": "Hello"})
            self.assertEqual(response.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")


    def test_delete_message(self):
        """Can a logged-in user delete their own message?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            msg = Message(text="Test delete", user_id=self.user.id)
            db.session.add(msg)
            db.session.commit()

            response = c.post(f"/messages/{msg.id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            self.assertEqual(Message.query.count(), 0)
