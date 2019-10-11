import re
import string
import pickle

import tqdm

import PIL
import requests
from io import BytesIO

import torchvision

from datetime import datetime

import pandas as pd


def clean_sentence(s):
    # symb = "!@#%*&()[]{}/?²\"\'#№.,:;%*()<>\n₽1234567890-+–«»\"\\qwertyuiopasdfghjklzxcvbnm"
    # symb = "йцукенгшщзхъфывапролджэёячсмитьбю"
    s = s.lower()
    #for c in symb:
        #s = s.replace(c, "")
    s = re.sub('[^йцукенгшщзхъфывапролджэёячсмитьбю]', ' ', s)
    # s = s.replace('\xa0', " ")

    return s.lower().strip()
    

def clean_text(text):
    res = []
    num_words = 0
    for i in range(len(text)):
        clean = clean_sentence(text[i])
        if len(clean) > 0:
            clean = clean.split()
            # no n_grams for single characters
            for w in clean:
                if len(w) < 2:
                    continue
            res.append(clean)
            num_words += len(clean)
    return res, num_words


def extract_date_info(date):
    """

    :param date: datetime format
    :return: some features, you can easily understand them from their names
    """
    # date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    week_day = [0] * 7
    week_day[date.weekday()] = 1

    is_weekend = 0
    if date.weekday() == 5 or date.weekday() == 6:
        is_weekend = 1

    is_working_time = 0
    if 9 < date.hour < 18 and not is_weekend:
        is_working_time = 1

    is_daytime = 0
    if 7 < date.hour < 23:
        is_daytime = 1

    return week_day + [is_weekend] + [is_working_time] + [is_daytime]


def embedings2df(path):
    with open(path, 'rb') as es:
        embedded_stories = pickle.load(es)
    
    records = dict()
    for key in tqdm.tqdm(embedded_stories.keys()):
        records[key] = embedded_stories[key]['emb']
        
    return pd.DataFrame.from_dict(records, orient='index')


def features_extractor(url_stories, model, device=None):
    features = dict()
    
    for story_id in tqdm.tqdm(list(url_stories.keys())):
        features[story_id] = []
        
        urls = url_stories[story_id]

        for url in tqdm.tqdm(urls):
            response = requests.get(url)
            image = PIL.Image.open(BytesIO(response.content))

            image = torchvision.transforms.ToTensor()(image.convert("RGB"))
            image = image.unsqueeze(0)

            if device == 'cuda':
                model.to(device)
            
            output = model.forward(image)
            output = output.squeeze(0).detach().numpy()

            features[story_id].append(output)
        
    return features  