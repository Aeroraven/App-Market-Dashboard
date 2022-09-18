import base64
import enum
import math

import cv2
import pandas as pd
import numpy as np
import wordcloud
from scipy.special import *


class DataCache:
    main_dataset: pd.DataFrame = None
    review_dataset: pd.DataFrame = None
    avg_reviews = math.sqrt(44152.9)
    avg_download = (15462912)
    avg_price = 1.027368
    avg_rating = 4.191757
    avg_apps = 328.4545


def get_main_dataset():
    if DataCache.main_dataset is None:
        DataCache.main_dataset = pd.read_csv(r'./data/googleplaystore.csv', encoding="gbk")
    return DataCache.main_dataset


def get_review_dataset():
    if DataCache.review_dataset is None:
        DataCache.review_dataset = pd.read_csv(r"./data/googleplaystore_user_reviews.csv")
    return DataCache.review_dataset


def get_main_stats_by_category(category, key):
    dataset = get_main_dataset()
    if category is not None:
        dataset = dataset[dataset['Category'].isin([category])]
    return dataset[key].reset_index(drop=True)


def get_app_reivews(app):
    dataset = get_review_dataset()
    if app is not None:
        dataset = dataset[dataset['App'].isin([app])]
    return dataset['Translated_Review'].reset_index(drop=True)

def get_app_reivews_polarity(app):
    dataset = get_review_dataset()
    if app is not None:
        dataset = dataset[dataset['App'].isin([app])]
    fw = dataset['Sentiment'].reset_index(drop=True)
    ls = [0,0,0]
    for i in range(len(fw)):
        if fw[i] == "Positive":
            ls[0] += 1
        if fw[i] == "Neutral":
            ls[1] += 1
        if fw[i] == "Negative":
            ls[2] += 1
    return ls


def get_main_stats_by_app_name(app_name, key):
    dataset = get_main_dataset()
    if app_name is not None:
        dataset = dataset[dataset['App'].isin([app_name])]
    return dataset[key].reset_index(drop=True)


def get_cate_radar(category):
    series_rt = get_main_stats_by_category(category, "Rating")
    series_pr = get_main_stats_by_category(category, "Price")
    series_in = get_main_stats_by_category(category, "Installs")
    series_rv = get_main_stats_by_category(category, "Reviews")
    standard = [DataCache.avg_apps, DataCache.avg_rating, DataCache.avg_price, DataCache.avg_download,
                DataCache.avg_reviews]
    installs = []
    ratings = []
    reviews = []
    price = []
    for i in range(len(series_in)):
        if pd.isna(series_in[i]) or pd.isna(series_rt[i]) or pd.isna(series_rv[i]):
            continue
        installs.append(int(series_in[i].replace(",", "").replace("+", "")))
        ratings.append(series_rt[i])
        reviews.append(series_rv[i])
        price.append(float(series_pr[i].replace("$", "")))
    avg = lambda x: sum(x) / len(x)
    cate = [len(price), avg(ratings), avg(price), (avg(installs)), math.sqrt(avg(reviews))]
    cate_r = [cate[i] / standard[i] * standard[1] for i in range(len(standard))]
    standard_r = [standard[1] for _ in range(len(standard))]
    standard_r[1] = standard[1]
    cate_r[1] = cate[1]
    return cate_r, standard_r, ["Variety", "Rating", "Price", "Popularity", "Review"]


def get_rating_stats(category):
    series = get_main_stats_by_category(category, "Rating")
    series = series.dropna()
    series = series[series <= 5.0]
    return series


def get_content_rating_stats_by_category(category):
    cr = ['Everyone', 'Everyone 10+', 'Teen', 'Mature 17+', 'Adults only 18+', 'Unrated']
    cr.reverse()
    cr_re = {}
    for i in range(len(cr)):
        cr_re[cr[i]] = i
    series_cr = get_main_stats_by_category(category, "Content Rating")
    series_in = get_main_stats_by_category(category, "Installs")
    series_rt = get_main_stats_by_category(category, "Rating")
    installs = [[] for _ in range(len(cr))]
    ratings = [[] for _ in range(len(cr))]
    for i in range(len(series_cr)):
        if pd.isna(series_cr[i]):
            continue
        installs[cr_re[series_cr[i]]].append(series_in[i].replace(",", "").replace("+", ""))
        if not np.isnan(series_rt[i]):
            ratings[cr_re[series_cr[i]]].append(series_rt[i])
    return cr, [len(i) for i in installs], installs, ratings


def get_review_rating_download_bubble_map(category):
    series_in = get_main_stats_by_category(category, "Installs")
    series_rt = get_main_stats_by_category(category, "Rating")
    series_rv = get_main_stats_by_category(category, "Reviews")
    series_ap = get_main_stats_by_category(category, "App")
    installs = []
    ratings = []
    reviews = []
    apps = []
    for i in range(len(series_in)):
        if pd.isna(series_in[i]) or pd.isna(series_rt[i]) or pd.isna(series_rv[i]) or pd.isna(series_ap[i]):
            continue
        installs.append(2 + (math.log2(int(series_in[i].replace(",", "").replace("+", "")))))
        ratings.append(series_rt[i])
        reviews.append(series_rv[i])
        apps.append(series_ap[i])
    return apps, reviews, ratings, installs


def generate_word_cloud(comments):
    c = wordcloud.WordCloud()
    c.generate(comments)
    # success, encoded_image = cv2.imencode(".png", c.to_array())
    # byte_data = encoded_image.tobytes()
    # base = "data:image/png;base64," + base64.b64encode(byte_data).decode('utf-8')
    return c.to_array()


def generate_word_cloud_by_app(app):
    ds = get_app_reivews(app)
    if len(ds) == 0:
        return generate_word_cloud("Empty Data")
    strs = ""
    for i in range(len(ds)):
        if not pd.isna(ds[i]):
            strs += ds[i]+" "
    if strs == "":
        return generate_word_cloud("Empty Data")
    return generate_word_cloud(strs)

def get_app_rating_ref(app_name):
    fr = get_main_stats_by_app_name(app_name, "Rating")
    return fr[0]


def get_app_reviews_ref(app_name):
    fr = get_main_stats_by_app_name(app_name, "Reviews")
    return fr[0]


def get_app_downloads_ref(app_name):

    fr = get_main_stats_by_app_name(app_name, "Installs")
    return fr[0].replace(",", "").replace("+", "")

def get_app_cr_ref(app_name):
    cr = ['Everyone', 'Everyone 10+', 'Teen', 'Mature 17+', 'Adults only 18+', 'Unrated']
    dm = {
        'Everyone': 3,
        'Everyone 10+': 10,
        'Teen': 12,
        'Mature 17+': 17,
        'Adults only 18+': 18,
        'Unrated': -1
    }
    fr = get_main_stats_by_app_name(app_name, "Content Rating")
    return dm[fr[0]]


def get_categories():
    fw = []
    fs = []
    ds = get_main_dataset()['Category']
    for i in range(len(ds)):
        if ds[i] not in fw:
            lk = ds[i].replace("_", " ").lower().capitalize()
            fw.append(ds[i])
            fs.append(lk)
    return fs


def get_category_i(name):
    return name.upper().replace(" ", "_")


def get_application_list(category):
    fw = []
    ds = get_main_stats_by_category(category, "App")
    for i in range(len(ds)):
        if ds[i] not in fw:
            fw.append(ds[i])
    fw = sorted(fw)
    return fw


if __name__ == "__main__":
    print(get_app_reivews("Honkai Impact 3rd"))
