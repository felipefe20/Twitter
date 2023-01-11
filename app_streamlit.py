import streamlit as st
import pandas as pd
import numpy as np
#from streamlit_autorefresh import st_autorefresh
from math import floor
import snscrape.modules.twitter as sntwitter
import pandas as pd
from tqdm import tqdm
import datetime
#from datetime import datetime, timedelta
st.set_page_config(layout="wide")

def search_twitter(all_words=False, exact_phrase="", any_words="", exclude_words="",hashtags="",
                    from_account="", to_account="", mention_account="",
                    exclude_replies=False, exclude_retweets=False, min_replies=False, min_likes=False, min_retweets=False,
                    start_date=False, end_date=False):

    any_words=any_words.replace(","," OR ")
    
    #Hashtags with # and separated by comma
    hashtags=hashtags.replace(" ","")
    hashtags=hashtags.replace(",", " OR ")
    
    from_account=from_account.replace(" ","")
    from_account=from_account.replace("@","from:").replace(","," OR ")

    to_account=to_account.replace(" ","")
    to_account=to_account.replace("@","to:").replace(","," OR ")
    
    mention_account=mention_account.replace(" ","")
    mention_account=mention_account.replace(",", " OR ")

    #until=until:2022-12-03 
    #since=since:2022-11-30
    
    query_list = [
            #query_terms,
            all_words if all_words else "",
            f"'{exact_phrase}'" if exact_phrase else "",
            f"({any_words})" if any_words else "",
            f"-{exclude_words}" if exclude_words else "",
            f"({hashtags})" if hashtags else "",
            f"({from_account})" if from_account else "",
            f"({to_account})" if to_account else "",
            f"({mention_account})" if mention_account else "",
            f"since:{start_date}" if start_date else "",
            f"until:{end_date}" if end_date else "",
            "-filter:replies" if exclude_replies else "",
            "-filter:nativeretweets" if exclude_retweets else "",
            f"min_replies:{min_replies}" if min_replies else "",
            f"min_faves:{min_likes}" if min_likes else "",
            f"min_retweets:{min_retweets}" if min_retweets else "",
            "lang:en"
                ]
    
    query_str = " ".join(query_list)

    return query_str

def get_twitter_df(query):
    id_tweet=[]
    nick_name=[]
    user=[]
    tweets=[]
    time=[]
    likes=[]
    retweets=[]
    link=[]
    replies=[]
    lang=[]
    
    count=1

    for tweet in tqdm(sntwitter.TwitterSearchScraper(query).get_items()): 
        id_tweet.append(tweet.id)
        nick_name.append(tweet.user.displayname)
        user.append(tweet.user.username)
        tweets.append(tweet.content)
        time.append(tweet.date.replace(tzinfo=None))
        likes.append(tweet.likeCount)
        retweets.append(tweet.retweetCount)
        replies.append(tweet.replyCount)
        link.append(tweet.url)
        lang.append(tweet.lang)
        if count%10000 ==0: print(tweet.date.replace(tzinfo=None))
        count+=1


    data={
        'id_tweet':id_tweet,
        'nick_name':nick_name,
        'user':user,
        'tweets':tweets,
        'time':time,
        'likes':likes,
        'retweets':retweets,
        'link':link,
        'replies':replies,
        'language':lang
    }

    return pd.DataFrame(data)





st.title('Creating social listening dashboard prototype')


#st_autorefresh(interval=20000, limit=100, key="fizzbuzzcounter")

