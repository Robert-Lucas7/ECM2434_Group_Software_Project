from .models import Challenge, DailyChallenge
import random 
import django

DONT_REPEAT = 6

def get_new_daily_challenge():
    recent_daily_challenges = DailyChallenge.objects.all().order_by('-assigned')[:DONT_REPEAT + 1].values_list('challenge',flat=True)
    already_done_challenges = Challenge.objects.filter(pk__in=recent_daily_challenges)
    possible_challenges = Challenge.objects.all().difference(already_done_challenges)
    random_challenge = random.choice(possible_challenges)
    new_daily_challenge = DailyChallenge(challenge=random_challenge, assigned = django.utils.timezone.now())
    new_daily_challenge.save()
    print(f"{new_daily_challenge.assigned.strftime('%Y-%m-%d %H:%M:%S')}: {new_daily_challenge.challenge.title}")
