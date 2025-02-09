from django.shortcuts import render

def index(request):
    level =1
    return  render(request, 'index.html', {'level': level})
