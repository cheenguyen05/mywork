from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username


class SearchInfo(models.Model):
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name
