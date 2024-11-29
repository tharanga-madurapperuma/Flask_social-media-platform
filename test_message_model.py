"""Message Model Test"""

import os
from unittest import TestCase
from models import db, User, Likes, Message
from app import app

os.environ['DATABASE_URL'] = "postgresql://postgres:<password>@localhost/warbler-test"

from app import app

db.create_all()

class MessageModelTestCase(TestCase):
    """Test Message model"""

    def setUp(self):    
        """Create test client, add data"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.user = User.signup("testUser", "test@gmail.com", "password", None)
        db.session.commit()

        self.message = Message(text="Test message", user_id=self.user.id)
        db.session.add(self.message)
        db.session.commit()
        

    def tearDown(self):
        """Clean up transactions."""

        db.session.rollback()


    def test_message_model(self):
        """Does the basic model work?"""

        self.assertEqual(self.message.text, "Test message")
        self.assertEqual(self.message.user_id, self.user.id)

        