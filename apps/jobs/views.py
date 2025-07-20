from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.seekers.models import JobSeekerProfile
from .models import JobPost
from .serializers import JobPostSerializer
from .permissions import IsEmployer

# Create & list jobs for employer
class JobPostCreateListView(generics.ListCreateAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return JobPost.objects.filter(employer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

# Public job list (with search/filter support)
class PublicJobListView(generics.ListAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'is_active']
    search_fields = ['title', 'location', 'skills_required']

    def get_queryset(self):
        # This is the optimized queryset
        return JobPost.objects.filter(is_active=True).select_related('employer').prefetch_related('skill_tags')


# Employer can view, update, or delete their jobs
class JobPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        # --- This makes swagger schema generation work! ---
        if getattr(self, 'swagger_fake_view', False):
            return JobPost.objects.none()
        # --- End swagger fix ---
        return JobPost.objects.filter(employer=self.request.user)

# "Recommended jobs for you" for seekers
class RecommendedJobsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seeker = JobSeekerProfile.objects.get(user=request.user)
        seeker_skills = seeker.skill_tags.all()
        location = seeker.location  # Or use: location = request.query_params.get("location")
        jobs = JobPost.objects.filter(
            skill_tags__in=seeker_skills,
            is_active=True,
            location__icontains=location
        ).distinct()
        serializer = JobPostSerializer(jobs, many=True)
        return Response(serializer.data)

# Dummy test
class DummyJobView(APIView):
    def get(self, request):
        return Response({"message": "Job API working"})
