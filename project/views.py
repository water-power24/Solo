from django.shortcuts import render, redirect
from .models import EverydayTask

def index(request):
    level = 1
    last_completed_day = request.session.get("last_completed_day", 0)
    task = EverydayTask.objects.filter(day__gt=last_completed_day).order_by("day").first()
    
    return render(request, "index.html", {"task": task, 'level': level})

def complete_day(request, day):
    if request.method == "POST":
        request.session["last_completed_day"] = day
        return redirect("index")

    task = EverydayTask.objects.filter(day=day).first()  # Теперь это объект, а не число
    return render(request, "index.html", {"task": task})

def reset_progress(request):
    request.session["last_completed_day"] = 0
    return redirect("index")