from django.shortcuts import render, redirect
from .models import EverydayTask, CustomUser
from .forms import CustomUserCreationForm, FitnessForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login

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
    step = request.session.get('registration_step', '1')

    if request.method == 'POST':
        if step == '1':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                request.session['new_user_id'] = user.id  # Сохраняем ID пользователя
                request.session['registration_step'] = '2'  # Переход на шаг 2
                return redirect('register')

        elif step == '2':
            user_id = request.session.get('new_user_id')
            user = CustomUser.objects.get(id=user_id)
            form = FitnessForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                login(request, user)  # Автоматический вход
                del request.session['new_user_id']
                del request.session['registration_step']
                return redirect('index')

    # Отображение правильной формы в зависимости от шага
    if step == '1':
        form = CustomUserCreationForm()
    else:
        form = FitnessForm()

    return render(request, 'register.html', {'form': form, 'step': step})


@login_required
def profile(request):
    user = request.user 
    return render(request, 'profile.html', {'user': user})
