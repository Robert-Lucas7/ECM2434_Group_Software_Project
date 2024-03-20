from .models import Challenge, DailyChallenge
import random 
import django

DONT_REPEAT = 7

def get_new_daily_challenge():
    print("=== STARTING CRON ===")
    recent_daily_challenges = DailyChallenge.objects.all().order_by('assigned')[:DONT_REPEAT + 1].values_list('challenge',flat=True)
    possible_challenges = Challenge.objects.filter(pk__in=recent_daily_challenges)

    random_challenge = random.choice(possible_challenges)
    new_daily_challenge = DailyChallenge(challenge=random_challenge, assigned = django.utils.timezone.now())
    new_daily_challenge.save()
    print(f"{new_daily_challenge.assigned.strftime('%Y-%m-%d')}: {new_daily_challenge.challenge.title}")
    print("=== ENDING CRON ===")
