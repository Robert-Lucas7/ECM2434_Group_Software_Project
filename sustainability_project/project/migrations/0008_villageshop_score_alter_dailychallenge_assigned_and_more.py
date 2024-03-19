# Generated by Django 4.2.9 on 2024-03-19 13:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_rename_item_number_village_position_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='villageshop',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dailychallenge',
            name='assigned',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 13, 4, 1, 829302, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='userchallenges',
            name='submitted',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 13, 4, 1, 829302, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='village',
            name='purchased',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 19, 13, 4, 1, 829302, tzinfo=datetime.timezone.utc)),
        ),
    ]
