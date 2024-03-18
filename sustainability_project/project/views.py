from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.conf import settings
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from datetime import datetime
import math
from .forms import Signup, LoginForm, MakePost
from .models import CustomUser, Challenge, UserChallenges, DailyChallenge, Village, VillageShop
import json
import random


def index(request):
    return render(request, 'project/index.html')

def privacy_policy(request):
    return render(request, 'project/privacy_policy.html')

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to the index page after logging out


def sample_profile(request):
    return render(request, 'project/sample_profile.html')

@login_required()
def map(request):
    # Will update

    user = request.user

    completed_challenges = UserChallenges.objects.filter(user=user).exclude(user_lat__isnull=True)

    challenge_list = [[challenge.response, float(challenge.user_lat), float(challenge.user_long)]
                      for challenge in completed_challenges]

    print(challenge_list)

    return render(request, 'map.html', context={'challenges': json.dumps(challenge_list)})

@login_required()
def village_shop(request):
    num_coins = UserChallenges.objects.filter(user=request.user).aggregate(Sum('points'))['points__sum']
    if not num_coins:
        num_coins = 0
    items = [{
        'item' : item.item,
        'cost' : item.cost,
        'quantity_remaining' : item.max_quantity - Village.objects.filter(user=request.user, item=item).count(),
        'can_afford' : num_coins > item.cost
    } for item in VillageShop.objects.all()]
    context = {
        'num_coins' : num_coins,
        'items' : items
    }

    return render(request, 'project/village_shop.html', context)

@login_required
def village(request):
    # The grid will always be 6x6 so the 'position' attribute can be used to find the row/col.
    # Build the board from the DB.
    all_village_items = list(Village.objects.filter(user=request.user).order_by("position"))
    # for item in all_village_items:
    #     print(f"{item.position}")
    board = []
    # total_images = 9  # Total available images, from 01.png to 09.png
    # Corrected the range to start from 1 and added proper formatting for file names
    # available_images = [f'{i:02d}.png' for i in range(1, total_images + 1)]
    # empty_chance = 0.9  # Approx 30% of the tiles will be empty
    
    for row in range(6):  # Assuming a 6x6 board
        board_row = []
        for col in range(6):
            image_path = None
            if len(all_village_items) > 0 and all_village_items[0].position == row * 6 + col:
                image_path = all_village_items[0].item.image_name
                all_village_items.pop(0)
            # if random.random() > empty_chance and available_images:
            #     # Select a random image and remove it from the list to avoid repeats
            #     image_path = f'project/game_assets/{random.choice(available_images)}'
            #     available_images.remove(image_path.split('/')[-1])
            # else:
            #     image_path = None  # This tile will be empty
            board_row.append({'image_path': image_path})
        board.append(board_row)

    context = {'board': board}
    return render(request, 'project/village.html', context)


@login_required
def leaderboard(request, metric="streak"):
    users = CustomUser.objects.all()
    users_by_streak = list(users.order_by("-streak"))
    position_of_current_user = 0
    past_current_user = False
    data = []
    entries_per_page = 5
    for i, user in enumerate(users_by_streak):
        if i != 0 and user.streak != users_by_streak[i - 1].streak and not past_current_user:
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
            "username": user.username,
            # The keys are displayed as a column header (so should be full words).
            "streak": user.streak,
            "points": overall_user_points if overall_user_points else 0,
            "this weeks points": this_week_points,
            "last weeks points": last_week_points,
            "this months points": this_months_points,
            "last months points": last_months_points
        })
    context = {
        'entries': data,
        'user_position': position_of_current_user + 1,
        'first_page': data[:5],
        # To iterate over in the template to display the page buttons.
        'num_pages': range(math.ceil(len(users) / entries_per_page)),
        'num_challenges_completed': {
            "username": request.user.username,
            "challenges_completed": UserChallenges.objects.filter(user=request.user).count(),
            "challenges_completed this weeks points": UserChallenges.objects.filter(user=request.user, submitted__week=
            datetime.now().isocalendar()[1]).count(),
            "challenges_completed this months points": UserChallenges.objects.filter(user=request.user,
                                                                                     submitted__month=datetime.now().month).count()
        }
    }
    return render(request, 'project/leaderboard.html', context)


