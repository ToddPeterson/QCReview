import datetime

from django.test import TestCase
from django.utils import timezone

from .utils import create_qcrun, create_suite


class TestQCRun(TestCase):
    def setUp(self):
        self.run1 = create_qcrun(123, 'ADAMSDEV')
        self.suite1 = create_suite(self.run1, 'adamspy', 10, 5, 1)
        self.run2 = create_qcrun(456, 'ADAMSDEV2')
        self.suite2 = create_suite(self.run2, 'adamspy', 10, 5, 1)

    def test_run_has_suite(self):
        self.assertTrue(self.run1.has_suite('adamspy'))
        self.assertFalse(self.run1.has_suite('aview'))


class TestSuiteRun(TestCase):
    def setUp(self):
        self.run1 = create_qcrun(123, 'ADAMSDEV')
        self.suite1 = create_suite(self.run1, 'adamspy', 10, 5, 1)
        self.run2 = create_qcrun(456, 'ADAMSDEV2')
        self.suite2 = create_suite(self.run2, 'adamspy', 10, 5, 1)
    
    def test_elapsed_time(self):
        time1 = timezone.now()
        delta = datetime.timedelta(minutes=25)
        time2 = time1 + delta
        suite = create_suite(self.run1, 'elapsed', 0, 0, 0, start=time1, end=time2)
        self.assertEqual(suite.elapsed_time, delta)

