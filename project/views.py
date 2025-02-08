from django.shortcuts import render

from django.shortcuts import render

def level_up(request):
    level = 1  
    return render(request, 'levelup/level_up.html', {'level': level})
