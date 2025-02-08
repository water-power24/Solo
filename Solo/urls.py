
from django.contrib import admin
from django.urls import path
from level_up import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.level_up, name='level_up'),
]
