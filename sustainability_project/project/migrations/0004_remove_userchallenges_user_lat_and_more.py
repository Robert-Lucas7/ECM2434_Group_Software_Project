# Generated by Django 5.0.1 on 2024-03-18 11:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0003_alter_dailychallenge_assigned_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailychallenge",
            name="assigned",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 11, 58, 4, 403464, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userchallenges",
            name="submitted",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 11, 58, 4, 403665, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
