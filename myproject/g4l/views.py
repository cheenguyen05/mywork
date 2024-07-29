from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm, UserUpdateForm, ProfileUpdateForm, ScheduleForm, TodoListForm

from django.contrib.auth.decorators import login_required

from .models import Profile, Schedule, TodoList

from django.db.models import Q

# - Authentication models and functions
 
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

#
# HOMEPAGE
#
def homepage(request):

    return render(request, 'g4l/index.html')


#
# REGISTER
#

def register(request):

    form =  CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("mylogin")
 

    context = {'registerform':form}

    return render(request, 'g4l/register.html', context=context)

#
# MYLOGIN
#

def mylogin(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")


    context = {'loginform':form}

    return render(request, 'g4l/mylogin.html', context=context)


#
# LOGOUT
#
def user_logout(request):

    auth.logout(request)

    return redirect("")


#
# DASHBOARD 
#
@login_required(login_url="mylogin")
def dashboard(request):

    return render(request, 'g4l/dashboard.html')


#
# PROFILE
#
@login_required(login_url="mylogin")
def profile(request, user_id=None):
    # Nếu user_id không được cung cấp, sử dụng user đã đăng nhập
    if user_id is None:
        user = request.user
    else:
        user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, instance=user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile', user_id=user.id)  # Redirect tới profile của người dùng

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_id': user.id,
    }

    return render(request, 'g4l/profile.html', context=context)


#
# SEARCH
#
def search_view(request):
    query = request.GET.get('query', '').strip()
    filter_type = request.GET.get('filter_type', '')

    if not query:
        users = User.objects.none()
    else:
        users = User.objects.all()

        if filter_type and query:
            if filter_type == 'username':
                users = users.filter(username__icontains=query)
            elif filter_type == 'school':
                user_profiles = Profile.objects.filter(school__icontains=query)
                users = users.filter(id__in=user_profiles.values('user_id'))
            elif filter_type == 'age':
                user_profiles = Profile.objects.filter(age=query)
                users = users.filter(id__in=user_profiles.values('user_id'))
        else:  # Tìm kiếm mọi thứ khi không có filter_type
            user_profiles = Profile.objects.filter(
                Q(user__username__icontains=query) |
                Q(school__icontains=query) |
                Q(age__icontains=query)
            )
            users = users.filter(id__in=user_profiles.values('user_id'))

    context = {
        'users': users,
        'query': query,
        'filter_type': filter_type
    }

    return render(request, 'g4l/search.html', context=context)



#
# CREATE SCHEDULE
#
@login_required
def schedule_list(request):
    schedules = Schedule.objects.filter(user=request.user)
    return render(request, 'g4l/schedule_list.html', {'schedules': schedules})
#@login_required
#def schedule_detail(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    return render(request, 'g4l/schedule_detail.html', {'schedule': schedule})

@login_required
def schedule_create(request):
    form = ScheduleForm()

    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            return redirect('schedule_list')

    context = {'scheduleform':form}

    return render(request, 'g4l/schedule_form.html', context=context)

def schedule_delete(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        schedule.delete()
        return redirect('schedule_list')
    return render(request, 'g4l/schedule_confirm_delete.html', {'schedule': schedule})

#
# TODOLIST
#
@login_required
def create_todolist(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id, user=request.user)

    if request.method == "POST":
        form = TodoListForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.schedule = schedule
            todo.save()
            return redirect('schedule_list')
    else:
        form = TodoListForm()

    context = {
        'createform':form,
        'schedule': schedule
    }

    return render(request, 'g4l/todolist_form.html', context=context)


def todolist_delete(request, pk):
    if request.method == "POST":
        todo = get_object_or_404(TodoList, pk=pk)
        todo.delete()
        return redirect('todolist')
    return render(request, 'g4l/todo_confirm_delete.html', {'todo': todo})

