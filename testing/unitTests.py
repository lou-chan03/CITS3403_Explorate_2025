import unittest

class UnitTests(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    def test_example(self):
        self.assertEqual(1 + 1, 2)
        
    def tearDown(self):
        return super().tearDown()