from django.shortcuts import render, get_object_or_404
from .models import User
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

def profile(request, username):
    user = get_object_or_404(User, pk=username) #Should prevent SQL injection as django queries are parameterized.
    context = {
        'user':user,
        'challenges': []
    }
    return render(request, 'project/profile.html', context)