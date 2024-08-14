from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm, UserUpdateForm, ProfileUpdateForm, ScheduleForm, TodoListForm, TodoListUpdateForm, TaskForm

from django.contrib.auth.decorators import login_required

from .models import Profile, Schedule, TodoList, Task

from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.urls import reverse

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
    # Lấy dữ liệu tìm kiếm từ query parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    specific_date = request.GET.get('specific_date')

    # Lọc lịch trình dựa trên người dùng
    schedules = Schedule.objects.filter(user=request.user).order_by('start_date')
    
    # Lọc lịch trình dựa trên ngày tháng tìm kiếm
    if start_date and end_date:
        schedules = schedules.filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
        )
    elif specific_date:
        schedules = schedules.filter(
            Q(start_date__lte=specific_date) & Q(end_date__gte=specific_date)
        )

    # Thiết lập Paginator
    p = Paginator(schedules, 5)
    page = request.GET.get('page')
    lists = p.get_page(page)
    nums = "a" * lists.paginator.num_pages

    context = {
        'schedules': schedules,
        'lists': lists,
        'nums': nums,
    }

    return render(request, 'g4l/schedule_list.html', context=context)



@login_required(login_url="mylogin")
def schedule_detail(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    todos = schedule.get_sorted_todos()

     #search query and filtering
    job_type = request.GET.get('job_type')
    day = request.GET.get('day')

    if job_type:
        todos = todos.filter(job_type=job_type)

        if job_type == 'weekly' and day:
            todos = todos.filter(days_of_week__icontains=day)
        elif job_type == 'monthly' and day:
            todos = todos.filter(days_of_month__icontains=day)
        elif job_type == 'one-time' and day:
            todos = todos.filter(specific_date=day)

    
    #hiển thị job_type của todolist
    for todo in todos:
        if todo.job_type == 'weekly':
            todo.days_info = todo.get_days_of_week()
        elif todo.job_type == 'monthly':
            todo.days_info = todo.get_days_of_month()
        elif todo.job_type == 'one_time':
            todo.days_info = [todo.specific_date]

    p = Paginator(todos, 5)
    page = request.GET.get('page')
    lists = p.get_page(page)
    nums = "a" * lists.paginator.num_pages

    context={
        'schedule':schedule,
        'todos':todos,
        'lists': lists,
        'nums': nums,
        'job_type': job_type,
        'day': day,
    }
    return render(request, 'g4l/schedule_detail.html', context=context)


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

@login_required(login_url="mylogin")
def schedule_delete(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        return redirect('schedule_list')
    return redirect('schedule_list')
    

@login_required(login_url="mylogin")
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
            # Set additional fields based on job_type
            job_type = form.cleaned_data['job_type']
            if job_type == 'daily':
                todo.days_of_week = None
                todo.days_of_month = None
                todo.specific_date = None
            elif job_type == 'weekly':
                days_of_week = form.cleaned_data.get('days_of_week')
                if days_of_week:
                    todo.set_days_of_week(days_of_week.split(','))
                todo.days_of_month = None
                todo.specific_date = None
            elif job_type == 'monthly':
                days_of_month = form.cleaned_data.get('days_of_month')
                if days_of_month:
                    todo.set_days_of_month(days_of_month.split(','))
                todo.days_of_week = None
                todo.specific_date = None
            elif job_type == 'one_time':
                todo.days_of_week = None
                todo.days_of_month = None
                todo.specific_date = form.cleaned_data.get('specific_date')

            todo.save()
            return redirect('schedule_detail', pk=schedule.id)
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
def todolist_detail(request, pk):
    todo = get_object_or_404(TodoList, pk=pk)
    tasks = todo.get_sorted_task()

    p = Paginator(tasks, 5)
    page = request.GET.get('page')
    lists = p.get_page(page)
    nums = "a" * lists.paginator.num_pages

    context = {
        'todo': todo,
        'tasks': tasks,
        'lists': lists,
        'nums': nums,
    }
    return render(request, 'g4l/todolist_detail.html', context=context)

@login_required(login_url="mylogin")
def todolist_delete(request, pk):
    todo = get_object_or_404(TodoList, pk=pk)
    schedule_id =todo.schedule.pk # lấy id của schedule liên quan
    if request.method == "POST":
        todo.delete()
        return redirect('schedule_detail', pk=schedule_id)
    return redirect('schedule_detail', pk=schedule_id)


@login_required(login_url="mylogin")
def todolist_update(request, pk):
    todo = get_object_or_404(TodoList, pk=pk)
    schedule_id =todo.schedule.pk
    if request.method == 'POST':
        form = TodoListUpdateForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('schedule_detail', pk=schedule_id)
    return redirect('schedule_detail', pk=schedule_id)


@login_required(login_url="mylogin")
def todolist_complete(request):
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

#
# TASKS
#
@login_required(login_url="mylogin")
def task(request, todo_id):
    todo = get_object_or_404(TodoList, id=todo_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.todo = todo # Liên kết task với TodoList
            task.save()
            return redirect('todolist_detail', pk=todo.id)

    else:
        form = TaskForm()

    sorted_task = todo.get_sorted_task()


    context = {
        'taskform':form,
        'todo': todo,
        'sorted_task':sorted_task
    
    }

    return render(request, 'g4l/task_form.html', context=context)

@login_required(login_url="mylogin")
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    todo_id =task.todo.pk
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('todolist_detail', pk=todo_id)
    return redirect('todolist_detail', pk=todo_id)

@login_required(login_url="mylogin")
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    todo_id =task.todo.pk # lấy id của todolist liên quan
    if request.method == "POST":
        task.delete()
        return redirect('todolist_detail', pk=todo_id)
    return redirect('todolist_detail', pk=todo_id)

@login_required(login_url="mylogin")
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    todo_id =task.todo.pk 
    if request.method == "POST":
        task.completed = not task.completed
        if task.completed:
            task.completed_at = timezone.now()
        else:
            task.completed_at = None
        task.save()

    #laáy tham số page từ request GET hoặc POST
    page = request.POST.get('page') or request.GET.get('page', '1') #mặc định trang 1 nếu không có page

    return redirect(f'{reverse("todolist_detail", kwargs={"pk":todo_id})}?page={page}')