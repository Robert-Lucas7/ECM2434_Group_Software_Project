# Generated by Django 5.0.1 on 2024-03-18 11:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0004_remove_userchallenges_user_lat_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userchallenges",
            name="user_lat",
            field=models.DecimalField(decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name="dailychallenge",
            name="assigned",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 11, 58, 19, 1459, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userchallenges",
            name="submitted",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 11, 58, 19, 1669, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
