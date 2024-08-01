from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm, UserUpdateForm, ProfileUpdateForm, ScheduleForm, TodoListForm

from django.contrib.auth.decorators import login_required

from .models import Profile, Schedule, TodoList

from django.db.models import Q
from django.utils import timezone

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
    # Nếu không có ID trong URL, sử dụng ID của người dùng đã đăng nhập
    if user_id is None:
        user_id = request.user.id

    # Lấy đối tượng người dùng hoặc trả về lỗi 404 nếu không tìm thấy
    user = get_object_or_404(User, id=user_id)

    # Nếu người dùng không phải là người đang xem profile, chỉ cho phép xem thông tin
    if user_id != request.user.id:
        u_form = None
        p_form = None
    else:
        # Chỉ cho phép cập nhật thông tin nếu xem profile của chính mình
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=user)
            p_form = ProfileUpdateForm(request.POST, instance=user.profile)

            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                return redirect('profile', user_id=user.id)
        else:
            u_form = UserUpdateForm(instance=user)
            p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        'is_self': user_id == request.user.id,  # Xác định xem đây có phải là profile của chính người dùng không
        'logged_in_user': request.user  # Đảm bảo rằng tên người dùng đăng nhập luôn được truyền
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
@login_required(login_url="mylogin")
def schedule_list(request):
    schedules = Schedule.objects.filter(user=request.user)
    return render(request, 'g4l/schedule_list.html', {'schedules': schedules})

@login_required(login_url="mylogin")
def schedule_detail(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    return render(request, 'g4l/schedule_detail.html', {'schedule': schedule})

@login_required(login_url="mylogin")
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
    if request.method == 'POST':
        schedule.delete()
        return redirect('schedule_list')
    return redirect('schedule_list')

def schedule_update(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('schedule_list')
    return redirect('schedule_list')

#
# TODOLIST
#
@login_required(login_url="mylogin")
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

    sorted_todos = schedule.get_sorted_todos()

    context = {
        'createform':form,
        'schedule': schedule,
        'sorted_todos': sorted_todos
    }

    return render(request, 'g4l/todolist_form.html', context=context)

@login_required(login_url="mylogin")
def todolist_delete(request, pk):
    if request.method == "POST":
        todo = get_object_or_404(TodoList, pk=pk)
        todo.delete()
        return redirect('todolist')
    return render(request, 'g4l/todo_confirm_delete.html', {'todo': todo})

@login_required(login_url="mylogin")
def mark_todolist_complete(request):
    if request.method == "POST":
        todo_id = request.POST.get("todo_id")
        todo = get_object_or_404(TodoList, id=todo_id, user=request.user)
        todo.completed = not todo.completed
        if todo.completed:
            todo.completed_at = timezone.now()
        else:
            todo.completed_at = None
        todo.save()
    return redirect('schedule_list')