with st.form(key="my_form"):
    a, b, c, d = st.columns([1.5, 1.5, 1.5, 1.5])
    all_words=a.text_input(label="All of these words")
    exact_phrase=b.text_input(label="This exact phrase")
    any_words=c.text_input(label="Any of these words")
    exclude_words=d.text_input(label="Exclude these words")


    a, b, c, d = st.columns([1, 1, 1, 1])
    hashtags=a.text_input(label="All of these hashtags (use #)")
    from_account=b.text_input(label="From accounts (use @)")
    to_account=c.text_input(label="To accounts(use @)")
    mention_account=d.text_input(label="Mentioning accounts (use @)")

    st.title("Engagement")

    a, b, c = st.columns([1, 1, 1])
    min_replies=a.number_input(label="Min replies", value=False)
    min_likes=b.number_input(label="Min likes", value=False)
    min_retweets=c.number_input(label="Min retweets", value=False)

    a, b  = st.columns([1, 2])
    exclude_replies = a.checkbox("Exclude replies", False)
    exclude_retweets = b.checkbox("Exclude retweets", False)

    st.title("Dates")
    a, b  = st.columns([1, 1])
    start_date = a.date_input(
                "Tweets from")

    end_date=b.date_input(
                "Tweets until")

    submit_button = st.form_submit_button(label="Submit")


query_str=search_twitter( 
                all_words=all_words, exact_phrase=exact_phrase, any_words=any_words, 
                exclude_words=exclude_words,hashtags=hashtags,
                    from_account=from_account, to_account=to_account, mention_account=mention_account,
                    exclude_replies=exclude_replies, exclude_retweets=exclude_retweets,
                    min_replies=min_replies, min_likes=min_likes, 
                    min_retweets=min_retweets,
                    start_date=start_date, end_date=end_date
                    )

            



st.write(query_str)


df_tweets = get_twitter_df(query_str)

st.write(df_tweets)
#data=pd.read_csv(r"C:\Users\fernandeztovar.7\OneDrive - Teleperformance\Desktop\Projects team\Social Listening\webapp_sociallistening\data\final_df_star.csv")
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_tweets)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)
count_tweets=str(df_tweets["id_tweet"].count())
st.metric(label="Number of tweets", value=count_tweets)


st.title("Data Analysis section")

import ast
import pandas as pd
from TextMining import text_functions
from TextMining import social_media_functions
import regex as re

#df_tweets=df_tweets.drop_duplicates(subset=["id_tweet","link","user","time"],inplace=True)

df_tweets = text_functions.polarity(df_tweets,"tweets")

df1 = df_tweets.copy()

def get_polarity(x):
    if x<-0.3:
        return "negative"
    elif x>0.3:
        return "positive"
    else:
        return "neutral"


df1["Polarity_name"] = df1["Polarity"].apply(get_polarity)
df1["tweets"] = df1["tweets"].apply(social_media_functions.remove_urls)
df1["tweets"] = df1["tweets"].apply(social_media_functions.remove_phone_numbers)
df1["tweets"] = df1["tweets"].apply(social_media_functions.remove_mentions)



#df1["month"]=df1["time"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%B"))
#df1["year"]=df1["time"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%Y"))
df1["month"]=df1["time"].dt.month
df1["year"]=df1["time"].dt.year
df1["date"]=df1["time"].dt.date
df1["Hour"]=df1["time"].dt.hour

words = text_functions.create_freq_words_df(df1, columns_to_group = ["year", "month","date","id_tweet","Polarity_name"], remove_sw=True, lema=True, text_col="tweets")
bigrams = text_functions.create_bigram_df(df1, columns_to_group = ["year", "month","date","id_tweet","Polarity_name"], remove_sw=True, lema=True, text_col="tweets")
bigrams.reset_index(inplace=True)

words.reset_index(inplace=True)
mentions = social_media_functions.find_mentions(df_tweets, column_text="tweets", columns_to_keep=["id_tweet"])
mentions_freq=mentions.groupby("mentions").count().reset_index().rename(columns={"id_tweet":"freq"}).sort_values(by="freq", ascending=False)


hashtags = social_media_functions.find_hashtags(df_tweets, column_text="tweets", columns_to_keep=["id_tweet"])

hashtags_freq=hashtags.groupby("hashtags").count().reset_index().rename(columns={"id_tweet":"freq"}).sort_values(by="freq", ascending=False)

