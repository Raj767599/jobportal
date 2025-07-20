from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.jobs.models import JobPost
from apps.jobs.serializers import JobPostSerializer
from .models import JobSeekerProfile
from .serializers import JobSeekerProfileSerializer
from .permissions import IsJobSeeker
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.common.permissions import IsEmployer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .permissions import IsJobSeeker
from utils.resume_parser import extract_resume_data

from rest_framework import viewsets
from .models import JobSeekerProfile
from .serializers import JobSeekerProfileSerializer
from rest_framework.permissions import IsAuthenticated

class JobSeekerProfileViewSet(viewsets.ModelViewSet):
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

class JobSeekerProfileCreateView(CreateAPIView):
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JobSeekerProfileDetailView(RetrieveUpdateAPIView):
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    permission_classes = [IsAuthenticated]


class ResumeParserView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def post(self, request):
        file = request.FILES.get('resume')
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        with open('temp_resume.pdf', 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        data = extract_resume_data('temp_resume.pdf')
        return Response(data)
    

class ResumeParserAndProfileAutoFillView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def post(self, request):
        file = request.FILES.get('resume')
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        with open('temp_resume.pdf', 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        parsed = extract_resume_data('temp_resume.pdf')
        seeker_profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)
        
        # Auto-fill only if fields are empty
        if not seeker_profile.full_name and parsed.get("name"):
            seeker_profile.full_name = parsed["name"]
        if not seeker_profile.skills and parsed.get("skills"):
            seeker_profile.skills = parsed["skills"]
        seeker_profile.resume = file  # Save the actual file

        # ⬇️ **Add this block here for skill tagging** ⬇️
        skill_names = [s.strip() for s in parsed.get("skills", "").split(",") if s.strip()]
        skill_objs = []
        from .models import Skill

        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            skill_objs.append(skill)
        seeker_profile.save()  # Save first before setting M2M
        seeker_profile.skill_tags.set(skill_objs)  # Update ManyToMany field

        return Response({
            "parsed_data": parsed,
            "profile_auto_filled": True,
            "profile": {
                "full_name": seeker_profile.full_name,
                "skills": seeker_profile.skills
            }
        })
  
        

class SearchSeekerBySkillView(generics.ListAPIView):
    serializer_class = JobSeekerProfileSerializer

    def get_queryset(self):
        skill = self.request.query_params.get('skill')
        if skill:
            return JobSeekerProfile.objects.filter(skill_tags__name__icontains=skill)
        return JobSeekerProfile.objects.all()        
    

class RecommendedSeekersForJobView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request, job_id):
        try:
            job = JobPost.objects.get(pk=job_id, employer=request.user)
        except JobPost.DoesNotExist:
            return Response({"detail": "Job not found or unauthorized."}, status=404)
        
        job_skills = job.skill_tags.all()
        seekers = JobSeekerProfile.objects.filter(skill_tags__in=job_skills).distinct()
        serializer = JobSeekerProfileSerializer(seekers, many=True)
        return Response(serializer.data)   
    

