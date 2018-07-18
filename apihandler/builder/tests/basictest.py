import unittest
from django.test import TestCase


class TestBasic(unittest.TestCase):
	def test_basic(self):
		a = 1
		self.assertEqual(1, a)

	def test_basic_2(self):
		a = 1
		assert a == 1


if __name__ == '__main__':
	unittest.main()