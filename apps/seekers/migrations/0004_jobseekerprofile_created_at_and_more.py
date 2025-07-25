# Generated by Django 5.2.4 on 2025-07-19 22:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '__first__'),
        ('seekers', '0003_alter_jobseekerprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekerprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='skill_tags',
            field=models.ManyToManyField(blank=True, related_name='seekers', to='common.skill'),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='location',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='skills',
            field=models.TextField(blank=True),
        ),
    ]
