from rest_framework.test import APITestCase
from django.urls import reverse
from apps.users.models import User
from apps.jobs.models import JobPost
from apps.applications.models import Application
from apps.common.models import Skill
from django.core.files.uploadedfile import SimpleUploadedFile

class JobPortalEndToEndTest(APITestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="Python")

    def test_full_flow(self):
        # 1. Register employer
        employer = User.objects.create_user(username="emp", email="emp@site.com", password="emp123", role="employer")

        # 2. Employer creates job
        self.client.force_authenticate(user=employer)
        job_data = {
            "title": "Python Developer",
            "location": "Delhi",
            "salary": "8 LPA",
            "experience_required": "2 years",
            "skills_required": "Python",
            "description": "Good Python developer required."   # <--- Add this line
        }

        job_resp = self.client.post(reverse('employer-jobs'), job_data, format='json')

        print("RESPONSE:", job_resp.status_code, job_resp.data)
        self.assertEqual(job_resp.status_code, 201)
        job_id = job_resp.data['id']

        # 3. Register seeker
        seeker = User.objects.create_user(username="seek", email="seek@site.com", password="seek123", role="job_seeker")
        self.client.force_authenticate(user=seeker)

        # 4. Seeker fills profile
        profile_data = {
            "full_name": "Test Seeker",
            "location": "Delhi",
            "experience": "1 year",
            "education": "BCA",
            "skills": "Python",
            "phone": "9999999999",
            "resume": SimpleUploadedFile("resume.pdf", b"resume", content_type="application/pdf"),
            "skill_tags": [self.skill.id]
        }
        profile_resp = self.client.post(reverse('seeker-profile'), profile_data, format='multipart')
        self.assertEqual(profile_resp.status_code, 201)

        # 5. Seeker applies to job
        apply_url = reverse('apply-to-job', kwargs={'job_id': job_id})
        app_data = {
            "resume": SimpleUploadedFile("resume.pdf", b"resume", content_type="application/pdf"),
        }
        apply_resp = self.client.post(apply_url, app_data, format='multipart')
        self.assertEqual(apply_resp.status_code, 201)

        # 6. Employer shortlists
        self.client.force_authenticate(user=employer)
        app_obj = Application.objects.get(job_id=job_id, applicant=seeker)
        status_url = reverse('update-application-status', kwargs={"pk": app_obj.id})
        resp = self.client.patch(status_url, {"status": "shortlisted"}, format='json')
        self.assertEqual(resp.status_code, 200)

        # 7. Seeker checks application status
        self.client.force_authenticate(user=seeker)
        my_apps_url = reverse('my-applications')
        seeker_apps = self.client.get(my_apps_url)
        print("SEEKER APPLICATIONS:", seeker_apps.data)
        self.assertEqual(seeker_apps.status_code, 200)
        self.assertEqual(seeker_apps.data['results'][0]['status'], "shortlisted")

