import re  # For preprocessing
import json
import pandas as pd  # For data handling
from time import time  # To time our operations
from collections import defaultdict  # For word frequency

import spacy  # For preprocessing
import nltk
from nltk.tokenize import word_tokenize
#nltk.download('all')

import logging  # Setting up the loggings to monitor gensim
from gensim.models import Word2Vec, KeyedVectors
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

import gensim.downloader as api
w2v_model = api.load('word2vec-google-news-300')

required_preprocess = True
create_temporal_graph = True 
use_all_words = True
write_to_file = True

books = ['Lenin_Selected_Works', 'Lenin_a_Political_Life']

with open("json_files/%s/temporal_word_list.json"%books[0], 'r') as content:
    gandhi_autobio = json.load(content)
with open("json_files/%s/temporal_word_list.json"%books[1], 'r') as content:
    gandhi_bio = json.load(content)



if required_preprocess:

    nlp = spacy.load("en_core_web_sm", disable=['ner', 'parser']) # disabling Named Entity Recognition for speed
    def cleaning(doc):
        # Lemmatizes and removes stopwords
        # doc needs to be a spacy Doc object
        txt = [token.lemma_ for token in doc if not token.is_stop]
        # Word2Vec uses context words to learn the vector representation of a target word,
        # if a sentence is only one or two words long,
        # the benefit for the training is very small
        if len(txt) > 2:
            return ' '.join(txt)


    # nltk.download('punkt')
    # nltk.download('stopwords')
    from nltk.corpus import stopwords

    stop_words = set(stopwords.words('english'))
    stop_words.update(["'s","u", "sometimes", "firom", "g", "even", "many", "p", "pp", "w", "us", "said", "told", "came", "come", "became", "dr", "go", "sjt", "co", "un", "one", "might", "must", 
    'january','feb','march','april','may','june','july','august','september','october','november','december', 'vol', 'mr', 'k', 'self', 'thy', 'thus', 'west','sw',
    'end', 'tion', 'th', 'used', 'location', 'indians', 'indian', 'wrote', 'already', 'con', 'ment', 'whils', 'work', 'also', 'could', 'know', 'learnt', 'spite',
    'see', 'get', 'beginning', 'ing', 'east', 'felt', 'take', 'tie',',','.','in','and','this','we','they','way','I','The','11','22','1947','1969','1943','?',';','he','this','we','in','but','would',
    'it','1942','1945','1970','’','‘','*',')','(','4','2','sr','sc','ov','z', 'time', 'moment', 'day', 'hour', 'evening', 'night', 'month', 'day', 'year', 'large', 'small', 'begin', 'start', 'week',
    'like', 'say',  'thing', 'low', 'high', 'ji', 'stn', 'tell','weekly', 'daily', 'thirteen', 'seven', 'eighteen', 'nineteen', 'twenty', 'seventeen', 'true', 'truth',
    'bene', 'te', 'su', 'xe', 'di', 'l', 'ection', 'cient', 'n', 'dence', 'erence', 'h', 'ort', 'speci', 'r', 'ter', 'ght', 'ected', 'erence', 'ort', 'ere', 'dre'
    ])

    t = time()

    tokens_autobio = {}
    tokens_bio = {}
    for range, sentences in gandhi_autobio.items():
        brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in sentences.split('.'))
        sent = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000)]
        sent = [x for x in sent if x is not None]
        tokens = word_tokenize(' '.join(sent))
        tokens = [x for x in tokens if x not in stop_words]
        tokens_autobio[range] = tokens

    for range, sentences in gandhi_bio.items():
        brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in sentences.split('.'))
        sent = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000)]
        sent = [x for x in sent if x is not None]
        tokens = word_tokenize(' '.join(sent))
        tokens = [x for x in tokens if x not in stop_words]
        tokens_bio[range] = tokens

    print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))


