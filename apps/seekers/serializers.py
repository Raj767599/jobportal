from rest_framework import serializers

from apps.seekers.models import JobSeekerProfile

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    def validate_resume(self, value):
        max_size = 5 * 1024 * 1024  # 5MB
        allowed_extensions = ['pdf', 'doc', 'docx']
        ext = value.name.split('.')[-1].lower()

        if value.size > max_size:
            raise serializers.ValidationError("Resume file too large (max 5MB).")
        if ext not in allowed_extensions:
            raise serializers.ValidationError("Resume file type not allowed.")
        return value

    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ['user']
        