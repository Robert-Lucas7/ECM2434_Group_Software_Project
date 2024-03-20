from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.conf import settings
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError

from datetime import datetime
import math
import django

from . import cron
from .forms import Signup, LoginForm, MakePost, ChangeProfilePicture
from .models import CustomUser, Challenge, UserChallenges, DailyChallenge, Village, VillageShop
import json
import random


def index(request):
    return render(request, 'project/index.html')


def privacy_policy(request):
    return render(request, 'project/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'project/terms_conditions.html')
def terms_conditions(request):
    return render(request, 'project/terms_conditions.html')

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
    todays_challenges = UserChallenges.objects.filter(submitted__date=datetime.now()).exclude(user_lat__isnull=True)

    challenge_list = [[challenge.response, float(challenge.user_lat), float(challenge.user_long)]
                      for challenge in completed_challenges]

    todays_challenge_list = [[challenge.response, float(challenge.user_lat), float(challenge.user_long)]
        for challenge in todays_challenges]

    return render(request, 'map.html', context={'challenges': json.dumps(challenge_list),
                                                'todays_challenges': json.dumps(todays_challenge_list)})



@login_required()
def village_shop(request):
    # There must be a query parameter called 'position' in the get request of this page so you know in which position to store the bought item. If this parameter
    # isn't present an error page will be displayed with an option to go back to the village page.
    
    valid_position = True
    if 'position' in request.GET:
        pos = request.GET['position']
        if pos.isdigit():
            pos = int(pos)
            if pos < 0 or pos > 35:
                valid_position = False
        else:
            valid_position = False
    else:
        valid_position = False
    context = {}
    if valid_position:
        num_coins = request.user.coins  # UserChallenges.objects.filter(user=request.user).aggregate(Sum('points'))['points__sum']
        if not num_coins:
            num_coins = 0
        items = [{
            'item': item.item,
            'cost': item.cost,
            'can_afford': num_coins > item.cost,
            'image_name': item.image_name
        } for item in VillageShop.objects.all()]
        context = {
            'num_coins': num_coins,
            'items': items,
            'position': int(request.GET['position'])
        }
    context['error'] = not valid_position
    return render(request, 'project/village_shop.html', context)
    

@login_required
def village(request, username):
    user = get_object_or_404(CustomUser, username=username)
    # The grid will always be 6x6 so the 'position' attribute can be used to find the row/col.
    errors = []
    if request.method == "POST" and user == request.user:
        if 'item' in request.POST and 'position' in request.POST:
            valid = True
            # Validate position - convert to 'helper' function.
            pos = request.POST['position']
            if pos.isdigit():
                pos = int(pos)
                if pos < 0 or pos > 35:
                    valid = False
            else:
                valid = False
            # Validate item
            all_items = VillageShop.objects.filter(item=request.POST['item'])  # Safe from sql injection.
            if len(all_items) != 1:
                valid = False

            if valid:
                shop_item = all_items[0]  # all_items has exactly one element in it.
                num_same_items = Village.objects.filter(user=request.user, item=shop_item).count()
                if shop_item.cost > request.user.coins:
                    errors.append("Insufficient coints to buy item")
                if len(errors) == 0:  # Can buy the item.
                    # Check if there is already an item in the position and if there is delete it.
                    item_in_position = Village.objects.filter(user=request.user,
                                                              position=pos)  # pos has been converted to an int before.
                    if item_in_position:
                        item_in_position.delete()
                    new_item = Village(user=request.user, item=shop_item, position=pos)
                    user.coins -= shop_item.cost
                    new_item.save()
                    user.save()
            else:
                print("INVALID POST PARAMS")
    
    all_village_items = Village.objects.filter(user=user).order_by("position")
    board = []
    total_score = 0 #initialize score
    for row in range(6):
        board_row = []
        for col in range(6):
            image_path = None
            item_score = 0
            if all_village_items.exists() and all_village_items[0].position == row * 6 + col:
                village_item = all_village_items[0]
                image_path = village_item.item.image_name
                item_score = village_item.item.score # Fetch the score
                all_village_items = all_village_items[1:] # Move to the next item
            board_row.append({'image_path': image_path, 'score': item_score})
            total_score += item_score # Add the score to the total score     
        board.append(board_row)
    user.score = total_score # Update the user's score
    user.save()
    num_coins = user.coins if user.coins else 0
    context = {
        'board': board,
        'num_coins': num_coins,
        'total_score': total_score,
        'user': user,
        
    }
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
        this_months_coins = 0
        for uc in user_challenges:
            if uc.submitted.month == datetime.now().month:
                this_months_coins += uc.points

        data.append({
            "username": user.username,
            # The keys are displayed as a column header (so should be full words).
            "streak": user.streak,
            "monthly coins": this_months_coins,
            "village score" : user.score, 
        })
    context = {
        'entries': data,
        'user_position': position_of_current_user + 1,
        'first_page': data[:5],
        # To iterate over in the template to display the page buttons.
        'num_pages': range(math.ceil(len(users) / entries_per_page)),
        'num_challenges_completed': {
            "username": request.user.username,
            "challenges_completed": UserChallenges.objects.filter(user=request.user).count()
        }
    }
    return render(request, 'project/leaderboard.html', context)


import os


def registration(request):
    form = Signup(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = CustomUser.objects.get(username=form.cleaned_data.get('username'))
            profile_picture  = form.cleaned_data.get('profile_picture')
            user.profile_picture = profile_picture
            user.save()
            # request_file = open(os.path.join(settings.BASE_DIR, 'project', 'static/project/Example_Profile_Pic.jpg'), 'rb')  # This should be changed for when the custom profile picture is implemented.
            # if request_file:
            #     fs = FileSystemStorage(location=f"{settings.MEDIA_ROOT}/{form.cleaned_data.get('username')}")
            #     fs.save("profile-picture.jpg", request_file)
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
    if request.method == "POST":  
        profile_picture = request.POST.get('profile_picture')
        if profile_picture:
            user = request.user
            user.profile_picture = profile_picture
            user.save()
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
    todays_challenge = DailyChallenge.objects.all().order_by('-assigned')[0]
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
    daily_challenge = DailyChallenge.objects.all().order_by('-assigned')[0]

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

            # Calculating the users points for this challenge
            points = 100 + max(
                math.ceil((-0.1 * ((now() - daily_challenge.assigned).total_seconds() / 3600) + 2.4) * 10.5),
                0) + request.user.streak  # For a max of around 25 points for submitting quickly.
            print(points)
            user.coins += points
            user.save()
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


@login_required()
def gamekeeper(request):
    if request.method == 'POST':
        if 'deleteButton' in request.POST:
            post_id = request.POST.get('post_id')
            post = UserChallenges.objects.get(id=post_id)
            post.delete()

        elif 'editButton' in request.POST:
            post_id = request.POST.get('post_id')
            post = UserChallenges.objects.get(id=post_id)

            new_response = request.POST.get('response')
            post.response = new_response
            post.save()
        elif 'challengeDelete' in request.POST:
            challenge_title = request.POST.get('challenge_title')
            challenge = Challenge.objects.get(title=challenge_title)
            print(f'Challenge {challenge_title} has been deleted')
            challenge.delete()

        elif 'submit_challenge' in request.POST:
            challenge_title = request.POST.get('new_title')
            challenge_description = request.POST.get('new_description')

            challenge_lat = request.POST.get('challenge_lat')
            challenge_long = request.POST.get('challenge_long')

            if challenge_lat and challenge_long:
                try:
                    challenge = Challenge(title=challenge_title, description=challenge_description, location_lat=challenge_lat, location_long=challenge_long)
                except ValidationError as e:
                    challenge = Challenge(title=challenge_title, description=challenge_description)


            else:
                challenge = Challenge(title=challenge_title, description=challenge_description)

            challenge.save()

        elif "random_challenge" in request.POST:
            daily_challenge = DailyChallenge.objects.all().order_by('-assigned')[0]
            challenges = Challenge.objects.exclude(title = daily_challenge.challenge.title)
            print(daily_challenge.challenge.title)


            challenge = random.choice(challenges)

            new_daily_challenge = DailyChallenge(challenge=challenge, assigned=django.utils.timezone.now())
            new_daily_challenge.save()

            daily_challenge = DailyChallenge.objects.all().order_by('-assigned')[0]
            print(daily_challenge.challenge.title)





    user = request.user
    if user.is_gamekeeper:
        user_challenges = UserChallenges.objects.all()
        challenges = Challenge.objects.all()
        daily_challenge = DailyChallenge.objects.all().order_by('-assigned')[0]

        return render(request, 'game_keeper.html', context={'userchallenges': user_challenges, 'challenges': challenges, 'daily_challenge': daily_challenge})
    else:
        return redirect('home')
