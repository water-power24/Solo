from django.shortcuts import render, redirect, get_object_or_404
from .models import EverydayTask, CustomUser, Habit, HabitProgress, UserProgress
from .forms import CustomUserCreationForm, FitnessForm, HabitForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.utils.timezone import now
from datetime import timedelta

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
                request.session['new_user_id'] = user.id  
                request.session['registration_step'] = '2'  
                return redirect('register')

        elif step == '2':
            user_id = request.session.get('new_user_id')
            user = CustomUser.objects.get(id=user_id)
            form = FitnessForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                login(request, user)  
                del request.session['new_user_id']
                del request.session['registration_step']
                return redirect('index')

    if step == '1':
        form = CustomUserCreationForm()
    else:
        form = FitnessForm()

    return render(request, 'register.html', {'form': form, 'step': step})


@login_required
def profile(request):
    user = request.user 
    habits_in_progress = Habit.objects.filter(user=request.user, completed=False)
    completed_habits = Habit.objects.filter(user=request.user, completed=True)

    return render(request, 'profile.html', {
        'user': user, 
        'habits': habits_in_progress,  
        'habits_in_progress': habits_in_progress,
        'completed_habits': completed_habits,
    })
@login_required
def create_habit(request):
    if request.method == "POST":
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_progress', habit_id=habit.id)
    else:
        form = HabitForm()

    return render(request, 'create_habit.html', {'form': form})

def habit_progress(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    progress_days = {p.day: p for p in HabitProgress.objects.filter(habit=habit)}
    for day in range(1, 22):
        if day not in progress_days:
            progress_days[day] = HabitProgress.objects.create(habit=habit, day=day, completed=False)

    if request.method == "POST":
        completed_count = 0  

        for day in range(1, 22):
            completed = request.POST.get(f"day_{day}") == "on"
            progress_days[day].completed = completed
            progress_days[day].save()

            if completed:
                completed_count += 1

        habit.completed_days = completed_count
        habit.completed = completed_count == 21  
        habit.save()

        return redirect("habit_progress", habit_id=habit.id)

    return render(request, "habit_progress.html", {"habit": habit, "progress_days": progress_days.values()})