from django.shortcuts import render, redirect
from .models import EverydayTask, CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
    level = request.user.level if request.user.is_authenticated else 1
    last_completed_day = request.session.get("last_completed_day", 0)
    task = EverydayTask.objects.filter(day__gt=last_completed_day).order_by("day").first()
    
    return render(request, "index.html", {"task": task, 'level': level})

@login_required
def complete_day(request, day):
    if request.method == "POST":
        last_completed_day = request.session.get("last_completed_day", 0)
        request.session["last_completed_day"] = day
        
        user = request.user
        completed_days = day  

        if completed_days % 2 == 0:  
            user.level += 1
            user.save()

        return redirect("index")

    task = EverydayTask.objects.filter(day=day).first() 
    return render(request, "index.html", {"task": task})

def reset_progress(request):
    request.session["last_completed_day"] = 0
    if request.user.is_authenticated:
        request.user.level = 1
        request.user.save()
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
