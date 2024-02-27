import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime

from .forms import Signup, LoginForm, MakePost
from .models import CustomUser, Challenge, UserChallenges, DailyChallenge
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.
from django.http import HttpResponse

from django.shortcuts import render
import math

def index(request):
    return render(request, 'project/index.html')

def sample_profile(request):
    return render(request, 'project/sample_profile.html')

@login_required
def leaderboard(request, metric="streak"):
    users = CustomUser.objects.all()
    users_by_streak = list(users.order_by("-streak"))
    position_of_current_user = 0
    past_current_user = False
    data = []
    entries_per_page = 5
    for i, user in enumerate(users_by_streak):
        if i != 0 and user.streak != users_by_streak[i-1].streak and not past_current_user:
            position_of_current_user += 1
            if user == request.user:
                past_current_user = True
        
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
        'user_position' : position_of_current_user + 1,
        'first_page' : data[:5],
        'num_pages' : range(math.ceil(len(users) /entries_per_page)), # To iterate over in the template to display the page buttons.
        'num_challenges_completed' : {
            "username" : request.user.username,
            "challenges_completed" : UserChallenges.objects.filter(user=request.user).count(),
            "challenges_completed this weeks points" : UserChallenges.objects.filter(user=request.user, submitted__week=datetime.now().isocalendar()[1]).count(),
            "challenges_completed this months points" : UserChallenges.objects.filter(user=request.user, submitted__month=datetime.now().month).count()
        }
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
    user = get_object_or_404(CustomUser, username=username)
    user_challenges = UserChallenges.objects.filter(user=user)
    todays_challenge = DailyChallenge.objects.latest("assigned")  # Corrected from "date_assigned" to "assigned"
    context = {
        'user': user,
        'user_challenges': user_challenges,
        'user_points' : user_challenges.aggregate(Sum("points"))['points__sum']
        #'todays_challenge': todays_challenge.challenge
    }
    return render(request, 'project/profile.html', context)


# This is the view for the home page. It will display the most recent posts.
def home(request):
    print(request.user)
    print()
    #Get the most recent challenge from the database.
    todays_challenge = DailyChallenge.objects.latest('assigned')
    #Get all posts that are for the most recent challenge
    posts_for_todays_challenge = UserChallenges.objects.filter(daily_challenge = todays_challenge).order_by("-submitted")
    users_challenge = posts_for_todays_challenge.filter(user = request.user)
    
    context = {
        'daily_challenge' : todays_challenge.challenge.title,
        'posts' : [{
                    'username' : post.user.username,
                    'created_at' : post.submitted,
                    'content' : post.response
                } for post in posts_for_todays_challenge],
        'already_completed_challenge' : True if users_challenge else False #If the user has already completed the daily challenge, they will be given the option to resubmit it.
    }
    return render(request, 'home.html', context)



def make_post(request):
    if request.method == 'POST':
        form = MakePost(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            uc = UserChallenges(daily_challenge = DailyChallenge.objects.latest("date_assigned"), user = request.user, submitted = datetime.now(), completed = True, response = comment)
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