import os


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
            # Save user profile to the file system.
            request_file = open(os.path.join(settings.BASE_DIR, 'project', 'static/project/Example_Profile_Pic.jpg'),
                                'rb')  # This should be changed for when the custom profile picture is implemented.
            if request_file:
                fs = FileSystemStorage(location=f"{settings.MEDIA_ROOT}/{form.cleaned_data.get('username')}")
                fs.save("profile-picture.jpg", request_file)
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
                return render(request, 'login.html', {'error': 'Incorrect username or password.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required()
def profile(request, username):
    # If a POST request is made to this page with an image (profile picture) save it to '/media/{username}/profile-picture.{extension}'
    # Needs improved security - only jpg and png should be uploaded.
    if request.method == "POST":  # From: https://www.geeksforgeeks.org/django-upload-files-with-filesystemstorage/
        # Document should be changed to 'image' (or similar)
        request_file = request.FILES['document'] if 'document' else None
        if request_file:
            fs = FileSystemStorage(
                location=f"{settings.MEDIA_ROOT}/{request.user.username}")
            file = fs.save("profile-picture", request_file)
            # fileurl = fs.url(file)

    # If the user requesting the profile page isn't that user, redirect them to the homepage.
    # if request.user.username == username:
    user = get_object_or_404(CustomUser, username=username)
    user_challenges = UserChallenges.objects.filter(user=user)
    # Corrected from "date_assigned" to "assigned"
    todays_challenge = DailyChallenge.objects.latest("-assigned")
    context = {
        'user': user,
        'user_challenges': user_challenges,
        'user_points': user_challenges.aggregate(Sum("points"))['points__sum']
        # 'todays_challenge': todays_challenge.challenge
    }
    return render(request, 'project/profile.html', context)
    # else:
    #   return redirect("home")


# This is the view for the home page. It will display the most recent posts.
@login_required()
def home(request):
    # Get the most recent challenge from the database.
    # Currently doesn't actually get latest, just so can test out all challenges
    todays_challenge = DailyChallenge.objects.all()[2]
    # Get all posts that are for the most recent challenge
    posts_for_todays_challenge = UserChallenges.objects.filter(
        daily_challenge=todays_challenge).order_by("-submitted")
    users_challenge = posts_for_todays_challenge.filter(user=request.user)

    context = {
        'daily_challenge': todays_challenge.challenge.title,
        'posts': [{
            'username': post.user.username,
            'created_at': post.submitted,
            'content': post.response
        } for post in posts_for_todays_challenge],
        # If the user has already completed the daily challenge, they will be given the option to resubmit it.
        'already_completed_challenge': True if users_challenge else False
    }
    return render(request, 'home.html', context)

@login_required()
def make_post(request):
    user = request.user
    daily_challenge = DailyChallenge.objects.all()[2]

    try:
        previous_challenge_completed = UserChallenges.objects.filter(user=user, daily_challenge=daily_challenge)[0]
        response = previous_challenge_completed.response
        completed = previous_challenge_completed.completed
    except:
        previous_challenge_completed = False
        response = None
        completed = None

    if request.method == 'POST':
        form = MakePost(request.POST)
        if form.is_valid():
            if previous_challenge_completed:
                print("success")
                previous_challenge_completed.delete()
            else:
                print("fail")
                user.streak += 1

            if user.streak > user.best_streak:
                user.best_streak = user.streak
            user.save()
            # Calculating the users points for this challenge
            points = 100 + max(
                math.ceil((-0.1 * ((now() - daily_challenge.assigned).total_seconds() / 3600) + 2.4) * 10.5),
                0) + request.user.streak  # For a max of around 25 points for submitting quickly.
            print(points)

            comment = form.cleaned_data.get('comment')
            user_lat = request.POST.get('user_lat')
            user_long = request.POST.get('user_long')

            if not user_lat or not user_long:
                user_lat = None
                user_long = None


            # To access this page user must be authenticated so request.user is adequate.
            uc = UserChallenges(daily_challenge=daily_challenge, user=request.user,
                                submitted=datetime.now(), completed=True, response=comment,
                                points=points, user_lat=user_lat, user_long=user_long)
            uc.save()

            return redirect("home")
    else:
        form = MakePost()
    context = {
        'form': form,
        'daily_challenge': daily_challenge.challenge,
        'completed': completed,
        'response': response
    }
    return render(request, 'make_post.html', context)

