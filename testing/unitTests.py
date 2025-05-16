import unittest

from Explorate import create_app
from Explorate.auth import TestingConfig
from Explorate.models import db
from Explorate.routes import recommend
class UnitTests(unittest.TestCase):
    def setUp(self):
        testApplication = create_app(TestingConfig)
        return super().setUp()

    def test_reccommend(self):
        pass
        
    def tearDown(self):
        return super().tearDown()