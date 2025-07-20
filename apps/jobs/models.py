from django.db import models
# ✅ CORRECT
from apps.users.models import User


from django.db import models
from apps.users.models import User
from apps.common.models import Skill



class JobPost(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, db_index=True)
    salary = models.CharField(max_length=100)
    experience_required = models.CharField(max_length=100)
    skills_required = models.TextField(blank=True)
    skill_tags = models.ManyToManyField(Skill, blank=True, related_name='job_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.employer.username}"
