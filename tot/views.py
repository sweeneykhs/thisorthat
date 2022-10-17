import re
from sre_constants import IN
from xml.dom.expatbuilder import theDOMImplementation
from django.shortcuts import redirect, render, HttpResponse
import pandas as pd
from tot.models import clothes, search_history, userChoice, theme, spec, items
from django.views.generic import ListView, CreateView, UpdateView
from .forms import *
from django.urls import reverse_lazy

import pandas as pd
import datetime as dt
import json
import csv
import pickle

import requests
import itertools
import time
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from .forms import InputForm, newSearchForm, theme_test
# from googletrans import Translator
# from google_trans_new import google_translator  
# translator = google_translator() 

from collections import Counter
import requests
from io import BytesIO
import statistics
from numpy.random import choice
import random


def table(request):
    df = pd.DataFrame(list(clothes.objects.all().values()))
    geeks_object = df.to_html()
  
        # parsing the DataFrame in json format.
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context = {'d': data}
  
    return render(request, 'table.html', context)



def set_up(request,clothes):
    clothes = pd.DataFrame(list(clothes.objects.all().values()))
    category_list=list(set(clothes.subcategory_eng))

    return clothes, category_list

def unique_words(request, category, df):
    temp=[]
    temp_df=df.loc[df.subcategory_eng==category]
    for i in temp_df['name_eng']:
        for j in i.split():
            temp.append(j)
    temp2=dict(Counter(temp))
    temp3=list(set(temp))
        
    return temp, temp2, temp3

def make_descr(request, category_list, df):
    cat_descr={}
    for i in category_list:
        cat_descr[i]=unique_words(request, i, df)
    return cat_descr

def explore_init(request, cat,cat_descr):
    cols=cat_descr[cat][2]
    init_value=5
    search_df=pd.DataFrame(columns=cols)
    data=[2]*(len(cols))
    search_df.loc[len(search_df)] = data
    return search_df

def generate_options(request, cat,search_df,df):
#     choice=1
    temp_df=df.loc[df.subcategory_eng==cat]
    temp_df['current_score']=temp_df['name_eng']
    for index, row in temp_df.iterrows():
        words=(row['name_eng']).split()
#         print(temp_df)
#         print(index)
        at_score=[]
#         words=temp_df['name_eng'][row]
#         print(words)
        for word in words :
#             print(search_df)
            at_score.append(search_df[word][len(search_df)-1])
#         print('AT',at_score)
        temp_df['current_score'][index]=statistics.mean(at_score)
#     print(temp_df)
    df_index=list(temp_df.index)
    weights=temp_df['current_score']
    total_weights=sum((weights))
    balanced_weights=[]
    for w in weights:
        balanced_weights.append(w/total_weights)
#     print(len(df_index), len(weights))
    options_index=np.random.choice(df_index, size=2, replace=False, p=balanced_weights)
    options=[]
#     for o in options_index:
#         print(o)
    options=temp_df.loc[options_index]
#     print(options)
    temp=[]
    for i in options.image_url:
        print(i)
        try:
            # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            # response = requests.get(str(i), headers=headers)
            # img = Image.open(BytesIO(response.content))
            # img        
            # temp.append(img)
            temp.append(i)
        except:
            pass

    return temp, options
        
        
#     print(search_df)
def make_choice(request, options, user_input, search_df):
#     user_input=int(input('Do you prefer 1 or 2?'))
    choice=user_input-1
    if choice==1:
        neg_choice=0
    else:
        neg_choice=1
    pos_words=options['name_eng'].values.flatten().tolist()[choice].split()
    neg_words=options['name_eng'].values.flatten().tolist()[neg_choice].split()
    print(pos_words)
    print(neg_words)
    search_df.loc[search_df.shape[0]] = [None]*len(search_df.columns)
    max_score=0
    max_limit=100000
    row = len(search_df)-1
#         print(search_df)
    for j in search_df.columns:
#             print(j)
        if j in pos_words:
            if search_df[j][row-1]>1:
                search_df[j][row]=pow(search_df[j][row-1],2)
            else:
                search_df[j][row]=search_df[j][row-1]*2
#             print('yes')
        elif j in neg_words:
            if search_df[j][row-1]>1:
                search_df[j][row]=pow(search_df[j][row-1], 0.5)
            else:
                search_df[j][row]=search_df[j][row-1]/2
        else:
            search_df[j][row]=pow(search_df[j][row-1], 1)
        # total_score=total_score+search_df[j][row]
        if search_df[j][row]>max_score:
            max_score=search_df[j][row]
    if max_score>max_limit:
        for j in search_df.columns:
            search_df[j][row]=search_df[j][row]/max_limit
    for j in search_df.columns:
        search_df[j][row]=search_df[j][row]/max_limit