if create_temporal_graph:
    import networkx as nx
    def create_graph(word_list, T=0.5):
        mygraph = nx.Graph()

        for n in word_list:
            if n in list(w2v_model.index_to_key):
                mygraph.add_node(n)
        for n1 in word_list:
            for n2 in word_list:
                try:
                    if n1 != n2 and w2v_model.similarity(n1, n2)>T:
                        mygraph.add_edge(n1, n2)
                except:
                    pass
        return mygraph


    from community import community_louvain
    import matplotlib.pyplot as plt
    from networkx.algorithms.community import greedy_modularity_communities
    import numpy as np

    autobio_temporal_communities = {}
    i = 0
    for yrange, tokens in tokens_autobio.items():

        t = time()
        print("len of tokens %s"%len(tokens))

        if use_all_words:
            G = create_graph(tokens)
        else:
            G = create_graph(tokens[:1000])

        part_graph = community_louvain.best_partition(G)

        autobio_temporal_communities[yrange] = {}
        for word, com in part_graph.items():
            if isinstance(word, str):
                try:
                    autobio_temporal_communities[yrange][com].append(word)
                except:
                    autobio_temporal_communities[yrange][com] = [word]

        communities = [part_graph.get(node) for node in G.nodes()]
        # plt.figure(figsize=(30, 30))

        # nx.draw(G, node_color = communities, with_labels=False,
        #                   pos = nx.spring_layout(G, k=0.3*1/np.sqrt(len(G.nodes())),
        #                   iterations=30), font_weight='bold', font_family = 'serif',edge_color = '#acff9d', node_size=50, ax=ax[i])
        # ax[i].set_axis_on()
        i += 1

        print('Time to detect community {} : {} mins'.format(i+1, round((time() - t) / 60, 2)))


    with open('json_files/%s/word_temporal_communities.json'%books[0], 'w') as content:
        json.dump( autobio_temporal_communities ,content, indent=4 )


    bio_temporal_communities = {}
    i = 0
    for yrange, tokens in tokens_bio.items():

        t = time()
        print("len of tokens %s"%len(tokens))
        if use_all_words:
            G = create_graph(tokens)
        else:
            G = create_graph(tokens[:1000])

        part_graph = community_louvain.best_partition(G)

        bio_temporal_communities[yrange] = {}
        for word, com in part_graph.items():
            if isinstance(word, str):
                try:
                    bio_temporal_communities[yrange][com].append(word)
                except:
                    bio_temporal_communities[yrange][com] = [word]

        communities = [part_graph.get(node) for node in G.nodes()]
        i += 1

        print('Time to detect community {} : {} mins'.format(i+1, round((time() - t) / 60, 2)))


    with open('json_files/%s/word_temporal_communities.json'%books[1], 'w') as content:
        json.dump(bio_temporal_communities ,content, indent=4 )

if not create_temporal_graph:
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

if write_to_file:
    result_file = open("word_temporal_networks_%s.txt"%books[1].split('_')[0], "w+")
    result_file.write("####################################### Autobiography ###############################################\n")

    links = 0
    threshold = 0.25
    number_of_snap = len(autobio_temporal_communities_list)
    i = 0

    while i < number_of_snap-1:
        for com1, word_list1 in autobio_temporal_communities_list[i].items():
            for com2, word_list2 in autobio_temporal_communities_list[i+1].items():
                intersection = set(word_list1).intersection(set(word_list2))
                similarity = min(len(intersection)/len(word_list1), len(intersection)/(len(word_list2)))
                if similarity > threshold:
                    links += 1
                    result_file.write("snap%s Community%s words %s -> snap%s community%s words %s\n"%(i+1, com1, word_list1, i+2, com2, word_list2))
                    print("snap%s Community%s words %s -> snap%s community%s words %s"%(i+1, com1, word_list1, i+2, com2, word_list2))
                    result_file.write("Evolution = %s\n"%evaluation_topic_modelling(word_list1, word_list2))
                    print("Evolution = %s"%evaluation_topic_modelling(word_list1, word_list2))
        i += 1


    result_file.write("\n\n\n\n")

    result_file.write("####################################### Biography ###############################################\n")

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
                    result_file.write("snap%s Community%s words %s -> snap%s community%s words %s\n"%(i+1, com1, word_list1, i+2, com2, word_list2))
                    print("snap%s Community%s words %s -> snap%s community%s words %s"%(i+1, com1, word_list1, i+2, com2, word_list2))
                    result_file.write("Evolution = %s\n"%evaluation_topic_modelling(word_list1, word_list2))
                    print("Evolution = %s"%evaluation_topic_modelling(word_list1, word_list2))
        i += 1