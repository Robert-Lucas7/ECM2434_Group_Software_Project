from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render

def index(request):
    return render(request, 'project/index.html')

def home(request):
    return render(request, 'project/home.html')

def navbar(request):
    return render(request, 'project/navbar.html')

def base(request):
    return render(request, 'project/base.html')