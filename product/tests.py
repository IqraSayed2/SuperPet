from django.test import TestCase
from.Calculator import Calculator

# Create your tests here.

class CalculatorTest(TestCase):
    def setUp(self):
        self.c=Calculator()

    def test_add(self):
        self.assertEqual(self.c.add(12,10),22)    #actual,expected
        self.assertEqual(self.c.add(5,5),10)

    def test_subtract(self):
        self.assertEqual(self.c.subtract(12,10),2)  
        self.assertEqual(self.c.subtract(5,5),0)

    def test_isEven(self):
        self.assertTrue(self.c.is_even(4))
        self.assertTrue(self.c.is_even(30))
        self.assertFalse(self.c.is_even(1))
        self.assertFalse(self.c.is_even(5))
        with self.assertRaises(TypeError):
            self.c.is_even("A")

    def test_isOdd(self):
        self.assertTrue(self.c.is_odd(3))
        self.assertFalse(self.c.is_odd(30))