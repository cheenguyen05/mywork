from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.decorators import login_required

from .models import Profile

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
    query = request.GET.get('query', '')
    filter_type = request.GET.get('filter_type', 'everything')

    if not query:
        users = User.objects.none()
        #return redirect("")
    else:
        users = User.objects.all()

        
        if query:  # Nếu không có filter_type nhưng có query, tìm kiếm mọi thứ
            user_profiles = Profile.objects.filter(
                Q(user__username__icontains=query) |
                Q(school__icontains=query) |
                Q(age__icontains=query)
            )
            users = users.filter(id__in=user_profiles.values('user_id'))
        else:
            if filter_type == 'username' and query:
                users = users.filter(username__icontains=query)
            elif filter_type == 'school' and query:
                user_profiles = Profile.objects.filter(school__icontains=query)
                users = users.filter(id__in=user_profiles.values('user_id'))
            elif filter_type == 'age' and query:
                user_profiles = Profile.objects.filter(age=query)
                users = users.filter(id__in=user_profiles.values('user_id'))
            

    context = {
        'users': users,
        'query': query,
        'filter_type': filter_type
    }
    
    return render(request, 'g4l/search.html', context=context)