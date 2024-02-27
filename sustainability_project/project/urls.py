from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('home/', views.home, name='home'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.user_login, name='login'),
    path('sample_profile/', views.sample_profile, name='sample_profile'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('make_post/', views.make_post, name='make_post'),

]
