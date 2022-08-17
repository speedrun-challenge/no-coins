# -*- coding: utf-8 -*-
import unittest

from util import is_before_deadline


class TestMethods(unittest.TestCase):

  def test_is_before_deadline(self):
    self.assertTrue(is_before_deadline('2022-08-16T18:32:45Z'))
    self.assertTrue(is_before_deadline('2022-09-01T12:00:00Z'))
    self.assertTrue(is_before_deadline('2022-09-04T02:59:59Z'))

    self.assertFalse(is_before_deadline('2022-09-04T03:00:00Z'))
    self.assertFalse(is_before_deadline('2022-09-04T03:00:01Z'))
    self.assertFalse(is_before_deadline('2023-01-01T01:00:00Z'))


if __name__ == '__main__':
  unittest.main()
