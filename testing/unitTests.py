import unittest

from Explorate import create_app
from Explorate.config import TestingConfig
from Explorate.models import db, User, Adventure, UserSelection, Recommendations, Ratings
from Explorate.routes import recommend
class UnitTests(unittest.TestCase):
    def setUp(self):
        testApplication = create_app(TestingConfig)
        self.app_ctx = testApplication.app_context()
        self.app_ctx.push()
        db.create_all()
        self.client = testApplication.test_client()
        return super().setUp()
    
    def addUser(self, username, password):
        user = User(
            Username=username,
            email=f'{username}@example.com',
            password=password,
            country='Australia',
            dateofbirth='2000-1-1'
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    # test that we can add users to database
    def test_addUser(self):
        user = self.addUser(
            username='newuser',
            password='testpassword'
        )  
        
        retrieved_user = User.query.filter_by(email='newuser@example.com').first()
    
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.Username, 'newuser')
        
    # test that sign up works
    def test_signup(self):
        response = self.client.post('/sign-up', data={
            'Username':'testuser',
            'email':'testuser@example.com',
            'password1':'password123',
            'password2':'password123',
            'birthdate':'2000-01-01',
            'country':'Australia'
        })
        
        with self.client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            assert('success', 'Account created!' in flashes)
            
    #test sign up for existing email
    def test_signup_dupemail(self):
        #first user sign up
        self.client.post('/sign-up', data={
            'Username':'testuser',
            'email':'testuser@example.com',
            'password1':'password123',
            'password2':'password123',
            'birthdate':'2000-01-01',
            'country':'Australia'
        })
        
        #response to second user sign up
        response = self.client.post('/sign-up', data={
            'Username':'testuser2',
            'email':'testuser@example.com',
            'password1':'password456',
            'password2':'password456',
            'birthdate':'2000-01-01',
            'country':'Australia'
        })
        
        with self.client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            assert('error', 'Email already exists.' in flashes)
    
    #test a successful login
    def test_login_success(self):
        self.addUser(username='testUser', password='testpassword123')
        
        response = self.client.post('/login', data={
            'Username' : 'testUser',
            'password3': 'testpassword123'
        })
        
        with self.client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            assert('success', 'Logged in successfully!' in flashes)
        
    # test a failed login
    def test_login_fail(self):
        self.addUser(username='testUser', password='testpassword123')
        
        response = self.client.post('/login', data={
            'Username' : 'testUser',
            'password3': 'testpassword1234'
        })
        
        with self.client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            assert('error', 'Incorrect password, try again.' in flashes)
            
    # test a login where user doesnt exist
    def test_login_nonexist(self):
        response = self.client.post('/login', data={
            'Username' : 'testUser',
            'password3': 'testpassword1234'
        })
        
        with self.client.session_transaction() as sess:
            flashes = sess.get('_flashes', [])
            assert('error', 'Username does not exist.' in flashes)
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()
        return super().tearDown()