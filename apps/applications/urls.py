from django.urls import path
from .views import ApplyToJobView, MyApplicationsView, ApplicantsForJobView, DummyApplicationView, update_application_status

urlpatterns = [
    path('apply/<int:job_id>/', ApplyToJobView.as_view(), name='apply-to-job'),
    path('mine/', MyApplicationsView.as_view(), name='my-applications'),
    path('for-job/<int:job_id>/', ApplicantsForJobView.as_view(), name='applicants-for-job'),
    path('dummy/', DummyApplicationView.as_view(), name='applications-dummy'),
    path('update-status/<int:pk>/', update_application_status, name='update-application-status'),
]
