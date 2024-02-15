from django.shortcuts import render, get_object_or_404
from .models import User, Challenge, UserChallenges, ChallengesAssigned
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

def registration(request):
    return render(request, 'project/registration.html')

def profile(request, username):
    user = get_object_or_404(User, pk=username) #Should prevent SQL injection as django queries are parameterized.
    user_challenges = UserChallenges.objects.filter(user=user)    
    todays_challenge = ChallengesAssigned.objects.latest("date_assigned")
    print(todays_challenge.challenge)
    context = {
        'user':user,
        'user_challenges': user_challenges,
        'todays_challenge' : todays_challenge.challenge
    }
    return render(request, 'project/profile.html', context)
