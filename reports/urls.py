from django.urls import path
from .views import ReportView, DownloadReportView

urlpatterns = [
    path('report/', ReportView.as_view(), name='report'),
    path('download_report/', DownloadReportView.as_view(), name='download_report'),
]