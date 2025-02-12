from django.shortcuts import render

def index(request):
    level =1
    today = now().day
    task = EverydayTask.objects.filter(day=today).first()
    if not task:
        task = EverydayTask.objects.order_by('day').first()
    return  render(request, 'index.html', {'level': level, 'task': task})

from django.shortcuts import render
from .models import EverydayTask
from datetime import datetime
from django.utils.timezone import now

