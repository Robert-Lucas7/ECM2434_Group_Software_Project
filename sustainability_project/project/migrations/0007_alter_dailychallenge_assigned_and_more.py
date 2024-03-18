# Generated by Django 5.0.1 on 2024-03-18 22:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0006_villageshop_alter_dailychallenge_assigned_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dailychallenge",
            name="assigned",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 22, 37, 28, 285466, tzinfo=datetime.timezone.utc
                ),
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userchallenges",
            name="submitted",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 22, 37, 28, 285660, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="village",
            name="purchased",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 3, 18, 22, 37, 28, 285022, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
