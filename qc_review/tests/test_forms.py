from django.test import TestCase

from qc_review.forms import QCRunSelectForm

from .utils import create_qcrun, create_suite


class TestForms(TestCase):
    def setUp(self):
        self.run1 = create_qcrun(123, 'ADAMSDEV')
        self.suite1 = create_suite(self.run1, 'adamspy', 10, 5, 1)
        self.run2 = create_qcrun(456, 'ADAMSDEV2')
        self.suite2 = create_suite(self.run2, 'adamspy', 10, 5, 1)

    def test_qcrun_select_valid_data(self):
        form = QCRunSelectForm(data={
            'codeline': 'ADAMSDEV',
            'changelist': 123
        })
        self.assertTrue(form.is_valid())

    def test_qcrun_select_no_data(self):
        form = QCRunSelectForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_qcrun_select_invalid_codeline(self):
        form = QCRunSelectForm(data={
            'codeline': 'XXX',
            'changelist': 123
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_qcrun_select_invalid_changelist(self):
        form = QCRunSelectForm(data={
            'codeline': 'ADAMSDEV2',
            'changelist': 0
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
