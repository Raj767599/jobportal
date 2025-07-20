from rest_framework.test import APITestCase
from django.urls import reverse
from apps.users.models import User
from apps.seekers.models import JobSeekerProfile
from apps.jobs.models import JobPost
from apps.common.models import Skill

class RecommendedSeekersAPITest(APITestCase):
    def setUp(self):
        # Create employer user and log in
        self.employer = User.objects.create_user(
            username="hr1", email="hr1@example.com", password="hrpass", role="employer"
        )
        self.client.login(email="hr1@example.com", password="hrpass")

        # Create some skills
        self.skill_python = Skill.objects.create(name="Python")
        self.skill_django = Skill.objects.create(name="Django")
        self.skill_js = Skill.objects.create(name="JavaScript")

        # Create a job post by employer with skill tags
        self.job = JobPost.objects.create(
            employer=self.employer,
            title="Python Developer",
            description="Build stuff",
            location="Remote",
            salary="100k",
            experience_required="2+ years",
            skills_required="Python, Django"
        )
        self.job.skill_tags.add(self.skill_python, self.skill_django)

        # Create seekers with matching and non-matching skills
        self.seeker1_user = User.objects.create_user(
            username="seeker1", email="seeker1@example.com", password="seekpass", role="job_seeker"
        )
        self.seeker1_profile = JobSeekerProfile.objects.create(
            user=self.seeker1_user, full_name="Alice", location="Remote", experience="2 years", education="BS", skills="Python"
        )
        self.seeker1_profile.skill_tags.add(self.skill_python)

        self.seeker2_user = User.objects.create_user(
            username="seeker2", email="seeker2@example.com", password="seekpass", role="job_seeker"
        )
        self.seeker2_profile = JobSeekerProfile.objects.create(
            user=self.seeker2_user, full_name="Bob", location="Remote", experience="2 years", education="BS", skills="JavaScript"
        )
        self.seeker2_profile.skill_tags.add(self.skill_js)

    def test_recommended_seekers_for_job(self):
        # Employer gets JWT token
        url = reverse('recommended-seekers', kwargs={'job_id': self.job.id})
        self.client.force_authenticate(user=self.employer)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Only seeker1 (with Python skill) should appear
        seekers = response.json()
        seeker_emails = [s['user'] for s in seekers]
        self.assertIn(self.seeker1_user.id, [s['user'] for s in seekers])
        self.assertNotIn(self.seeker2_user.id, [s['user'] for s in seekers])

    def test_unauthorized_employer_cannot_see(self):
        # Another employer tries to access this job's recommendations
        other_employer = User.objects.create_user(
            username="hr2", email="hr2@example.com", password="hr2pass", role="employer"
        )
        self.client.force_authenticate(user=other_employer)
        url = reverse('recommended-seekers', kwargs={'job_id': self.job.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
