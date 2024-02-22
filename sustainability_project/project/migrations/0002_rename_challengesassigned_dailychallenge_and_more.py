# Generated by Django 5.0.1 on 2024-02-22 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChallengesAssigned',
            new_name='DailyChallenge',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='info',
        ),
        migrations.RemoveField(
            model_name='userchallenges',
            name='challenge',
        ),
        migrations.RemoveField(
            model_name='userchallenges',
            name='date',
        ),
        migrations.AddField(
            model_name='challenge',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='challenge',
            name='location_lat',
            field=models.DecimalField(decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='challenge',
            name='location_long',
            field=models.DecimalField(decimal_places=8, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userchallenges',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userchallenges',
            name='daily_challenge',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='project.dailychallenge'),
        ),
        migrations.AddField(
            model_name='userchallenges',
            name='response',
            field=models.CharField(default=None, max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userchallenges',
            name='submitted',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
    ]
