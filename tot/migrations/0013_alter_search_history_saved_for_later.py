# Generated by Django 4.1.2 on 2022-10-18 04:05

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tot', '0012_alter_search_history_saved_for_later'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search_history',
            name='saved_for_later',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300, null=True), blank=True, default=list, size=None),
        ),
    ]
