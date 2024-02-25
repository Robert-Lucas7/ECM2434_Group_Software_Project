import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime

from .forms import Signup, LoginForm, MakePost
from .models import CustomUser, Challenge, UserChallenges, DailyChallenge
from django.db.models import Sum
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

def leaderboard(request, metric="streak"):
    users = CustomUser.objects.all()
    users_by_streak = users.order_by("-streak")
    position_of_current_user = -1
    data = []
    entries_per_page = 5
    for i, user in enumerate(users_by_streak):
        if user == request.user: #As users must be logged in to access this page.
            position_of_current_user = i + 1
        # Points for the different time periods are determined by iterating over all UserChallenge entries (as there is a points value for each entry)
        user_challenges = UserChallenges.objects.filter(user=user)
        overall_user_points = 0
        this_week_points = 0
        last_week_points = 0
        this_months_points = 0
        last_months_points = 0
        for uc in user_challenges:
            datetime_now = datetime.now()
            if uc.submitted.isocalendar()[1] == datetime_now.isocalendar()[1]:
                this_week_points += uc.points
            elif uc.submitted.isocalendar()[1] - 1 == datetime_now.isocalendar()[1] - 1:
                last_week_points += uc.points
            if uc.submitted.month == datetime_now.month:
                this_months_points += uc.points
            elif uc.submitted.month - 1 == datetime_now.month - 1:
                last_months_points += uc.points
            overall_user_points += uc.points 

        data.append({
            "username" : user.username,
            # The keys are displayed as a column header (so should be full words).
            "streak" : user.streak,
            "points" : overall_user_points if overall_user_points else 0,
            "this weeks points" : this_week_points,
            "last weeks points" : last_week_points,
            "this months points" : this_months_points,
            "last months points" : last_months_points
        })
    context = {
        'entries' : data,
        'user_position' : position_of_current_user,
        'first_page' : data[:5],
        'num_pages' : range((len(users) // entries_per_page) + 1) # To iterate over in the template to display the page buttons.
    }
    return render(request, 'project/leaderboard.html', context)


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
    todays_challenge = DailyChallenge.objects.latest("date_assigned")
    #print(todays_challenge.challenge)
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



def make_post(request):
    if request.method == 'POST':
        form = MakePost(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('message')
            uc = UserChallenges(user = request.user, submitted = datetime.now, completed = True, response = comment)
            uc.save()
    else:
        form = MakePost()
        return render(request, 'make_post.html', {'form': form})

def test(request):
    todays_challenge = Challenge.objects.last()
    context = {
        'todays_challenge': todays_challenge
    }
    print(todays_challenge)
    return render(request, 'test.html', context=context)

