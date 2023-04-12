from django.urls import path
from .views import TriggerReportView,GetReportView

urlpatterns = [
    path('trigger_report', TriggerReportView.as_view()),
    path('get_report/<uuid:report_id>', GetReportView.as_view()),
]