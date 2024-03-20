from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.conf import settings
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.contrib import messages

from datetime import datetime
import math
import django

from . import cron
from .forms import Signup, LoginForm, MakePost, ChangeProfilePicture
from .models import CustomUser, Challenge, UserChallenges, DailyChallenge, Village, VillageShop
import json
import random
import os


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
    return redirect('index')  


def sample_profile(request):
    return render(request, 'project/sample_profile.html')

# Code by Dan
@login_required
def remove_item(request):
    if request.method == "POST":
        pos = request.POST.get('position')
        if pos:
            pos = int(pos) 
            # Retrieve the item to be removed
            item_to_remove = Village.objects.filter(user=request.user, position=pos).first()
            # Delete item from the village and refund user
            if item_to_remove:
                refund_amount = int(item_to_remove.item.cost * 0.6)
                request.user.coins += refund_amount
                request.user.save()
                item_to_remove.delete()
                messages.success(request, f"Item successfully removed. {refund_amount} coins refunded.")
            else:
                messages.error(request, "No item found in the selected position.")
        else:
            messages.error(request, "Position not specified.")
    # Redirect back to the referring page or to the 'village'
    return redirect(request.META.get('HTTP_REFERER', 'village'))

# Code by Ben
@login_required()
def map(request):
    user = request.user

    completed_challenges = UserChallenges.objects.filter(user=user).exclude(user_lat__isnull=True)
    todays_challenges = UserChallenges.objects.filter(submitted__date=datetime.now()).exclude(user_lat__isnull=True)

    challenge_list = [[challenge.response, float(challenge.user_lat), float(challenge.user_long)]
                      for challenge in completed_challenges]

    todays_challenge_list = [[challenge.response, float(challenge.user_lat), float(challenge.user_long)]
        for challenge in todays_challenges]

    return render(request, 'map.html', context={'challenges': json.dumps(challenge_list),
                                                'todays_challenges': json.dumps(todays_challenge_list)})


# Code by Rob
@login_required()
def village_shop(request):
    pos = request.GET.get('position', None)
    context = {'error': True}  # Default context in case of an invalid position
    if pos and pos.isdigit():
        pos = int(pos)
        if 0 <= pos <= 35:
            item_to_remove = Village.objects.filter(user=request.user, position=pos).first()
            refund_amount = 0
            if item_to_remove:
                refund_amount = int(item_to_remove.item.cost * 0.6)
            
            items = [{
                'item': item.item,
                'cost': item.cost,
                'can_afford': request.user.coins >= item.cost,
                'image_name': item.image_name
            } for item in VillageShop.objects.all()]

            context = {
                'num_coins': request.user.coins,
                'items': items,
                'position': pos,
                'item_to_remove': item_to_remove,
                'refund_amount': refund_amount, 
            }
    else:
        return redirect('error_page')  # Redirect to an error page or handle as fits your application

    return render(request, 'project/village_shop.html', context)


# Code by Dan
@login_required
def village(request, username):
    user = get_object_or_404(CustomUser, username=username)
    # check for invalid requests
    if request.method == "POST" and user == request.user:
        item_name = request.POST.get('item')
        pos = request.POST.get('position')

        if not pos.isdigit() or not item_name:
            messages.error(request, "Invalid request.")
            return redirect('village', username=username)

        pos = int(pos)
        if pos < 0 or pos > 35:
            messages.error(request, "Invalid position.")
            return redirect('village', username=username)

        try:
            shop_item = VillageShop.objects.get(item=item_name)
        except VillageShop.DoesNotExist:
            messages.error(request, "Item does not exist.")
            print("here3")
            return redirect('village', username=username)

        existing_item = Village.objects.filter(user=user, position=pos).first()
        if existing_item:
            refund_amount = int(existing_item.item.cost * 0.6)
            user.coins += refund_amount
            existing_item.delete()

        if user.coins < shop_item.cost:
            messages.error(request, "Insufficient coins to buy this item.")
            print(shop_item.cost)
            return redirect('village', username=username)

        user.coins -= shop_item.cost
        Village.objects.create(user=user, item=shop_item, position=pos)
        user.save()
        messages.success(request, "Item placed successfully.")
    else:  # Valid request
        # Create board with items in the correct positions
        all_village_items = Village.objects.filter(user=user).order_by("position")
        board = []
        total_score = 0
        for row in range(6):
            board_row = []
            for col in range(6):
                image_path = None
                item_score = 0
                if all_village_items.exists() and all_village_items[0].position == row * 6 + col:
                    village_item = all_village_items[0]
                    image_path = village_item.item.image_name
                    item_score = village_item.item.score
                    all_village_items = all_village_items[1:]
                board_row.append({'image_path': image_path, 'score': item_score})
                total_score += item_score
            board.append(board_row)
        user.score = total_score
        user.save()
        num_coins = user.coins if user.coins else 0
        context = {
            'board': board,
            'num_coins': num_coins,
            'total_score': total_score,
            'user': user,
        }
        return render(request, 'project/village.html', context)

    # Redirect back to the village page after POST action
    return redirect('village', username=username)

