from django.shortcuts import render
from .project_euler_count import count as pec_count

def index(request):
    return render(request, 'home/index.html')

def projects(request):
    context = {'project_euler_count': pec_count()}
    return render(request, 'home/projects.html', context)
