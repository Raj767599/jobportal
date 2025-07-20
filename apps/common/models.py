from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)


    def __str__(self):
        return self.name
