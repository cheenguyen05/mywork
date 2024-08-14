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
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('one_time', 'One-time'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    schedule = models.ForeignKey(Schedule, related_name='todolist', on_delete=models.CASCADE)
    titles = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, default='Daily')
    days_of_week = models.CharField(max_length=100, blank=True, null=True)  # Lưu các ngày trong tuần
    days_of_month = models.CharField(max_length=100, blank=True, null=True)  # Lưu các ngày trong tháng
    specific_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)


    def set_days_of_week(self, days):
        self.days_of_week = ','.join(map(str, days))

    def get_days_of_week(self):
        return self.days_of_week.split(',') if self.days_of_week else []

    def set_days_of_month(self, days):
        self.days_of_month = ','.join(map(str, days))

    def get_days_of_month(self):
        return self.days_of_month.split(',') if self.days_of_month else []

    def get_sorted_task(self):
        return self.task.all().order_by('start_time')

    def status_color(self):
        total_tasks = self.task.count()
        completed_tasks = self.task.filter(completed=True).count()

        if completed_tasks == 0:
            return 'red'
        elif completed_tasks == total_tasks:
            return 'green'
        else:
            return 'yellow'

    def __str__(self):
        return self.titles

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    todo = models.ForeignKey(TodoList, related_name='task', on_delete=models.CASCADE)
    titles = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.titles