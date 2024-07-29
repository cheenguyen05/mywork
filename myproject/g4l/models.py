from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titles = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.titles

class TodoList(models.Model):
    JOB_TYPE_CHOICES = [
        ('daily', 'Hàng ngày'),
        ('weekly', 'Ngày trong tuần'),
        ('monthly', 'Ngày trong tháng'),
        ('one_time', 'Làm trong ngày'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    schedule = models.ForeignKey(Schedule, related_name='todolist', on_delete=models.CASCADE)
    titles = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, default='one_time')

    def __str__(self):
        return self.titles