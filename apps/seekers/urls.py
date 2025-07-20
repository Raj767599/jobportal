from django.urls import path
from .views import  JobSeekerProfileCreateView, JobSeekerProfileDetailView, RecommendedSeekersForJobView, ResumeParserAndProfileAutoFillView, SearchSeekerBySkillView
from .views import ResumeParserView

urlpatterns = [
 path('profile/', JobSeekerProfileCreateView.as_view(), name='seeker-profile'),
    path('profile/<int:pk>/', JobSeekerProfileDetailView.as_view(), name='seeker-profile-detail'),
    path('parse-resume/', ResumeParserView.as_view(), name='parse-resume'),
    path('parse-and-autofill/', ResumeParserAndProfileAutoFillView.as_view(), name='parse-autofill'),
    path('search-by-skill/', SearchSeekerBySkillView.as_view(), name='search-by-skill'),
    path('recommended/<int:job_id>/', RecommendedSeekersForJobView.as_view(), name='recommended-seekers'),
]
