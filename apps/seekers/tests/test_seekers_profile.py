from rest_framework.test import APITestCase
from django.urls import reverse
from apps.users.models import User
from apps.seekers.models import JobSeekerProfile
from apps.common.models import Skill
from django.core.files.uploadedfile import SimpleUploadedFile
class SeekerProfileTest(APITestCase):
    def setUp(self):
        # Create job seeker user
        self.seeker_user = User.objects.create_user(
            username="seekerx", email="seekerx@example.com", password="seekpass", role="job_seeker"
        )
        self.skill_python = Skill.objects.create(name="Python")
        self.skill_js = Skill.objects.create(name="JavaScript")
        self.client.force_authenticate(user=self.seeker_user)


    def test_create_profile(self):
        url = reverse('seeker-profile')
        data = {
            "full_name": "Seeker X",
            "location": "Noida",
            "experience": "1 year",
            "education": "BCA",
            "skills": "Python, JavaScript",
            "skill_tags": [self.skill_python.id, self.skill_js.id],
            "phone": "9876543210",
            "resume": SimpleUploadedFile("resume.pdf", b"dummy data", content_type="application/pdf")
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(JobSeekerProfile.objects.filter(full_name="Seeker X").exists())


    def test_update_profile(self):
        profile = JobSeekerProfile.objects.create(
            user=self.seeker_user,
            full_name="Old Name",
            location="Delhi",
            experience="0 year",
            education="Diploma",
            skills="Python",
            phone="1112223333",
            resume=SimpleUploadedFile("resume.pdf", b"old data", content_type="application/pdf")
        )
        profile.skill_tags.add(self.skill_python)
        url = reverse('seeker-profile-detail', kwargs={"pk": profile.pk})
        data = {
            "full_name": "Updated Name",
            "location": "Bangalore",
            "experience": "2 years",
            "education": "BTech",
            "skills": "Python, JavaScript",
            "skill_tags": [self.skill_python.id, self.skill_js.id],
            "phone": "9998887777",
            "resume": SimpleUploadedFile("resume.pdf", b"new data", content_type="application/pdf")
        }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, 200)
        profile.refresh_from_db()
        self.assertEqual(profile.full_name, "Updated Name")
        self.assertEqual(profile.location, "Bangalore")

