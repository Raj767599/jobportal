from rest_framework.test import APITestCase
from django.urls import reverse
from apps.users.models import User
from apps.jobs.models import JobPost
from apps.applications.models import Application
from apps.common.models import Skill
from django.core.files.uploadedfile import SimpleUploadedFile

class ApplicationTest(APITestCase):
    def setUp(self):
        self.employer = User.objects.create_user(username="emp", email="emp@example.com", password="emp123", role="employer")
        self.seeker = User.objects.create_user(username="seeker", email="seeker@app.com", password="seek123", role="job_seeker")
        self.skill = Skill.objects.create(name="Python")
        self.job = JobPost.objects.create(
            title="Python Dev",
            employer=self.employer,
            location="Delhi",
            salary="8 LPA",
            experience_required="2 years",
            skills_required="Python"
        )
        self.job.skill_tags.add(self.skill)
        self.client.force_authenticate(user=self.seeker)
        self.dummy_resume = SimpleUploadedFile("resume.pdf", b"my dummy resume", content_type="application/pdf")

    def test_apply_to_job(self):
        url = reverse('apply-to-job', kwargs={"job_id": self.job.id})
        data = {
            "resume": self.dummy_resume,
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Application.objects.filter(job=self.job, applicant=self.seeker).exists())

    def test_cannot_apply_twice(self):
        # First application
        Application.objects.create(job=self.job, applicant=self.seeker, resume=self.dummy_resume)
        url = reverse('apply-to-job', kwargs={"job_id": self.job.id})
        # New dummy file for the second try
        dummy_resume2 = SimpleUploadedFile("resume2.pdf", b"new content", content_type="application/pdf")
        data = {
            "resume": dummy_resume2,
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertIn('already applied', response.json()['detail'].lower())
