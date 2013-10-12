#!/usr/bin/env python3
'''Tests for SpiralPrinter and related functions.'''
import sys
import unittest
from io import StringIO
from spiral import *


class Expected:
    EXAMPLE = '''20 21 22 23 24
19  6  7  8  9
18  5  0  1 10
17  4  3  2 11
16 15 14 13 12
'''

    SIX = '''6    \n\
5 0 1
4 3 2
'''

    FOUR = '''  0 1
4 3 2
'''

    TWO = '''0 1
  2
'''


class SpiralPrinterTest(unittest.TestCase):
    def setUp(self):
        self.string_output = StringIO()
        sys.stdout = self.string_output

    def test_example_output(self):
        SpiralPrinter(24).print_spiral()
        self.assertEqual(Expected.EXAMPLE, self.string_output.getvalue())

    def test_zero(self):
        SpiralPrinter(0).print_spiral()
        self.assertEqual('0\n', self.string_output.getvalue())

    def test_bound_expand_positive_x(self):
        SpiralPrinter(1).print_spiral()
        self.assertEqual('0 1\n', self.string_output.getvalue())

    def test_bound_expand_positive_y(self):
        SpiralPrinter(6).print_spiral()
        self.assertEqual(Expected.SIX, self.string_output.getvalue())

    def test_bound_expand_negative_x(self):
        SpiralPrinter(4).print_spiral()
        self.assertEqual(Expected.FOUR, self.string_output.getvalue())

    def test_bound_expand_negative_y(self):
        SpiralPrinter(2).print_spiral()
        self.assertEqual(Expected.TWO, self.string_output.getvalue())


class CommandLineTest(unittest.TestCase):
    def test_bad_argument(self):
        with self.assertRaises(BadArgumentsException):
            main(['progname', 'foo'])

    def test_too_many_arguments(self):
        with self.assertRaises(BadArgumentsException):
            main(['progname', '42', '42'])

    def test_too_few_arguments(self):
        with self.assertRaises(BadArgumentsException):
            main(['progname'])

    def test_negative_argument(self):
        with self.assertRaises(BadArgumentsException):
            main(['progname', '-1'])

    def test_good_argument(self):
        self.string_output = StringIO()
        sys.stdout = self.string_output
        main(['progname', '24'])

if __name__ == '__main__':
    unittest.main()