# Code by Rob
@login_required
# Displays leaderboard of users based on the metric passed in the URL
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
            "streak": user.streak,
            "monthly coins": this_months_coins,
            "village score" : user.score, 
        })
    context = {
        'entries': data,
        'user_position': position_of_current_user + 1,
        'first_page': data[:5],
        'num_pages': range(math.ceil(len(users) / entries_per_page)),
        'num_challenges_completed': {
            "username": request.user.username,
            "challenges_completed": UserChallenges.objects.filter(user=request.user).count()
        }
    }
    return render(request, 'project/leaderboard.html', context)


# Code by Henry
def registration(request):
    form = Signup(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = CustomUser.objects.get(username=form.cleaned_data.get('username'))
            profile_picture  = form.cleaned_data.get('profile_picture')
            user.profile_picture = profile_picture
            user.save()
            return redirect("login")
        else:
            print(form.errors)
            return render(request, 'project/registration.html', {'form': form})
    else:
        form = Signup()
        return render(request, 'project/registration.html', {'form': form})

# Code by Henry
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

# Code by Henry
@login_required()
def profile(request, username):
    if request.method == "POST":  
        profile_picture = request.POST.get('profile_picture')
        if profile_picture:
            user = request.user
            user.profile_picture = profile_picture
            user.save()
    user = get_object_or_404(CustomUser, username=username)
    user_challenges = UserChallenges.objects.filter(user=user)
    todays_challenge = DailyChallenge.objects.latest("-assigned")
    context = {
        'user': user,
        'user_challenges': user_challenges,
        'user_points': user_challenges.aggregate(Sum("points"))['points__sum']
    }
    return render(request, 'project/profile.html', context)


# Code by Elliot
@login_required()
def home(request):
    item = VillageShop.objects.get(item="Tree")
    print(item)
    todays_challenge = DailyChallenge.objects.all().order_by('-assigned')[0]
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
        # If user already completed daily challenge, they can resubmit 
        'already_completed_challenge': True if users_challenge else False
    }
    return render(request, 'home.html', context)

# Code by Henry
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

# Code by Ben
@login_required()
def gamekeeper(request):
    if request.method == 'POST':
        # Delete post
        if 'deleteButton' in request.POST:
            post_id = request.POST.get('post_id')
            post = UserChallenges.objects.get(id=post_id)
            post.delete()

        # Edit post
        elif 'editButton' in request.POST:
            post_id = request.POST.get('post_id')
            post = UserChallenges.objects.get(id=post_id)

            new_response = request.POST.get('response')
            post.response = new_response
            post.save()

        # Delete challenge
        elif 'challengeDelete' in request.POST:
            challenge_title = request.POST.get('challenge_title')
            challenge = Challenge.objects.get(title=challenge_title)
            print(f'Challenge {challenge_title} has been deleted')
            challenge.delete()

        # Edit challenge
        elif 'challengeEdit' in request.POST:
            edit_title = request.POST.get('edit_title')
            edit_description = request.get('edit_description')

            challenge_title = request.POST.get('challenge_title')

            challenge = Challenge.objects.get(title=challenge_title)
            challenge.title = edit_title
            challenge.description =edit_description

            challenge.save()


        # Submit new challenge
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

        # Assign new daily challenge
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
