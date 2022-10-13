# Generated by Django 4.1.2 on 2022-10-13 04:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tot', '0007_remove_specs_theme_delete_items_delete_specs_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='spec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tot.theme')),
            ],
        ),
        migrations.CreateModel(
            name='items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('spec', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tot.spec')),
                ('theme', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tot.theme')),
            ],
        ),
    ]