col1, col2, col3, col4=st.columns([2,2,2,2])

#with col1:
col1.write("Words frequency")
col1.write(words[["word","freq"]].sort_values(by="freq",ascending=False) )
col2.write("Bigrams frequency")
col2.write(bigrams[["bigram","freq"]].sort_values(by="freq",ascending=False))
col3.write("Mentions frequency")
col3.write(mentions_freq)
col4.write("Hashtags frequency")
col4.write(hashtags_freq)




#df2=df1.groupby("date").mean().reset_index()


#dropdown of hashtags, mentions, To, From


#Plots

#Tweets and avg polarity by day

#trying with month as well in the same fig


#Select user and see his tweets (% participation)



#plots Section


import plotly.express as px

a, b, c, d = st.columns([1.5, 1.5, 1.5, 1.5])

x_axis_variable=a.selectbox("x axis variable",["date","month"])

user_filter=b.multiselect("user filter",df1["user"].unique())

#mention_filter=c.multiselect("mention filter",mentions_freq["mentions"].unique())

#To_filter=d.selectbox("x axis variable",hashtags_freq["hashtags"].unique())

if len(user_filter)!=0:

    df1=df1[df1["user"].isin(user_filter)]


df2=df1.groupby(x_axis_variable).mean().reset_index()
df3=df1.groupby(x_axis_variable).count().reset_index()

#st.write(f"Average sentiment by {x_axis_variable}")

#st.write(df2)
#st.write(df3)
#fig=px.bar(df2, x=x_axis_variable, y="Polarity", title=f"Polarity vs {x_axis_variable}")
#st.write(fig)

fig1=px.line(df2, x=x_axis_variable, y="Polarity", title=f"Average polarity by {x_axis_variable}")

fig2=px.bar(df3,x=x_axis_variable, y="Polarity", title=f"#tweets by {x_axis_variable}")

a, b = st.columns([1.5, 1.5])

a.write(fig1)

b.write(fig2)

#freq by word by day and month

ids_tweets=df1["id_tweet"].unique()

words=words.sort_values(by="freq",ascending=False)

words=words[words["id_tweet"].isin(ids_tweets)]

fig1=px.bar( words[:20], x="word", y="freq", color=x_axis_variable, title=f"Word frequency by {x_axis_variable}",
        barmode="group")

#st.write(fig)


#freq by bigram by day and month

bigrams=bigrams.sort_values(by="freq",ascending=False)
bigrams=bigrams[bigrams["id_tweet"].isin(ids_tweets)]
fig2=px.bar( bigrams[:20], x="bigram", y="freq", color=x_axis_variable, title=f"Bigram frequency by {x_axis_variable}",
        barmode="group")

#st.write(fig)

a, b = st.columns([1.5, 1.5])

a.write(fig1)

b.write(fig2)
#Display tweets

st.subheader("Sample of tweets")

def display_dict(dict):
    for k, v in dict.items():
        a, b = st.columns([1, 4])
        a.write(f"**{k}:**")
        b.write(v)

def display_tweet(row):
    parsed_tweet = {
        "author": row["user"],
        "created_at": row["time"],
        "url": row["link"],
        "text": row["tweets"],
        "Polarity name":row["Polarity_name"]
    }
    display_dict(parsed_tweet)

for index, row in df1[:10].iterrows():
    display_tweet(row.to_dict())



#from streamlit_pandas_profiling import st_profile_report
#import pandas_profiling

#df2=df1.drop(["id_tweet","tweets","link","language","nick_name","SW removed","SW removed and Lematized"], axis=1)
#st.write(df2)
#pr = df2.profile_report(
#        correlations={"pearson": {"calculate": True},
#                                "spearman": {"calculate": False},
#                                "kendall": {"calculate": False},
#                                "phi_k": {"calculate": False}
#                                }
#            )
#st.subheader("Descriptive analytics")
#st_profile_report(pr)
