from django.urls import path
from .analytics import SeekersPerSkillView, JobsPerSkillView, SkillMatchAnalyticsView

urlpatterns = [
    path('analytics/seekers-per-skill/', SeekersPerSkillView.as_view()),
    path('analytics/jobs-per-skill/', JobsPerSkillView.as_view()),
    path('analytics/skill-matches/', SkillMatchAnalyticsView.as_view()),
]
