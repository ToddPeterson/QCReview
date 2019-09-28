import datetime

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .utils import create_qcrun, create_suite


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

        self.run1 = create_qcrun(123, 'ADAMSDEV')
        self.suite1 = create_suite(self.run1, 'adamspy', 10, 5, 1)
        self.run2 = create_qcrun(456, 'ADAMSDEV2')
        self.suite2 = create_suite(self.run2, 'adamspy', 10, 5, 1)

        self.index_url = reverse('qc_review:index')
        self.suite_detail_url = reverse('qc_review:suite-detail', args=[self.suite2.id])

    def test_summary_GET(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'qc_review/summary.html')

    def test_suite_detail_GET(self):
        response = self.client.get(self.suite_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'qc_review/suiterun_detail.html')

    def test_summary_POST_with_existing_run(self):
        response = self.client.post(self.index_url, {
            'codeline': self.run1.codeline,
            'changelist': self.run1.cl
        })
        self.assertEquals(response.status_code, 200)

    def test_summary_POST_404s_with_nonexistent_run(self):
        response = self.client.post(self.index_url, {
            'codeline': 'ADAMSDEV',
            'changelist': 456
        })
        self.assertEquals(response.status_code, 404)

    def test_summary_POST_redirects_index_with_invalid_form(self):
        response = self.client.post(self.index_url, {
            'codeline': 'XXX',
            'changelist': 0
        })
        self.assertEquals(response.status_code, 302)
        self.assertEqual(response.url, reverse('qc_review:index'))
