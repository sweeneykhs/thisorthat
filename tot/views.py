from errno import ESTALE
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
from .forms import InputForm, newSearchForm_category,newSearchForm_theme
# from googletrans import Translator
# from google_trans_new import google_translator  
# translator = google_translator() 

from collections import Counter
import requests
from io import BytesIO
import statistics
from numpy.random import choice
import random


# def table(request):
#     df = pd.DataFrame(list(clothes.objects.all().values()).iterator())
#     geeks_object = df.to_html()
  
#         # parsing the DataFrame in json format.
#     json_records = df.reset_index().to_json(orient ='records')
#     data = []
#     data = json.loads(json_records)
#     context = {'d': data}
  
#     return render(request, 'table.html', context)



def set_up(request,clothes):
    clothes = pd.DataFrame(list(clothes.objects.all().values().iterator()))
    category_list=list(set(clothes.subcategory_eng))

    return clothes, category_list

def unique_words(request, category, df):
    temp=[]
    # temp_df=df.loc[df.subcategory_eng==category]
    # print(temp_df)
    for i in df['description']:
        try:
            for j in i.split(", "):
                temp.append(j)
        except:
            pass
    temp2=dict(Counter(temp))
    temp3=list(set(temp))
        
    return temp, temp2, temp3

def make_descr(request, category_list, df):
    cat_descr={}
    for i in category_list:
        cat_descr[i]=unique_words(request, i, df)
        # print(cat_descr)
    return cat_descr

def explore_init(request, cat,cat_descr, df):
    # all_data=pd.DataFrame(clothes.objects.all().values().iterator())
    # print(all_data)
    # cat_data=all_data.loc[all_data['subcategory_eng']==cat]
    # Makes the description DF
    cols=cat_descr[cat][2]
    init_value=5
    search_df=pd.DataFrame(columns=cols)
    data=[init_value]*(len(cols))
    search_df.loc[len(search_df)] = data
    # Makes the colour DF
    colours=list(set(df.colour))
    init_value=5
    colour_df=pd.DataFrame(columns=colours)
    colour_data=[init_value]*(len(colours))
    colour_df.loc[len(colour_df)] = colour_data
    # Makes the colour DF
    brands=list(set(df.brand))
    init_value=5
    brand_df=pd.DataFrame(columns=brands)
    brand_data=[init_value]*(len(brands))
    brand_df.loc[len(brand_df)] = brand_data
    # print(brand_df)
    return search_df, colour_df, brand_df


def generate_options(request, cat,search_df, colour_df, brand_df, df, pk):
#     choice=1
    
    df['current_score']=df['name_eng']
    df['current_score_colour']=df['name_eng']
    df['current_score_brand']=df['name_eng']
    df['combined_score']=df['name_eng']
    for index, row in df.iterrows():
        
        try:
            words=(row['description']).split(", ")
            at_score=[]
        # print(search_df)
            for word in words :
            # print(word)
                at_score.append(search_df[word][len(search_df)-1])
        except:
            at_score=[0]
        df['current_score'][index]=statistics.mean(at_score)
        df['current_score_colour'][index]=colour_df[row['colour']][len(colour_df)-1]
        df['current_score_brand'][index]=brand_df[row['brand']][len(brand_df)-1]
