from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.decorators import login_required

from .models import Profile, SearchInfo

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
    results = SearchInfo.objects.all()

    if query:
        results = results.filter(
            Q(name__icontains=query) |
            Q(school__icontains=query) |
            Q(age=query)
        )

    context = {
        'results': results,
        'query': query,
    }
    
    return render(request, 'search_results.html', context=context)