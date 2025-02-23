
from django.contrib import admin
from django.urls import path
from project import views
from project.views import complete_day, reset_progress, logout_view, habit_progress
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("complete_day/<int:day>/", complete_day, name="complete_day"),
    path("reset_progress/", reset_progress, name="reset_progress"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('create_habit/', views.create_habit, name='create_habit'),
    path('habit_progress/<int:habit_id>/', habit_progress, name='habit_progress'),
]
