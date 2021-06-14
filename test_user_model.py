"""User model tests."""

# run these tests like:
#   createdb warbler-test
#   python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

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

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        # create user
        self.user1 = User.signup(email='test1@test.com', username='testuser1', password='password', image_url=None)
        self.user2 = User.signup(email='test2@test.com', username='testuser2', password='password', image_url=None)

        # add to session & commit 
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit() 

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers 
        # & no likes
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.likes), 0)
    
    def test_repr(self):
        user1 = repr(self.user1)
        self.assertIn('test1', user1)
        self.assertIn('testuser1', user1)
    
    def test_is_following(self):
        # user1 follow user2
        self.user1.following.append(self.user2)
        db.session.commit() 

        self.assertEqual(len(self.user2.following), 0)
        self.assertEqual(len(self.user2.followers), 1)
        self.assertEqual(len(self.user1.followers), 0)
        self.assertEqual(len(self.user1.following), 1) 
    
    def test_signup(self): 
        user = User.signup("test4", "test4@test.com", "password", None)
        user.id = 952139000
        db.session.commit()
        testuser = User.query.get(user.id)
        self.assertIsNotNone(testuser)
        self.assertEqual(testuser.username, "test4")
        self.assertEqual(testuser.email, "test4@test.com")
        self.assertNotEqual(testuser.password, "password")

    def test_user_authentication(self):
        user = User.authenticate(self.user2.username, 'password')
        self.assertEqual(user.id, self.user2.id)


