from .models import Challenge, ChallengesAssigned
import random 
import datetime

def get_new_daily_challenge():
    print("=== STARTING CRON ===")
    all_challenges = list(Challenge.objects.all())
    random_challenge = random.choice(all_challenges)
    new_daily_challenge = ChallengesAssigned(challenge=random_challenge, date_assigned = datetime.datetime.today())
    new_daily_challenge.save()
    print(f"{new_daily_challenge.date_assigned.strftime('%Y-%m-%d')}: {new_daily_challenge.challenge.title}")
    print("=== ENDING CRON ===")
