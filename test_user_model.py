"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql://postgres:Aa2000928#@localhost/warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        self.user1 = User.signup("user1", "user1@gmail.com", "password", None)
        self.user2 = User.signup("user2", "user2@gmail.com", "password", None)

        db.session.commit()

    
    def tearDown(self):
        db.session.rollback()


    def test_repr(self):
        """Does the repr method work as expected?"""
        self.assertEqual(
            repr(self.user1), f"<User #{self.user1.id}: user1, user1@gmail.com>"
        )


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@gmail.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    
    def test_is_following(self):
        """Does is_following correctly identify following status?"""

        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertTrue(self.user1.is_following(self.user2))
        self.assertFalse(self.user2.is_following(self.user1))


    def test_is_followed_by(self):
        """Does is_followed_by correctly identify followed-by status?"""

        self.user1.followers.append(self.user2)
        db.session.commit()

        self.assertTrue(self.user1.is_followed_by(self.user2))
        self.assertFalse(self.user2.is_followed_by(self.user1))


    def test_signup(self):
        """Does User.signup successfully create a new user?"""

        user = User.signup("newuser", "new@gmail.com", "password", None)
        db.session.commit()

        self.assertIsInstance(user, User)
        self.assertEqual(user.username, "newuser")


    def test_signup_invalid(self):
        """Does User.signup fail with invalid data?"""

        User.signup(None, "test@gmail.com", "password", None)

        with self.assertRaises(exc.IntegrityError):
             db.session.commit()


    def test_authenticate(self):
        """Does User.authenticate successfully return a user?"""

        user = User.authenticate("user1", "password")
        self.assertEqual(user, self.user1)


    def test_authenticate_invalid(self):
        """Does User.authenticate fail with invalid username/password?"""
        self.assertFalse(User.authenticate("user1", "wrongpassword"))
        self.assertFalse(User.authenticate("wronguser", "password"))