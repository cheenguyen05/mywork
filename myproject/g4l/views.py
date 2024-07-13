from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.decorators import login_required

from .models import Profile


#
# AUTHENTICATION 
#

# - Authentication models and functions
 
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def homepage(request):

    return render(request, 'g4l/index.html')




def register(request):

    form =  CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("mylogin")
 

    context = {'registerform':form}

    return render(request, 'g4l/register.html', context=context)



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


def user_logout(request):

    auth.logout(request)

    return redirect("")


@login_required(login_url="mylogin")
def dashboard(request):

    return render(request, 'g4l/dashboard.html')

@login_required(login_url="mylogin")
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')  
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_id': request.user.id,
    }

    return render(request, 'g4l/profile.html', context=context)