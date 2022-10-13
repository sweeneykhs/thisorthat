from dataclasses import field
from unicodedata import category
from django import forms
from .models import clothes, userChoice, search_history
import pandas as pd
import uuid
from django_select2 import forms as s2forms
   
# creating a form 
class InputForm(forms.ModelForm):

    class Meta:
        model = userChoice
        fields="__all__"

    # user_input = forms.IntegerField(help_text = "Do you prefer 1 or 2?")
    # first_name = forms.CharField(max_length = 200)
    # last_name = forms.CharField(max_length = 200)
    # roll_number = forms.IntegerField(
    #                  help_text = "Enter 6 digit roll number"
    #                  )
    # password = forms.CharField(widget = forms.PasswordInput())


theme_=['Clothes']
specifics_=['Womens']
# df = pd.DataFrame(list(clothes.objects.all().values()))
# clothes = pd.DataFrame(list(clothes.objects.all().values()))
# name_=list(set(clothes.subcategory_eng))

class newSearchForm(forms.ModelForm):
    class Meta:
        model = search_history
        fields = ('category',)
        # exclude=('arguments',)
        # theme = forms.ModelChoiceField(label="theme", queryset=clothes.objects.all().values())
    #     theme=forms.CharField(widget=forms.Select(choices=theme_))
    #     specifics=forms.CharField(widget=forms.Select(choices=specifics_))
    #     name=forms.CharField(widget=forms.Select(choices=name_))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class theme_test(forms.Form):
     themes = forms.ModelChoiceField(queryset=clothes.objects.all().order_by('theme'))
    # days = forms.ModelChoiceField(queryset=clothes.objects.all().values())
