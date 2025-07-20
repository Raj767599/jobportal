from django.urls import path
from .views import JobPostCreateListView, PublicJobListView, DummyJobView, JobPostDetailView, RecommendedJobsView

urlpatterns = [
    path('', JobPostCreateListView.as_view(), name='employer-jobs'),
    path('all/', PublicJobListView.as_view(), name='public-jobs'),
    path('<int:pk>/', JobPostDetailView.as_view(), name='job-detail'),
    path('recommended/', RecommendedJobsView.as_view(), name='recommended-jobs'),
    path('test/', DummyJobView.as_view(), name='jobs-test'),
]