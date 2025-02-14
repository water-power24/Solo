
from django.contrib import admin
from django.urls import path
from project import views
from project.views import complete_day, reset_progress

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("complete_day/<int:day>/", complete_day, name="complete_day"),
    path("reset_progress/", reset_progress, name="reset_progress"),
]
