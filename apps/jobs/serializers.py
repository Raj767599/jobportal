from rest_framework import serializers
from .models import JobPost, Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class JobPostSerializer(serializers.ModelSerializer):
    skill_tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skill.objects.all(), required=False
    )

    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ['employer', 'created_at']

    def create(self, validated_data):
        skill_tags = validated_data.pop('skill_tags', [])
        job = JobPost.objects.create(**validated_data)
        job.skill_tags.set(skill_tags)
        return job

    def update(self, instance, validated_data):
        skill_tags = validated_data.pop('skill_tags', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if skill_tags is not None:
            instance.skill_tags.set(skill_tags)
        return instance
