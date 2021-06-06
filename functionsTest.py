import unittest
import functions
import random

class MyTestCase(unittest.TestCase):



    def test_insert_to_table(self):

        tes = functions.insert_to_table(random.randint(20,100),1,1,"2024")
        print(tes)
        self.assertEqual(tes, 1)

    def test_projectManager(self):
        tes = functions.projectManager(1)
        self.assertEqual(tes,"nuri")




    def test_insert_user(self):
        tes = functions.insert_user(random.randint(20, 100), 1, "manager")
        self.assertEqual(tes, 1)

    def test_new_message(self):
        tes = functions.new_message("s", "t", "test")
        self.assertEqual(tes, 1)

    def test_userInproj(self):
        tes = functions.userInproj(1)
        self.assertEqual(tes, "lindd")


    ###############################בדיקות אינטגקציה##############################
    def test_intgration(self):
        n=random.randint(1,100)

        name="test"+str(n)

        pas="123"

        role="developer"

        t1=functions.new_user(name,pas,role)

        self.assertEqual(t1, 1)


        t2=functions.login(name,pas)

        self.assertEqual(t2, role)











if __name__ == '__main__':
    unittest.main()
