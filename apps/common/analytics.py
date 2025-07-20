from rest_framework.views import APIView
from rest_framework.response import Response
from apps.common.models import Skill

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Skill

class SeekersPerSkillView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        data = []
        for skill in skills:
            seeker_count = skill.seekers.count()
            data.append({"skill": skill.name, "seeker_count": seeker_count})
        data = sorted(data, key=lambda x: x["seeker_count"], reverse=True)
        return Response(data)

class JobsPerSkillView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        data = []
        for skill in skills:
            job_count = skill.job_posts.count()
            data.append({"skill": skill.name, "job_count": job_count})
        data = sorted(data, key=lambda x: x["job_count"], reverse=True)
        return Response(data)

class SkillMatchAnalyticsView(APIView):
    def get(self, request):
        skills = Skill.objects.all()
        data = []
        for skill in skills:
            seeker_count = skill.seekers.count()
            job_count = skill.job_posts.count()
            matches = min(seeker_count, job_count)
            data.append({
                "skill": skill.name,
                "seekers": seeker_count,
                "jobs": job_count,
                "matches": matches
            })
        data = sorted(data, key=lambda x: x["matches"], reverse=True)
        return Response(data)
