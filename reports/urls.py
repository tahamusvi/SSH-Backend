from django.urls import path
from .views import all_reports, ReportCreateView

urlpatterns = [
    path('', all_reports.as_view(), name='report-list'),
    path('create/', ReportCreateView.as_view(), name='report-create'),
]
