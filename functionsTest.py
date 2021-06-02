import unittest
import functions
import random

class MyTestCase(unittest.TestCase):



    def test_insert_to_table(self):

        t=functions.insert_to_table(random.randint(20,100),1,1)
        self.assertEqual(t, 1)

    def test_projectManager(self):
        t = functions.projectManager(4)
        self.assertEqual(t,"nuri")

    def test_insert_user(self):
        t = functions.insert_user(random.randint(20, 100), 1, "manager")
        self.assertEqual(t, 1)









if __name__ == '__main__':
    unittest.main()
