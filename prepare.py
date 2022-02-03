import unicodedata
import re
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
import pandas as pd
from time import strftime
import acquire


def basic_clean(df):
    for col in df.columns:
        df[col] = df[col].str.lower().str.normalize('NFKD')\
        .str.encode('ascii', 'ignore')\
        .str.decode('utf-8', 'ignore')\
        .replace(r"[^a-z0-9'\s]", '',regex=True)
    return df