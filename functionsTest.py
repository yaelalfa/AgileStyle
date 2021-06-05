import unittest
import functions
import random

class MyTestCase(unittest.TestCase):



    def test_insert_to_table(self):

        tes = functions.insert_to_table(random.randint(20,100),1,1)
        self.assertEqual(tes, 1)

    def test_projectManager(self):
        tes = functions.projectManager(4)
        self.assertEqual(tes,"nuri")

    def test_insert_user(self):
        tes = functions.insert_user(random.randint(20, 100), 1, "manager")
        self.assertEqual(tes, 1)

    def test_new_message(self):
        tes = functions.new_message("s", "t", "test")
        self.assertEqual(tes, 1)

    def test_userInproj(self):
        t = functions.userInproj(1)
        self.assertEqual(t, "x")









if __name__ == '__main__':
    unittest.main()
