# Generated by Django 4.1.2 on 2022-10-18 00:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tot', '0009_search_history_saved_for_later'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchoice',
            name='saved',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='search_history',
            name='saved_for_later',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), null=True, size=None),
        ),
    ]
