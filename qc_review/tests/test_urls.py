from django.test import SimpleTestCase
from django.urls import reverse, resolve
from qc_review.views import (
    SummaryView, 
    SuiteDetailView,
    SuiteDetailData,
    QCRunDataView
)


class TestUrls(SimpleTestCase):
    def test_index_resolves(self):
        url = reverse('qc_review:index')
        self.assertEqual(resolve(url).func.view_class, SummaryView)
    
    def test_suite_detail_resolves(self):
        url = reverse('qc_review:suite-detail', args=[0])
        self.assertEqual(resolve(url).func.view_class, SuiteDetailView)
    
    def test_suite_detail_data_resolves(self):
        url = reverse('qc_review:suite-detail-data')
        self.assertEqual(resolve(url).func.view_class, SuiteDetailData)
    
    def test_qc_run_data_resolves(self):
        url = reverse('qc_review:qcrun-data')
        self.assertEqual(resolve(url).func.view_class, QCRunDataView)
