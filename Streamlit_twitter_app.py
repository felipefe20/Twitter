import streamlit as st
import pandas as pd
import numpy as np
# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
import tweepy   
from credentials import *
import requests
from datetime import date
from datetime import timedelta
import re

#Plotly
import plotly.graph_objects as go
from st_aggrid import AgGrid


#Keys to fetch twitter data
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET_KEY)
api = tweepy.API(auth)

#Title and functions 
st.title('Twitter Sentiment Analysis')

def run_query(query, num_tweets):
    #query = f"{hashtag} -filter:retweets until:2022-02-25 since:2022-02-24"
    #tweets= tweepy.Cursor(api.search_tweets, query,count=num_tweets, lang='en').items(10000)

    tweets = api.search_tweets(q=query, lang="en",count=num_tweets)

    my_list_of_dicts = []
    for each_json_tweet in tweets:
        my_list_of_dicts.append(each_json_tweet._json)
        
    #with open('Arsenat_hashtag.txt', 'w') as file:
    #    file.write(json.dumps(my_list_of_dicts, indent=4))

    query_df=pd.json_normalize(my_list_of_dicts)


    return query_df



#Capturing info from user on sidebar
words=st.sidebar.text_input('Words separated by space', 'Arsenal best')

hashtag = st.sidebar.text_input('Hashtag', '#Arsenal')
num_tweets = st.sidebar.number_input('Num_tweets', 10)
RT_condition=st.sidebar.radio("Fetch RT?:",(False, True))
User_from=st.sidebar.text_input('User_from', '')
User_to=st.sidebar.text_input('User_to', '')
#Date input
Since = st.sidebar.date_input(
     "Date:",
     date.today() - timedelta(days = 7),
     min_value=date.today() - timedelta(days = 7),
     max_value=date.today())
Until = Since+ timedelta(days = 1)
Since=str(Since)
Until = str(Until)


#Slicer for time_range
#time_range = st.slider(
#     "Time of query in Colombia local time:",
#     value=(datetime.time(00, 00), datetime.time(12, 00)))


def check_blank_spaces(words, hashtag,User_from, User_to):
    if len(words)==0 and len(hashtag)==0 and len(User_from)==0 and len(User_to)==0:
        st.write("Any of these should be not blank: Words, Hashtag, User From, User To")
        return False
    else: 
        st.write("Query is succesful")
        return True


def create_query(words, hashtag, RT_condition, User_from, User_to, Since, Until):

    query=hashtag+" "+ words

    if len(User_from)!=0:
        query=query+" from:"+User_from

    if len(User_to)!=0:
        query=query+" to:"+User_to

    if len(Since)!=0:
        query=query+" since:"+Since

    if len(Until)!=0:
        query=query+" until:"+Until
    if RT_condition==False:
        query=query+" -filter:retweets"
    return query
    

if st.button('Run query'):
    
    if check_blank_spaces(words, hashtag,User_from, User_to):
        query=create_query(words, hashtag, RT_condition, User_from, User_to, Since, Until)
        st.write("Your query is:", query)
        st.write("and Total tweets:", num_tweets)

        query_df=run_query(query, num_tweets)
        try:
            query_df=query_df[["created_at","text","retweet_count","favorite_count","user.screen_name"
                                ,"user.verified","user.followers_count",
                                "user.friends_count","user.listed_count","user.location","user.description"
                                ,"user.favourites_count","user.statuses_count"]]
            #pass
        except:
            pass

        st.write(query_df, width=3000)
        #AgGrid(query_df)
    else: 
        st.write("Check your query")
    

#Sentiment Analysis using Spacy and transformers



#Most popular hashtags and mentions

def extract_hashtags(df):
    list=df["text"].to_list()
    allwords=" ".join([tweet for tweet in list]).lower()

    hashtags=re.findall(r"[#]\w+", allwords)

    hashtags_df=pd.Series(hashtags).value_counts().to_frame().reset_index().rename(columns={"index":"Hashtag",0:"Count_Hashtag"})

    return hashtags_df

def extract_mentions(df):
    list=df["text"].to_list()
    allwords=" ".join([tweet for tweet in list]).lower()

    mentions=re.findall(r"[@]\w+", allwords)

    mentions_df=pd.Series(mentions).value_counts().to_frame().reset_index().rename(columns={"index":"User",0:"Count_Mentions"})

    return mentions_df


hashtags_df=extract_hashtags(query_df)
mentions_df=extract_mentions(query_df)



import streamlit as st
from bokeh.plotting import figure

col1, col2= st.columns(2)


p = figure(title="Hashtags frequency", x_range=hashtags_df["Hashtag"], 
            tools="hover", tooltips=[('Count', '@$name')])

p.vbar(x=hashtags_df["Hashtag"], top=hashtags_df["Count_Hashtag"], width=0.9
        )

p.xgrid.grid_line_color = None
p.y_range.start = 0
p.xaxis.major_label_orientation = "vertical"
with col1:
    st.bokeh_chart(p, use_container_width=True)


m = figure(title="Mentions frequency", x_range=mentions_df["User"], tools="hover", tooltips="@$name")

m.vbar(x=mentions_df["User"], top=mentions_df["Count_Mentions"], width=0.9
        )

m.xgrid.grid_line_color = None
m.y_range.start = 0
m.xaxis.major_label_orientation = "vertical"

with col2:
    st.bokeh_chart(m, use_container_width=True)








#Agregar filtro de sentimiento positivo o negativo