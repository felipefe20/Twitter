import regex as re
import pandas as pd

def find_hashtags(df, column_text, columns_to_keep):

    df1 = df.copy()
    func = lambda x:  re.findall(r"(#\w+)", x)
    df1["hashtags"] = df1[column_text].apply(func)
    columns_to_keep = columns_to_keep + ["hashtags"]
    hashtags = df1.explode("hashtags")[columns_to_keep]
    hashtags = hashtags[pd.notna(hashtags["hashtags"])]
    return hashtags

def find_mentions(df, column_text, columns_to_keep):

    df1 = df.copy()
    func = lambda x: re.findall(r"(@\w+)", x)
    df1["mentions"] = df1[column_text].apply(func)
    columns_to_keep = columns_to_keep + ["mentions"]
    mentions = df1.explode("mentions")[columns_to_keep]
    mentions = mentions.dropna(subset=["mentions"])
    return mentions


def remove_last_link(text):
    tex = re.sub(r'(https?:\/\/.*[\r\n]*)', '', text)
    return tex

def remove_urls(text):
    tex = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    return tex

def remove_phone_numbers(text):
    tex = re.sub(r'(\+\d{2})?( )?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}', '', text)
    return tex

def remove_mentions(text):
    tex = re.sub(r'@(\w+)', '', text)
    return tex

def remove_hashtags(text):
    tex = re.sub(r'#(\w+)', '', text)
    return tex
