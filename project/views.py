from django.shortcuts import render, redirect
from .models import EverydayTask, CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    level = CustomUser.objects.values('level')
    last_completed_day = request.session.get("last_completed_day", 0)
    task = EverydayTask.objects.filter(day__gt=last_completed_day).order_by("day").first()
    
    return render(request, "index.html", {"task": task, 'level': level[0]['level']})

def complete_day(request, day):
    if request.method == "POST":
        request.session["last_completed_day"] = day
        return redirect("index")

    task = EverydayTask.objects.filter(day=day).first() 
    return render(request, "index.html", {"task": task})

def reset_progress(request):
    request.session["last_completed_day"] = 0
    return redirect("index")

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    user = request.user 
    return render(request, 'profile.html', {'user': user})
