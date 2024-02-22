from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime

from .forms import Signup, LoginForm
from .models import CustomUser, Challenge, UserChallenges, ChallengesAssigned
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

def sample_profile(request):
    return render(request, 'project/sample_profile.html')

def leaderboard(request):
    return render(request, 'project/leaderboard.html')


def registration(request):
    form = Signup(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password1')
            # new_user = authenticate(username=username, password=password)
            # if new_user is not None:
            #     login(request, new_user)
            #     return redirect('home')
            return redirect("login")
        else:
            print(form.errors)
            return render(request, 'project/registration.html', {'form': form})
    else:
        form = Signup()
        return render(request, 'project/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                print("User logged in successfully")
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(CustomUser,
                             username=username)  # Should prevent SQL injection as django queries are parameterized.
    user_challenges = UserChallenges.objects.filter(user=user)
    todays_challenge = ChallengesAssigned.objects.latest("date_assigned")
    print(todays_challenge.challenge)
    context = {
        'user': user,
        'user_challenges': user_challenges,
        'todays_challenge': todays_challenge.challenge
    }
    return render(request, 'project/profile.html', context)

# This is the view for the home page. It will display the most recent posts.
def home(request):
    # Simulated posts data with datetime objects for 'created_at'
    sample_posts = [
        {'title': 'Sample Post 1', 'author': {'username': 'user1'}, 'created_at': datetime(2024, 2, 20), 'content': 'This is the content of the first sample post.'},
        {'title': 'Sample Post 2', 'author': {'username': 'user2'}, 'created_at': datetime(2024, 2, 21), 'content': 'This is the content of the second sample post, showcasing more information.'},
        {'title': 'Sample Post 3', 'author': {'username': 'user3'}, 'created_at': datetime(2024, 2, 22), 'content': 'Here is the third sample post. It includes even more content for display.'}
    ]

    # Pass the simulated data to the template
    return render(request, 'home.html', {'posts': sample_posts})
