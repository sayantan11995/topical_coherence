import spacy  # For preprocessing
import nltk
from nltk.tokenize import word_tokenize
import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
#nltk.download('all')

import logging  # Setting up the loggings to monitor gensim
from gensim.models import Word2Vec, KeyedVectors
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)


books = ['SOMEWT', 'Life_of_Mahatma_Gandhi']

with open("json_files/%s/temporal_word_list.json"%books[0], 'r') as content:
    gandhi_autobio = json.load(content)
with open("json_files/%s/temporal_word_list.json"%books[1], 'r') as content:
    gandhi_bio = json.load(content)

with open('json_files/%s/word_temporal_communities.json'%books[0], 'r') as content:
    autobio_temporal_communities = json.load(content)

with open('json_files/%s/word_temporal_communities.json'%books[1], 'r') as content:
    bio_temporal_communities = json.load(content)

autobio_temporal_communities_list = [values for values in autobio_temporal_communities.values()]
bio_temporal_communities_list = [values for values in bio_temporal_communities.values()]

def evaluation_topic_modelling(word_list1, word_list2, phi=0.5):
    # intersection = set(word_list1).intersection(set(word_list2))
    # similarity = min(len(intersection)/len(word_list1), len(intersection)/(len(word_list2)))
    instability = len(set(word_list2))/ len(set(word_list1)) - 1

    # print(instability)
    if instability < - phi:
        return "Contract"
    elif instability >= - phi and instability <= phi:
        return "Survive"
    elif instability > phi:
        return "Grow"

links = 0
threshold = 0.25
number_of_snap = len(autobio_temporal_communities_list)
i = 0

evolution_type_list = ['Grow', 'Survive', 'Contract']
autobio_words = {}
bio_words = {}

for type in evolution_type_list:
    autobio_words[type] = []
    bio_words[type] = []

while i < number_of_snap-1:
    for com1, word_list1 in autobio_temporal_communities_list[i].items():
        for com2, word_list2 in autobio_temporal_communities_list[i+1].items():
            intersection = set(word_list1).intersection(set(word_list2))
            similarity = min(len(intersection)/len(word_list1), len(intersection)/(len(word_list2)))
            if similarity > threshold:
                links += 1
                type = evaluation_topic_modelling(word_list1, word_list2)
                autobio_words[type] += list(intersection)
                # print("snap%s Community%s words %s -> snap%s community%s words %s"%(i+1, com1, word_list1, i+2, com2, word_list2))
                # print("Evolution = %s"%evaluation_topic_modelling(word_list1, word_list2))

    i += 1

links = 0
threshold = 0.25
number_of_snap = len(bio_temporal_communities_list)
i = 0

while i < number_of_snap-1:
    for com1, word_list1 in bio_temporal_communities_list[i].items():
        for com2, word_list2 in bio_temporal_communities_list[i+1].items():
            intersection = set(word_list1).intersection(set(word_list2))
            similarity = min(len(intersection)/len(word_list1), len(intersection)/(len(word_list2)))
            if similarity > threshold:
                links += 1
                type = evaluation_topic_modelling(word_list1, word_list2)
                bio_words[type] += list(intersection)
    i += 1

# print(autobio_words['Survive'])


stop_words = set(stopwords.words('english'))
stop_words.update(["second", "st", "nd", "seventh", "tenth", "fourth", "lay", "autobiography", "put", "pull", "push"])
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stop_words,
                min_font_size = 10).generate(" ".join(bio_words['Survive']))
 
# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()