from rest_framework.test import APITestCase
from django.urls import reverse
from apps.users.models import User
from apps.jobs.models import JobPost
from apps.common.models import Skill

class JobPostTest(APITestCase):
    def setUp(self):
        # Create employer user
        self.employer = User.objects.create_user(
            username="hr2", email="hr2@example.com", password="hrpass2", role="employer"
        )
        self.client.force_authenticate(user=self.employer)

        # Create some skills
        self.skill_python = Skill.objects.create(name="Python")
        self.skill_django = Skill.objects.create(name="Django")

    def test_create_job_post(self):
        url = reverse('employer-jobs')  # Make sure this is your jobs create/list route name
        data = {
            "title": "Backend Developer",
            "description": "REST API work",
            "location": "Remote",
            "salary": "10-20 LPA",
            "experience_required": "3+ years",
            "skills_required": "Python, Django",
            "skill_tags": [self.skill_python.id, self.skill_django.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(JobPost.objects.filter(title="Backend Developer").exists())



    def test_employer_can_update_own_job(self):
        job = JobPost.objects.create(
            employer=self.employer,
            title="Old Job",
            description="Old",
            location="Delhi",
            salary="8 LPA",
            experience_required="2 years",
            skills_required="Python",
        )
        job.skill_tags.add(self.skill_python)
        url = reverse('job-detail', kwargs={"pk": job.pk})
        data = {
            "title": "Updated Job",
            "description": "Updated",
            "location": "Delhi",
            "salary": "9 LPA",
            "experience_required": "3 years",
            "skills_required": "Python, Django",
            "skill_tags": [self.skill_python.id, self.skill_django.id]
        }


        response = self.client.put(url, data, format='json')
        print("UPDATE RESPONSE:", response.status_code, response.json())
        self.assertEqual(response.status_code, 200)
        job.refresh_from_db()
        self.assertEqual(job.title, "Updated Job")


