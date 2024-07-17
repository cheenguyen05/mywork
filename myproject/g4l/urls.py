from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.homepage, name=""),

    path('register', views.register, name="register"),

    path('mylogin', views.mylogin, name="mylogin"),
    
    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),

    path('profile/<int:user_id>/', views.profile, name="profile"),

    path('profile', views.profile, name="profile"),

    path('search', views.search_view, name='search'),

]