#     print(temp_df)
    df_index=list(df.index)
    
    # for i in range(0,len(temp_df['current_score_brand'])):
    #     temp_df['combined_score'][i]=temp_df['current_score'][i]+temp_df['current_score_colour'][i]+temp_df['current_score_brand'][i]
    desc_weights=df['current_score']
    desc_total_weights=sum((desc_weights))
    desc_balanced_weights=[]
    for w in desc_weights:
        desc_balanced_weights.append(w/desc_total_weights)
    colour_weights=df['current_score_colour']
    colour_total_weights=sum((colour_weights))
    colour_balanced_weights=[]
    for w in colour_weights:
        colour_balanced_weights.append(w/colour_total_weights)
    brand_weights=df['current_score_brand']
    brand_total_weights=sum((brand_weights))
    brand_balanced_weights=[]
    for w in brand_weights:
        brand_balanced_weights.append(w/brand_total_weights)
    balanced_weights=[]
    brand_multiplier=0.1
    for i in range(0, len(desc_balanced_weights)):
        balanced_weights.append(desc_balanced_weights[i]+colour_balanced_weights[i]+(brand_balanced_weights[i]*brand_multiplier))
    total_balanced_weights=sum(balanced_weights)
    df['combined_score']=balanced_weights
    probs=[]
    for i in balanced_weights:
        # print(i, total_balanced_weights)
        try:
            probs.append(i/total_balanced_weights)
        except:
            probs.append(0)
            print(i)
#     print(len(df_index), len(weights))
    options_index=np.random.choice(df_index, size=2, replace=False, p=probs)
    options=[]
#     for o in options_index:
#         print(o)
    options=df.loc[options_index]
    search_all_info=search_history.objects.get(search_id=pk)
    search_all_info.options=options
    search_all_info.save
    print('Generate Options', options)
    for i in options.combined_score:
        try:
            print(i/total_balanced_weights)
        except:
            print(i)
    temp=[]
    temp2=[]
    for i in options.image_url:
        try:
            temp.append(i)
        except:
            pass
    for i in options.product_url:
        try:
            # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            # response = requests.get(str(i), headers=headers)
            # img = Image.open(BytesIO(response.content))
            # img        
            # temp.append(img)
            # print(i)
            temp2.append(i)
        except:
            pass

    return temp, options, temp2
        
        
#     print(search_df)
def make_choice(request, options, user_input, search_df, colour_df, brand_df):
#     user_input=int(input('Do you prefer 1 or 2?'))
    # print(search_df, '1')
    choice=user_input-1
    if choice==1:
        neg_choice=0
    else:
        neg_choice=1
    # this does the descirptions
    try:
        pos_words=options['description'].values.flatten().tolist()[choice].split(", ")
    except:
        pos_words=""
    try:
        neg_words=options['description'].values.flatten().tolist()[neg_choice].split(", ")
    except:
        neg_words=""
    # print(pos_words)
    # print(neg_words)
    search_df.loc[search_df.shape[0]] = [None]*len(search_df.columns)
    # print(search_df, '2')
    brand_df.loc[brand_df.shape[0]] = [None]*len(brand_df.columns)
    colour_df.loc[colour_df.shape[0]] = [None]*len(colour_df.columns)
    max_score=0
    max_limit=10000
    row = len(search_df)-1
