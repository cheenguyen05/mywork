from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

    def get_sorted_todos(self):
        return self.todolist.all().order_by('start_time')

class TodoList(models.Model):
    JOB_TYPE_CHOICES = [
        ('Daily', 'Hàng ngày'),
        ('Weekly', 'Ngày trong tuần'),
        ('Monthly', 'Ngày trong tháng'),
        ('One_time', 'Làm trong ngày'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    schedule = models.ForeignKey(Schedule, related_name='todolist', on_delete=models.CASCADE)
    titles = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, default='Daily')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titles