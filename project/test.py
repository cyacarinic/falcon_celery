# project/test.py
import unittest
from app import app
from falcon import testing


class TestAppRoutes(testing.TestCase):
    def setUp(self):
        super(TestAppRoutes, self).setUp()
        self.app = app

    def test_get_message(self):
        result = self.simulate_get('/ping')
        self.assertEqual(result.json, 'pong!')


if __name__ == '__main__':
    unittest.main()
