from rest_framework.test import APITestCase
from django.urls import reverse
from apps.users.models import User
from apps.common.models import Skill
from apps.jobs.models import JobPost

class JobPostTest(APITestCase):
    def setUp(self):
        self.employer = User.objects.create_user(username="emp", email="emp@example.com", password="emp123", role="employer")
        self.other_employer = User.objects.create_user(username="emp2", email="emp2@example.com", password="emp123", role="employer")
        self.skill = Skill.objects.create(name="Django")
        self.client.force_authenticate(user=self.employer)

    def test_create_job_post(self):
        url = reverse('employer-jobs')
        data = {
            "title": "Backend Developer",
            "description": "REST API work",
            "location": "Remote",
            "salary": "10-20 LPA",
            "experience_required": "3+ years",
            "skills_required": "Python, Django",
            "skill_tags": [self.skill.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], "Backend Developer")
        self.assertIn(self.skill.id, response.data['skill_tags'])

    def test_employer_can_update_own_job(self):
        job = JobPost.objects.create(
            title="Backend Developer",
            description="REST API work",
            location="Remote",
            salary="10-20 LPA",
            experience_required="3+ years",
            skills_required="Python, Django",
            employer=self.employer
        )
        job.skill_tags.add(self.skill)
        url = reverse('job-detail', kwargs={'pk': job.id})
        data = {
            "title": "Updated Job",
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "experience_required": job.experience_required,
            "skills_required": job.skills_required,
            "skill_tags": [self.skill.id]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        job.refresh_from_db()
        self.assertEqual(job.title, "Updated Job")

    def test_employer_cannot_update_others_job(self):
        job = JobPost.objects.create(
            title="Other Employer Job",
            description="desc",
            location="NY",
            salary="5 LPA",
            experience_required="2 years",
            skills_required="Django",
            employer=self.other_employer
        )
        url = reverse('job-detail', kwargs={'pk': job.id})
        data = {
            "title": "Hacked Title",
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "experience_required": job.experience_required,
            "skills_required": job.skills_required,
            "skill_tags": []
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 404)


    def test_public_job_list(self):
        JobPost.objects.create(
            title="Public Job 1",
            description="desc",
            location="NY",
            salary="5 LPA",
            experience_required="2 years",
            skills_required="Django",
            employer=self.employer,
            is_active=True
        )
        JobPost.objects.create(
            title="Inactive Job",
            description="desc",
            location="LA",
            salary="7 LPA",
            experience_required="3 years",
            skills_required="Python",
            employer=self.employer,
            is_active=False
        )
        self.client.logout()
        url = reverse('public-jobs')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_jobs_by_title(self):
        JobPost.objects.create(
            title="Django Developer",
            description="desc",
            location="NY",
            salary="5 LPA",
            experience_required="2 years",
            skills_required="Django",
            employer=self.employer,
            is_active=True
        )
        JobPost.objects.create(
            title="React Developer",
            description="desc",
            location="LA",
            salary="7 LPA",
            experience_required="3 years",
            skills_required="React",
            employer=self.employer,
            is_active=True
        )
        self.client.logout()
        url = reverse('public-jobs') + '?search=Django'
        response = self.client.get(url)
        print("SEARCH RESPONSE:", response.status_code, response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

