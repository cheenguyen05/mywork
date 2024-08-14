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

    path('schedule', views.schedule_list, name='schedule_list'),

    path('schedule/new/', views.schedule_create, name='schedule_create'),

    path('schedule/<int:pk>/', views.schedule_detail, name='schedule_detail'),

    path('schedule/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),

    path('schedule/<int:pk>/update/', views.schedule_update, name='schedule_update'),

    path('schedule/<int:pk>/edit/', views.schedule_update, name='schedule_update'),

    path('create_todolist/<int:schedule_id>/', views.create_todolist, name='create_todolist'),

    path('todolist/<int:pk>/', views.todolist_detail, name='todolist_detail'),

    path('todolist/<int:pk>/delete/', views.todolist_delete, name='todolist_delete'),

    path('todolist/<int:pk>/update/', views.todolist_update, name='todolist_update'),

    path('task/<int:todo_id>/', views.task, name='task'),

    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),

    path('task/<int:pk>/update/', views.task_update, name='task_update'),

    path('task_complete/<int:pk>/', views.task_complete, name='task_complete'),
]