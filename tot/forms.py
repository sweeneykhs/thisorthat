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

class newSearchForm_category(forms.ModelForm):
    iquery=clothes.objects.values_list("subcategory_eng", flat=True).distinct()
    iquery_choices=[('', 'None')] + [(id, id) for id in iquery]
    category=forms.ChoiceField(choices=iquery_choices,required=False, widget=forms.Select())
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

class newSearchForm_theme(forms.ModelForm):
    iquery=clothes.objects.values_list("theme", flat=True).distinct()
    iquery_choices=[('', 'None')] + [(id, id) for id in iquery]
    theme=forms.ChoiceField(choices=iquery_choices,required=False, widget=forms.Select())
    class Meta:
        model = search_history
        fields = ('theme',)
        
        # exclude=('arguments',)
        # theme = forms.ModelChoiceField(label="theme", queryset=clothes.objects.all().values())
    #     theme=forms.CharField(widget=forms.Select(choices=theme_))
    #     specifics=forms.CharField(widget=forms.Select(choices=specifics_))
    #     name=forms.CharField(widget=forms.Select(choices=name_))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class newSearchForm_spec(forms.Form):

    spec=forms.ModelChoiceField(queryset=search_history.objects.none())
    # class Meta:
    #     model = search_history
    #     fields = ('spec',)
        
    def __init__(self, *args, **kwargs):
        self.search_pk = kwargs.pop('pk')
        super(newSearchForm_spec, self).__init__(*args, **kwargs)
        search_theme=search_history.objects.get(search_id=self.search_pk).theme
        self.fields['spec'].queryset = clothes.filter(theme=search_theme)