        
def remove_stop_words(table, column, lematize=False):

    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    import regex as re

    stop_words = set(stopwords.words("english"))
    f = open("TextMining/words to delete.txt", "r")
    common_words = f.read().split('\n') 

    r = open("TextMining/regex_sintaxis_to_delete.txt", "r")
    reg =r.read().split('\n') 

    for remove in reg:
        table["SW removed"]=table[column].apply(lambda x: re.sub(remove," ",x))

    if lematize:
        table["SW removed"] = table[column].apply(lambda x: [w for w in word_tokenize(x) if not w in stop_words and w not in common_words and len(w) > 2])
        return lematize_words(table)
    else:
        table["SW removed"] = table[column].apply(lambda x: [w for w in word_tokenize(x) if not w in stop_words and w not in common_words and len(w) > 2])
        return table
    

def lematize_words(table):

    from nltk.stem import WordNetLemmatizer
    
    WNlemma = WordNetLemmatizer()
    table["SW removed and Lematized"]=table["SW removed"].apply(lambda x: [WNlemma.lemmatize(w, pos = "v") for w in x])
    return table

def polarity(table,column):

    from textblob import TextBlob

    pol= lambda x: TextBlob(x).sentiment.polarity
    table["Polarity"]=table[column].apply(pol)
    return table
        
        
def create_bigram_df(table, columns_to_group = False, remove_sw=False, lema=False, text_col=""):

    from nltk.probability import FreqDist
    from nltk import bigrams
    import pandas as pd

    if remove_sw:
        table = remove_stop_words(table,text_col,lema)

    if not bool(columns_to_group):
        table["group"]=1
        columns_to_group=["group"]

    #group df by month year and user and group by a custom function
    df_grouped=table.groupby(columns_to_group).apply(lambda x: sum(x["SW removed and Lematized"],[]))
    bigram=df_grouped.apply(lambda x: FreqDist(bigrams(x)))
    #explode bigram by key in the dictionary
    bigram_list=bigram.apply(lambda x: [ [key ,x[key]] for key in x])
    #bigram_list to a dataframe
    bigram_df=pd.DataFrame(bigram_list, columns=["bigram"])
    bigram_df=bigram_df.explode("bigram")
    #delete nan in bigram_df
    bigram_df.dropna(inplace=True)
    bigram_df["freq"]=bigram_df["bigram"].apply(lambda x: x[1])
    bigram_df["word1"]=bigram_df["bigram"].apply(lambda x: x[0][0])
    bigram_df["word2"]=bigram_df["bigram"].apply(lambda x: x[0][1])
    bigram_df["bigram"]=bigram_df["bigram"].apply(lambda x: x[0][0]+" "+x[0][1])

    return bigram_df


def create_trigram_df(table, columns_to_group= False, remove_sw=False, lema=False, text_col=""):

    from nltk.probability import FreqDist
    from nltk import trigrams
    import pandas as pd

    if remove_sw:   
        table = remove_stop_words(table,text_col,lema)

    if not bool(columns_to_group):
        table["group"]=1
        columns_to_group=["group"]

    #group df by month year and user and group by a custom function
    df_grouped=table.groupby(columns_to_group).apply(lambda x: sum(x["SW removed and Lematized"],[]))
    bigram=df_grouped.apply(lambda x: FreqDist(trigrams(x)))
    #explode bigram by key in the dictionary
    bigram_list=bigram.apply(lambda x: [ [key ,x[key]] for key in x])
    #bigram_list to a dataframe
    bigram_df=pd.DataFrame(bigram_list, columns=["trigram"])
    bigram_df=bigram_df.explode("trigram")
    #delete nan in bigram_df
    bigram_df.dropna(inplace=True)
    bigram_df["freq"]=bigram_df["trigram"].apply(lambda x: x[1])
    bigram_df["word1"]=bigram_df["trigram"].apply(lambda x: x[0][0])
    bigram_df["word2"]=bigram_df["trigram"].apply(lambda x: x[0][1])
    bigram_df["word3"]=bigram_df["trigram"].apply(lambda x: x[0][2])
    bigram_df["trigram"]=bigram_df["trigram"].apply(lambda x: x[0][0]+" "+x[0][1]+" "+x[0][2])
    return bigram_df


def create_freq_words_df(table, columns_to_group, remove_sw=False, lema=False, text_col=""):

    from nltk.probability import FreqDist
    import pandas as pd

    if remove_sw:
        table = remove_stop_words(table,text_col,lema)

    #group df by month year and user and group by a custom function
    df_grouped=table.groupby(columns_to_group).apply(lambda x: sum(x["SW removed and Lematized"],[]))
    bigram=df_grouped.apply(lambda x: FreqDist(x))

    #explode bigram by key in the dictionary
    bigram_list=bigram.apply(lambda x: [ [key ,x[key]] for key in x])

    #bigram_list to a dataframe
    bigram_df=pd.DataFrame(bigram_list, columns=["words"])
    bigram_df=bigram_df.explode("words")

    #delete nan in bigram_df
    bigram_df.dropna(inplace=True)
    bigram_df["freq"]=bigram_df["words"].apply(lambda x: x[1])
    bigram_df["word"]=bigram_df["words"].apply(lambda x: x[0])

    return bigram_df
