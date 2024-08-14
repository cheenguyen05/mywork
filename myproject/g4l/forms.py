
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django.forms.widgets import PasswordInput, TextInput, NumberInput

from django import forms
 
from .models import Profile, Schedule, TodoList, Task


# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):
    school = forms.CharField(required=False)
    age = forms.IntegerField(required=False)

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile(user=user, school=self.cleaned_data['school'], age=self.cleaned_data['age'])
            profile.save()
        return user


# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
# - Update profile
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email'] 

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'age']
# - Make schedule
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['titles', 'start_date', 'end_date', 'description']

class TodoListForm(forms.ModelForm):
    JOB_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('one_time', 'One-time'),
    ]

    job_type = forms.ChoiceField(choices=JOB_TYPE_CHOICES, required=True)

    days_of_week = forms.CharField(
        required=False,
        label='Ngày trong tuần (nhập số, ví dụ: 2,3,4)',
        help_text='Chọn tối đa 5 ngày trong tuần, từ 2 (Thứ 2) đến 8 (Chủ Nhật)'
    )
    
    days_of_month = forms.CharField(
        required=False,
        label='Ngày trong tháng (nhập số, ví dụ: 1,15,30)',
        help_text='Chọn tối đa 5 ngày trong tháng, từ 1 đến 31'
    )
    
    specific_date = forms.DateField(required=False, label='Ngày cụ thể')

    class Meta:
        model = TodoList
        fields = ['titles','start_time', 'end_time', 'job_type', 'days_of_week', 'days_of_month', 'specific_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['days_of_week'].widget.attrs.update({'class': 'form-control'})
        self.fields['days_of_month'].widget.attrs.update({'class': 'form-control'})
        self.fields['specific_date'].widget.attrs.update({'class': 'form-control'})

    def clean_days_of_week(self):
        days_of_week = self.cleaned_data.get('days_of_week')
        if days_of_week:
            days = list(map(int, days_of_week.split(',')))
            if any(day < 2 or day > 8 for day in days):
                raise forms.ValidationError("Ngày trong tuần phải nằm trong khoảng từ 2 đến 8")
            if len(days) > 5:
                raise forms.ValidationError("Chỉ được chọn tối đa 5 ngày trong tuần")
        return days_of_week

    def clean_days_of_month(self):
        days_of_month = self.cleaned_data.get('days_of_month')
        if days_of_month:
            days = list(map(int, days_of_month.split(',')))
            if any(day < 1 or day > 31 for day in days):
                raise forms.ValidationError("Ngày trong tháng phải nằm trong khoảng từ 1 đến 31")
            if len(days) > 5:
                raise forms.ValidationError("Chỉ được chọn tối đa 5 ngày trong tháng")
        return days_of_month
    
class TodoListUpdateForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['titles', 'start_time', 'end_time']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['titles', 'start_time', 'end_time']