from django.urls import path

from . import views

app_name = 'qc_review'
urlpatterns = [
    path('', views.SummaryView.as_view(), name='index'),
    path('suite/<int:pk>', views.SuiteDetailView.as_view(), name='suite-detail'),
    path('api/suite/data/', views.SuiteDetailData.as_view(), name='suite-detail-data'),
    path('api/runs/data/', views.QCRunDataView.as_view(), name='qcrun-data'),
]
