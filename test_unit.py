import unittest
import ugen
import os

class ugenTest(unittest.TestCase):

    def setUp(self):
        self.row1 = ['1234', 'Jozef', 'Miloslav', 'Hurban', 'Legal']
        self.row2 = ['4444', 'Jozef', '', 'Hurban', 'IT']
        self.row3 = ['1234', 'Jozef', 'Miloslav', 'Hurban', 'Legal']
        self.row4 = ['1234', 'Jozef', 'Miloslav', 'Abcdefghijklmnop', 'Legal']
        
        self.row5 = ['12ss', 'Jozef', 'Miloslav', 'Hurban', 'Legal']
        self.row6 = ['1234', 'Jo zef', 'Miloslav', 'Hurban', 'Legal']
        self.row7 = ['1234', 'Jozef', 'miloslav', 'Hurban', 'Legal']
        
        self.setOfUserNames = set()
        
    def test_readFile(self):
        self.assertIsInstance(ugen.readFile('input_file1.txt'), list)
        self.assertRaises(FileNotFoundError, ugen.readFile, 'wrongfile')

    def test_generateUserName(self):
        self.assertEqual(ugen.generateUserName(self.row1, self.setOfUserNames), 'jmhurban')
        self.assertEqual(ugen.generateUserName(self.row2, self.setOfUserNames), 'jhurban')
        self.assertEqual(ugen.generateUserName(self.row3, self.setOfUserNames), 'jmhurban1')
        self.assertEqual(ugen.generateUserName(self.row4, self.setOfUserNames), 'jmabcdef')
        

    def test_validateOneRow(self):    
        self.assertEqual(ugen.validateOneRow(self.row5), (False, 0))
        self.assertEqual(ugen.validateOneRow(self.row6), (False, 1))
        self.assertEqual(ugen.validateOneRow(self.row7), (False, 2))
        self.assertEqual(ugen.validateOneRow(self.row1), (True, ''))
        

    def test_parseFile(self):
        fileContent = []
        fileContent.append(self.row1)
        fileContent.append(self.row2)
        fileContent.append(self.row5)
        fileContent.append(self.row6)
        result = ugen.parseFile(fileContent, self.setOfUserNames)
        self.assertIsInstance(result, list)
        resultCorrect = [
                        ['1234', 'jmhurban', 'Jozef', 'Miloslav', 'Hurban', 'Legal'],
                        ['4444', 'jhurban', 'Jozef', '', 'Hurban', 'IT'],
                        ['IncorrectValue', '', 'Jozef', 'Miloslav', 'Hurban', 'Legal'],
                        ['1234', '', 'IncorrectValue', 'Miloslav', 'Hurban', 'Legal']
                        ]
        self.assertEqual(result, resultCorrect)

    def test_writeToOutputFile(self):
        ugen.writeToOutputFile([''], 'testoutput.txt')
        self.assertTrue(os.path.isfile('testoutput.txt'))
        os.remove('testoutput.txt')


