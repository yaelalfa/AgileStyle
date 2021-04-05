import unittest
import agileStyle as project
from tkinter import *

totest = project.main(Tk(),test=False)


class MyTestCase(unittest.TestCase):
    # def test_upper(self):
    #     a=totest.getData('linoyS')
    #     self.assertIsNotNone(a)

    def testMainGetUser(self):
        totest.username = 'linoy'
        totest.password = 'kloug'
        vUser = totest.login()
        self.assertTrue(vUser == None)
        totest.username = 'linoy'
        totest.password = 'linoy'
        vUser = totest.login()
        self.assertTrue(vUser != None and upper(vUser[3]) == 'manager')
        totest.username = 'noamp'
        totest.password = 'noamp'
        vUser = totest.login()
        self.assertTrue(vUser != None and upper(vUser[3]) == 'customer')
        totest.username = 'linoy'
        totest.password = 'linoy'
        vUser = totest.login()
        self.assertTrue(vUser != None and upper(vUser[3]) == 'developer')

    def testDb2(self):
        returnStatement = totest.getUser()
        self.assertTrue(len(returnStatement) > 1)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_something(self):
        self.assertEqual(True, False)





if __name__ == '__main__':
    unittest.main()