#         print(search_df)
    # print(search_df, brand_df)
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
                search_df[j][row]=pow(search_df[j][row-1], 0.75)
            else:
                search_df[j][row]=search_df[j][row-1]/2
        else:
            search_df[j][row]=search_df[j][row-1]*1.5 
        if search_df[j][row]>max_score:
            max_score=search_df[j][row]
    if max_score>max_limit:
        for j in search_df.columns:
            # print(max_score)
            search_df[j][row]=search_df[j][row]/1000
    # print(search_df, '3')

    # This does the brands
    max_score_brand=0
    pos_brand=options['brand'].values.flatten().tolist()[choice]
    neg_brand=options['brand'].values.flatten().tolist()[neg_choice]
    # print(brand_df.columns)
    for brand in brand_df.columns:
        if brand==pos_brand:
            if brand_df[brand][row-1]>1:
                brand_df[brand][row]=pow(brand_df[brand][row-1],2)
            else:
                brand_df[brand][row]=brand_df[brand][row-1]*2
        elif brand==neg_brand:
            if brand_df[brand][row-1]>1:
                brand_df[brand][row]=pow(brand_df[brand][row-1],0.75)
            else:
                brand_df[brand][row]=brand_df[brand][row-1]/2
        else:
            brand_df[brand][row]=brand_df[brand][row-1]*1.5
        if brand_df[brand][row]>max_score_brand:
            max_score_brand=brand_df[brand][row]
    if max_score_brand>max_limit:
        for brand in brand_df.columns:
            # print(max_score)
            brand_df[brand][row]=brand_df[brand][row]/1000
    ## This does the colours
    max_score_colour=0
    pos_colour=options['colour'].values.flatten().tolist()[choice]
    neg_colour=options['colour'].values.flatten().tolist()[neg_choice]
    for colour in colour_df.columns:
        if colour==pos_colour:
            if colour_df[colour][row-1]>1:
                colour_df[colour][row]=pow(colour_df[colour][row-1],2)
            else:
                colour_df[colour][row]=colour_df[colour][row-1]*2
        elif colour==neg_colour:
            if colour_df[colour][row-1]>1:
                colour_df[colour][row]=pow(colour_df[colour][row-1],0.75)
            else:
                colour_df[colour][row]=colour_df[colour][row-1]/2
        else:
            colour_df[colour][row]=colour_df[colour][row-1]*1.1
        if colour_df[colour][row]>max_score_colour:
            max_score_colour=colour_df[colour][row]     
    if max_score_colour>max_limit:
        for colour in colour_df.columns:
            # print(max_score)
            colour_df[colour][row]=colour_df[colour][row]/1000
   
    print(search_df, colour_df, brand_df)
    # print(test_df, '5')
    return(search_df, colour_df, brand_df)

def make_search(request, pk,  *args, **kwargs):

    pk=pk
    # df, category_list=set_up(request, clothes)
    # df= pd.read_json(request.session.get('df'))
    category_list= request.session.get('category_list')

    search_all_info=search_history.objects.get(search_id=pk)
    df=search_all_info.df
    cat=search_all_info.category
    cat_descr=make_descr(request, category_list, df)

    history, colour_df, brand_df=explore_init(request, cat, cat_descr, df)
    # print(history)

    ims, options, urls =generate_options(request, cat, history, colour_df, brand_df, df, pk)
    # print(urls)
    


    search_all_info=search_history.objects.get(search_id=pk)
    search_all_info.arguments=history
    search_all_info.arguments_colour=colour_df
    search_all_info.arguments_brand=brand_df
    
    search_df=search_all_info.arguments
    search_all_info.save()
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
    elif 'saveThis' in request.POST:
        user_input=1
        search_all_info.choice=user_input
        search_all_info.options=options
        search_all_info.saved_for_later.append(ims[0])
        search_all_info.saved_for_later_urls.append(urls[0])
        search_all_info.save()
        return redirect('search', pk)
    elif 'saveThat' in request.POST:
        user_input=2
        search_all_info.choice=user_input
        search_all_info.options=options
        search_all_info.saved_for_later.append(ims[1])
        search_all_info.saved_for_later_urls.append(urls[1])
        search_all_info.save()
        return redirect('search', pk)
    return render(request, 'search1.html', context)


