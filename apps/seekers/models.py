from django.db import models
from apps.common.models import Skill
from apps.users.models import User
from apps.common.models import Skill

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255, db_index=True)
    experience = models.CharField(max_length=100)
    education = models.CharField(max_length=255)
    skills = models.TextField(blank=True)  # legacy field, keep for now
    skill_tags = models.ManyToManyField(Skill, blank=True, related_name='seekers') # NEW
    resume = models.FileField(upload_to='resumes/')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.full_name} ({self.user.email})"