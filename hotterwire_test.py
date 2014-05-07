'''
Created on Apr 6, 2014

@author: ncliang
'''
import unittest
import hotterwire
import datetime


class Test(unittest.TestCase):
  def testSanitizeStarStr(self):
    self.assertEquals("4.0", hotterwire.SanitizeStarStr("4"))
    self.assertEquals("4.5", hotterwire.SanitizeStarStr("4.5"))

  def testIsWeekend(self):
    self.assertTrue(hotterwire.IsWeekend(datetime.date(2014, 04, 06)))
    self.assertTrue(hotterwire.IsWeekend(datetime.date(2014, 04, 05)))
    self.assertFalse(hotterwire.IsWeekend(datetime.date(2014, 04, 04)))


  def testContainsWeekend(self):
    self.assertTrue(hotterwire.ContainsWeekend(
        datetime.date(2014, 04, 04),
        datetime.date(2014, 04, 05)))
    self.assertTrue(hotterwire.ContainsWeekend(
        datetime.date(2014, 04, 06),
        datetime.date(2014, 04, 07)))
    self.assertFalse(hotterwire.ContainsWeekend(
        datetime.date(2014, 04, 07),
        datetime.date(2014, 04, 10)))
    self.assertTrue(hotterwire.ContainsWeekend(
        datetime.date(2014, 04, 07),
        datetime.date(2014, 04, 17)))
    self.assertTrue(hotterwire.ContainsWeekend(
        datetime.date(2014, 04, 07),
        datetime.date(2014, 04, 27)))


if __name__ == "__main__":
    unittest.main()