#     print(search_df)
    return(search_df)

def make_search(request, pk,  *args, **kwargs):
    # df=pd.DataFrame(list(clothes.objects.all().values()))
    # df=set_up(request)[0]
    pk=pk
    df, category_list=set_up(request, clothes)
    search_all_info=search_history.objects.get(search_id=pk)
    cat=search_all_info.category
    cat_descr=make_descr(request, category_list, df)

    history=explore_init(request, cat, cat_descr)
    # try:
    #     user_input=userChoice.choice
    #     print(user_input)
    # except:
    #     user_input=1
   

    ims, options =generate_options(request, cat, history, df)
    # form = userChoice(request.POST)
    # if form.is_valid():
    #     form.save()
    # while counter<10: 
    #     ims, options =generate_options(request, cat, history, df)
    # #     print(ims[0])
    # #     for im in ims:
    # #         im
    #     user_input=int(input('Do you prefer 1 or 2?'))
    


    search_all_info=search_history.objects.get(search_id=pk)
    search_all_info.arguments=history
    search_all_info.save()
    search_df=search_all_info.arguments
    

    #     counter+=1
    context = {'d1': ims[0], 'd2': ims[1], 'cat':cat, 'form':InputForm, 'pk':pk, 'df':search_df}
    # print(options.image_url[0])

    if 'This' in request.POST:
        user_input=1
        search_all_info.choice=user_input
        search_all_info.options=options
        search_all_info.save()
        return redirect('search', pk)
    elif 'That' in request.POST:
        user_input=2
        search_all_info.choice=user_input
        search_all_info.options=options
        search_all_info.save()
        return redirect('search', pk)
    return render(request, 'table2.html', context)


def search_flow(request, pk, *args, **kwargs):
    search_all_info=search_history.objects.get(search_id=pk)
    user_input=search_all_info.choice
    print(user_input)
    options=search_all_info.options
    history=search_all_info.arguments
    history=make_choice(request, options, user_input, history)
    
    pk=pk
    df, category_list=set_up(request, clothes)
    cat=search_all_info.category
    cat_descr=make_descr(request, category_list, df)
    ims, options =generate_options(request, cat, history, df)
    search_all_info.arguments=history
    search_all_info.save()
    search_df=search_all_info.arguments
   
    # scores=search_df.iloc[: , 1:]
    # scores=pd.to_numeric(scores[:,:])
    # best=scores.idxmax()
    # worst=scores.idxmin()
    context = {'d1': ims[0], 'd2': ims[1], 'cat':cat, 'form':InputForm, 'pk':pk, 'df':search_df}
    # print(options.image_url[0])

    if 'Option 1' in request.POST:
        user_input=1
        return redirect('search', pk)
    elif 'Option 2' in request.POST:
        user_input=2
        return redirect('search', pk)
    return render(request, 'table2.html', context)
    
    
    
    
    
    
    return


def NewSearch(request):
    # model = search_history
    form_class = newSearchForm()
    df, cats=set_up (request, clothes)

    if request.method=='POST':
        form_class= newSearchForm(request.POST)
        # category = request.POST.get('category')
        # form_class.fields['category'].choices = [(category, category)]
        if form_class.is_valid():
            search_history=form_class.save(commit=False)
            search_history.save()
            context={'pk':search_history.search_id}
            return redirect('pls', search_history.search_id)

    context={'form':form_class, 'cats':cats}
    return render(request, 'new_search.html', context)

# def index(request):
#     form_class=spec_test()
#     query_results = clothes.objects.values_list("subcategory_eng", flat=True).distinct()
#     spec_list = spec_test()
#     if request.method=='POST':
#         form_class= spec_test(request.POST)
#         search_history=form_class.save(commit=False)
#         search_history.save()
#         context={'pk':search_history.search_id}
#         return redirect('pls', search_history.search_id)

#     context = {
#         'query_results': query_results,
#         'location_list': spec_list,

#     }
#     return render(request,'index.html', context)

# def load_themes(request):
#     themes_id = request.GET.get('theme')
#     themes = theme.objects.filter(theme_id=themes_id).order_by('name')
#     return render(request, 'hr/city_dropdown_list_options.html', {'themes': themes})

# Create your views here.
def choosetheme(request):
   form = theme_test(request.POST)
   if request.method == "POST":
      form = theme_test(request.POST)
      if form.is_valid:
         #redirect to the url where you'll process the input
         return redirect('new') # insert reverse or url
   errors = form.errors or None # form not submitted or it has errors
   return render(request, 'theme_select.html',{
          'form': form,
          'errors': errors,
   })