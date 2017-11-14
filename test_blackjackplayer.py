#test_blackjackplayer
import unittest
import blackjackplayer
from peewee import *
from user import User

class testUser(unittest.TestCase):
    fixture_two = User.create(slack_id = 00000, name = "test_user", trolled = 0)
    fixture_two.save()

    #def setUp():
        #set up the test database
        #self.fixture_one = database
        #create tables
        #maybe populate with data?
        #self.fixture_two.save()
        #pass

    #def tearDown():
        #delete the test database
        #del self.fixture_one
        #del fixture_two

    def test_init(self):
        "test should create a user in one case and not the other" #need to fix assert methods
        a, b = User.get_or_create(id = self.fixture_two.id)
        print(a, b)
        c, d = User.get_or_create(id = " ")
        print(c, d)
        self.assertNotEqual(a, c)
        self.assertNotEqual(b, d)

    def test_testing(self):
        "testing to see if we're running tests"
        a = 2
        b = 3
        self.assertEqual(a, b)

if __name__ == "__main__":
    unittest.main()