def search_flow(request, pk, *args, **kwargs):
    search_all_info=search_history.objects.get(search_id=pk)
    user_input=search_all_info.choice
    
    options=search_all_info.options
    # print(options)
    history=search_all_info.arguments
    colour_df=search_all_info.arguments_colour
    brand_df=search_all_info.arguments_brand
    # print("HISTORY",history, colour_df)
    history, colour_df, brand_df=make_choice(request, options, user_input, history, colour_df, brand_df)
    print(history)
    pk=pk
    # df, category_list=set_up(request, clothes)
    df=search_all_info.df
    # category_list= request.session.get('category_list')
    cat=search_all_info.category
    ims, options, urls =generate_options(request, cat, history, colour_df, brand_df, df, pk)
    # print(urls)
    search_all_info.arguments=history
    search_all_info.arguments_colour=colour_df
    search_all_info.arguments_brand=brand_df
    search_all_info.options=options
    search_all_info.save()
    search_df=search_all_info.arguments
    # print(search_all_info.saved_for_later_urls)
    # scores=search_df.iloc[: , 1:]Flanker27
    # scores=pd.to_numeric(scores[:,:])
    # best=scores.idxmax()
    # worst=scores.idxmin()
    context = {'d1': ims[0], 'd2': ims[1], 'cat':cat, 'form':InputForm, 'pk':pk, 'df':search_df}
    # print(options.image_url[0])
    if 'saved_items' in request.POST:
        saves=search_all_info.saved_for_later
        saves_url=search_all_info.saved_for_later_urls

        context={'pk': pk, 'saves': saves,'saves_url': saves_url}
        return render(request, 'saved_items.html', context)
    else:
        if 'Option 1' in request.POST:
            user_input=1
            search_all_info.options=options
            search_all_info.save()
            return redirect('search', pk)
        elif 'Option 2' in request.POST:
            user_input=2
            search_all_info.options=options
            search_all_info.save()
            return redirect('search', pk)
        elif 'saveThis' in request.POST:
            user_input=1
            search_all_info.choice=user_input
            search_all_info.options=options
            search_all_info.saved_for_later.append(ims[0])
            search_all_info.saved_for_later_urls.append(urls[0])
            search_all_info.save()
        elif 'saveThat' in request.POST:
            user_input=2
            search_all_info.choice=user_input
            search_all_info.options=options
            search_all_info.saved_for_later.append(ims[1])
            search_all_info.saved_for_later_urls.append(urls[1])
            search_all_info.save()
        # print(search_all_info.saved_for_later)
        # print(search_df)
        return render(request, 'table2.html', context)


def NewSearch(request):
    # model = search_history
    form_class = newSearchForm_category()
    df, category_list=set_up (request, clothes)
    # request.session['df'] = df.to_json()
    request.session['category_list'] = category_list

    if request.method=='POST':
        form_class= newSearchForm_category(request.POST)
        # category = request.POST.get('category')
        # form_class.fields['category'].choices = [(category, category)]
        if form_class.is_valid():
            search_history=form_class.save(commit=False)
            cat=search_history.category
            search_history.df=df.loc[df.subcategory_eng==cat]
            search_history.save()
            context={'pk':search_history.search_id}
            return redirect('pls', search_history.search_id)

    context={'form':form_class, 'cats':category_list, 'df':df}
    return render(request, 'new_search.html', context)

def NewSearch_theme(request):
    # model = search_history
    form_class = newSearchForm_theme()
    # df, cats=set_up (request, clothes)
    themes=['Fashion']
    if request.method=='POST':
        form_class= newSearchForm_theme(request.POST)
        # category = request.POST.get('category')
        # form_class.fields['category'].choices = [(category, category)]
        if form_class.is_valid():
            search_history=form_class.save(commit=False)
            search_history.save()
            context={'pk':search_history.search_id}
            pk=search_history.search_id
            return redirect('new_spec', pk)

    context={'form':form_class, 'cats':themes}
    return render(request, 'new_search.html', context)

def NewSearch_spec(request, pk,  *args, **kwargs):
    # model = search_history
    form_class = newSearchForm_spec()
    # df, cats=set_up (request, clothes)
    themes=['Fashion']
    if request.method=='POST':
        form_class= newSearchForm_spec(request.POST)
        # category = request.POST.get('category')
        # form_class.fields['category'].choices = [(category, category)]
        if form_class.is_valid():
            search_history=form_class.save(commit=False)
            search_history.save()
            context={'pk':search_history.search_id}
            return redirect('pls', search_history.search_id,)

    context={'form':form_class, 'cats':themes, 'pk':search_history.search_id}
    return render(request, 'new_search.html', context)

def saved_items(request, pk, *args, **kwargs):
    search_all_info=search_history.objects.get(search_id=pk)
    saves=search_all_info.saved_for_later
    context = {'pk':pk, 'saves':saves}
    return render(request, 'saved_items.html', context)