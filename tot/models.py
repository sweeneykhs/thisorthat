from secrets import choice
from tkinter import CASCADE
from unicodedata import category
from django.db import models
import pandas as pd
import datetime
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
import uuid

from requests import options 


# Create your models here.
class clothes(models.Model):
    name_eng=models.CharField(("name_eng"), max_length=2000)	
    image_url=models.CharField(("image_url"), max_length=2000)
    subcategory_eng=models.CharField(("subcategory_eng"), max_length=2000)
    theme=models.CharField(("theme"), max_length=2000, null=True)
    spec=models.CharField(("spec"), max_length=2000, null=True)

class userChoice(models.Model):
    choice=models.IntegerField()
    # user=models.ForeignKey(User, on_delete=CASCADE)


theme_=['Clothes']
specifics_=['Womens']
df = pd.DataFrame(list(clothes.objects.all().values()))
clothes_ = pd.DataFrame(list(clothes.objects.all().values()))
name_=list(set(clothes_.subcategory_eng))
# print(name_)

class search_history(models.Model):
    theme=models.CharField(max_length=300)
    spec=models.CharField(max_length=300)
    category=models.CharField(max_length=300)
    arguments=PickledObjectField(null=True)
    choice=models.IntegerField(null=True)
    options=PickledObjectField(null=True)
    # id = models.BigIntegerField(primary_key=True)
    search_id = models.UUIDField( default=uuid.uuid4, editable=False, primary_key=True)
    def __str__(self):
        return self.arguments


class theme(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class spec(models.Model):
    theme = models.ForeignKey(theme, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class items(models.Model):
    name = models.CharField(max_length=100)
    theme = models.ForeignKey(theme, on_delete=models.SET_NULL, null=True)
    spec = models.ForeignKey(spec, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name