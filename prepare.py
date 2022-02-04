import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd
from time import strftime
import acquire

# I'M TAKING A NEW APPROACH
# def basic_clean(df):
#     for col in df.columns:
#         df[col] = df[col].str.lower().str.normalize('NFKD')\
#         .str.encode('ascii', 'ignore')\
#         .str.decode('utf-8', 'ignore')\
#         .replace(r"[^a-z0-9'\s]", '',regex=True)
#     return df

def basic_clean(df):
    df = original.str.lower().replace(r'[^\w\s]', '', regex=True)\
    .str.normalize('NFKD').str.encode('ascii', 'ignore').str.decode('utf-8', 'ignore')
    return df

# NEW APPROACH
# def tokenize(df):
#     for col in df.columns:
#         df[col] = df[col].apply(tokenizer.tokenize)
#     return df

def stem(df,col):
    ps = nltk.porter.PorterStemmer()
    stems = df[col].apply(lambda row: [ps.stem(word) for word in row])
    df['stemmed'] = stems.str.join(' ')
    return df