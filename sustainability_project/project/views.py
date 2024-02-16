from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect

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
                print("user logged in successfully")
                login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    print("Login Failed")
    return render(request, 'login.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(CustomUser,
                             pk=username)  # Should prevent SQL injection as django queries are parameterized.
    user_challenges = UserChallenges.objects.filter(user=user)
    todays_challenge = ChallengesAssigned.objects.latest("date_assigned")
    print(todays_challenge.challenge)
    context = {
        'user': user,
        'user_challenges': user_challenges,
        'todays_challenge': todays_challenge.challenge
    }
    return render(request, 'project/profile.html', context)
