import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("final.csv")
import re


def remove_hashtags(text):
    text = re.sub(r'@\w+', '', text)
    return text


def remove_emojis(text):
    text = [x for x in text.split(' ') if x.isalpha()]
    text = ' '.join(text)
    return text


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_urls(text):
    text = re.sub(r'http\S+', '', text)
    return text


def preprocess(text):
    text = remove_hashtags(text)
    text = remove_emoji(text)
    text = remove_urls(text)
    return text


df['content'] = df['content'].apply(preprocess)

df_data = pd.DataFrame(columns=['content', 'sentiment'])
for i in np.unique(df['sentiment']):
    temp = df.loc[df['sentiment'] == i].iloc[:700]
    print(temp.shape)
    df_data = df_data.append(temp, ignore_index=True)

X = df_data['content']
Y = df_data['sentiment']

enc = LabelEncoder()
Y = enc.fit_transform(Y)
filename = 'models/finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))




def predict():
    f = open('output.txt', 'r')
    text = pd.Series(f)
    pred = loaded_model.predict(text)
    f.close()
    return enc.classes_[pred][0]

# predict(f)
