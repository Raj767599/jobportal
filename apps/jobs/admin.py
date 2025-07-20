from django.contrib import admin
from .models import JobPost

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'employer', 'is_active', 'created_at')
    list_filter = ('is_active', 'location')
