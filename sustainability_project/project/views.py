# import json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime

from .forms import Signup, LoginForm, MakePost
from .models import CustomUser, Challenge, UserChallenges, DailyChallenge
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
    order_to_display = None
    table_header = ""
    # Sort the users by the metric to be compared.
    if metric == "points":
        order_to_display = users.order_by('-points')
        table_header = "Points"
    elif metric == "streak":
        order_to_display = users.order_by('-streak')
        table_header = "Streak"
    else:
        return redirect("leaderboard") #If there is an invalid 'metric' in the url, then redirect to the 'streak' leaderboard page.
    
    # Split the entries into pages of 5 and remove potentially sensitive data from the models.
    data = []
    current_page = []
    entries_on_page = 5
    for i,entry in enumerate(order_to_display):
        
        metricValue = 0
        if metric == "points":
            metricValue = entry.points
        else:
            metricValue = entry.streak
        current_page.append({
            'username' : entry.username,
            'metric' : metricValue
        })
        if(len(current_page) == entries_on_page or i == len(order_to_display) - 1):
            data.append(current_page)
            current_page = []
    
    context = {
        'entries' : data,
        'table_header' : table_header
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

