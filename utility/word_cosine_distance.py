import re  # For preprocessing
import os
import json
import pandas as pd  # For data handling
from time import time  # To time our operations
from collections import defaultdict  # For word frequency
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import spacy  # For preprocessing
from gensim.models import Word2Vec, KeyedVectors
import itertools
import collections
import matplotlib.pyplot as plt

import gensim.downloader as api
w2v_model = api.load('word2vec-google-news-300')

config = {
    "Gandhi1": {
        "autobiography": "SOMEWT",
        "biography": "Life_of_Mahatma_Gandhi",
        "start_year": 1888,
        "end_year": 1924,
        "year_window": 5
    },
    "Gandhi2": {
        "autobiography": "SOMEWT",
        "biography": "Gandhi_Before_India",
        "start_year": 1888,
        "end_year": 1914,
        "year_window": 5
    },
    "Nehru": {
        "autobiography": "Jawaharlal_Nehru_Autobiography",
        "biography": "Jawaharlal_Nehru_a_Biography",
        "start_year": 1912,
        "end_year": 1939,
        "year_window": 5
    },
    "Lincoln": {
        "autobiography": "Abraham_Lincoln_Autobiography",
        "biography": "Life_of_Abraham_Lincoln",
        "start_year": 1830,
        "end_year": 1865,
        "year_window": 8
    },
    "Nelson": {
        "autobiography": "nelson_autobiography",
        "biography": "nelson_mandela_biography",
        "start_year": 1939,
        "end_year": 1994,
        "year_window": 7
    },
    "Sachin": {
        "autobiography": "playing_it_my_way",
        "biography": "sachin_story_of_my_life",
        "start_year": 1984,
        "end_year": 2008,
        "year_window": 5
    },
    "Lenin": {
        "autobiography": "Lenin_Selected_Works",
        "biography": "Lenin_a_Political_Life",
        "start_year": 1890,
        "end_year": 1914,
        "year_window": 5
    }
}





stop_words = set(stopwords.words('english'))
stop_words.update(["'s","u", "sometimes", "firom", "g", "even", "many", "p", "pp", "w", "us", "said", "told", "came", "come", "became", "dr", "go", "sjt", "co", "un", "one", "might", "must", 
'january','feb','march','april','may','june','july','august','september','october','november','december', 'vol', 'mr', 'k', 'self', 'thy', 'thus', 'west','sw',
'end', 'tion', 'th', 'used', 'location', 'indians', 'indian', 'wrote', 'already', 'con', 'ment', 'whils', 'work', 'also', 'could', 'know', 'learnt', 'spite',
'see', 'get', 'beginning', 'ing', 'east', 'felt', 'take', 'tie',',','.','in','and','this','we','they','way','I','The','11','22','1947','1969','1943','?',';','he','this','we','in','but','would',
'it','1942','1945','1970','’','‘','*',')','(','4','2','sr','sc','ov','z', 'time', 'moment', 'day', 'hour', 'evening', 'night', 'month', 'day', 'year', 'large', 'small', 'begin', 'start', 'week',
'like', 'say',  'thing', 'low', 'high', 'ji', 'stn', 'tell','weekly', 'daily', 'thirteen', 'seven', 'eighteen', 'nineteen', 'twenty', 'seventeen', 'true', 'truth',
'bene', 'te', 'su', 'xe', 'di', 'l', 'ection', 'cient', 'n', 'dence', 'erence', 'h', 'ort', 'speci', 'r', 'ter', 'ght', 'ected', 'erence', 'ort', 'ere', 'dre', "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",    "below", "beside", "besides", "between", "beyond", "bill", "both",    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",    "find", "fire", "first", "five", "for", "former", "formerly", "forty",    "found", "four", "from", "front", "full", "further", "get", "give", "go",    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",    "latterly", "least", "less", "ltd", "made", "many", "may", "me",    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",    "move", "much", "must", "my", "myself", "name", "namely", "neither",    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",    "please", "put", "rather", "re", "same", "see", "seem", "seemed",    "seeming", "seems", "serious", "several", "she", "should", "show", "side",    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",    "something", "sometime", "sometimes", "somewhere", "still", "such",    "system", "take", "ten", "than", "that", "the", "their", "them",    "themselves", "then", "thence", "there", "thereafter", "thereby",    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",    "third", "this", "those", "though", "three", "through", "throughout",    "thru", "thus", "to", "together", "too", "top", "toward", "towards",    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",    "whence", "whenever", "where", "whereafter", "whereas", "whereby",    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",    "within", "without", "would", "yet", "you", "your", "yours", "yourself",    "yourselves", ".", "!", "?", ",", ";", ":", "[", "]", "{", "}", "-", "+",     "_", "/", "@", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "|", "=",
    ".-", ".,", "'", '"', ',"', 'aa', 'aaj', 'aakash', 'aam', 'aamer', 'aap', 'aaqib', 'aare', 'aata', 'aaye', 'aayi', 'ab', 'aback', 'abey', 's', 'h', 'c', 'hi', 'e',
    'sir'
])

# Get top n words
def get_tfidf_top_features(corpus, n_top=10):
    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf = tfidf_vectorizer.fit_transform([corpus])
    importance = np.argsort(np.asarray(tfidf.sum(axis=0)).ravel())[::-1]
    tfidf_feature_names = np.array(tfidf_vectorizer.get_feature_names())
    return tfidf_feature_names[importance[:n_top]]

# Change the type to 'autobio', 'bio', 'both' according to requirement
def get_avg_embedding_score(type='autobio', n_words=100, corpus_autobio='', corpus_bio=''):
    sim_array = []
    if type=='autobio' or type=='bio':
        try:
            word_list = get_tfidf_top_features(corpus_autobio, n_words) if type=='autobio' else get_tfidf_top_features(corpus_bio, n_words)
        except:
            word_list = []
        for n1 in word_list:
            for n2 in word_list:
                if n1 != n2 and n1 in list(w2v_model.index_to_key) and n2 in list(w2v_model.index_to_key):
                    sim_array.append(w2v_model.similarity(n1, n2))
    
    else:
        try:
            word_list1 = get_tfidf_top_features(corpus_autobio, n_words//2)
        except:
            word_list1 = []
        try:
            word_list2 = get_tfidf_top_features(corpus_bio, n_words//2)
        except:
            word_list2 = []
        for n1 in word_list1:
            for n2 in word_list2:
                if n1 != n2 and n1 in list(w2v_model.index_to_key) and n2 in list(w2v_model.index_to_key):
                    sim_array.append(w2v_model.similarity(n1, n2))

    
    average_score = sum(map(abs, sim_array)) / len(sim_array) if len(sim_array) > 0 else 0
    # print(sim_array)
    # print(average_score)
    return average_score

result_file = open("word_cosine_distance.txt", "w+")
    
for names in ['Lincoln','Nehru', 'Gandhi2']:

    result_file.write("####################################### %s ###############################################\n"%names)
    print("####################################### %s ###############################################\n"%names)
    selected_person = config[names] ## Change the person name accordingly

    autobio = selected_person['autobiography']
    bio = selected_person['biography']
    start = selected_person['start_year']
    end = selected_person['end_year']
    year_window = selected_person['year_window']
    start_year_list = [x for x in range(start, end, year_window)]
    end_year_list = [x+year_window-1 for x in start_year_list]

    for start_year, end_year in zip(start_year_list, end_year_list):
        
        corpus_autobio = ''
        corpus_bio = ''
        print("---------------------------------%s-%s----------------------------"% (start_year, end_year))
        result_file.write("---------------------------------Year-Range %s-%s----------------------------\n"% (start_year, end_year))
        with open("json_files/%s/year_chapter_chaptername_dict.json"%autobio, 'r', encoding="utf-8") as content:
            year_chapter = json.load(content)

        for year in year_chapter.keys():
            if int(year) >= start_year and int(year) <= end_year:
                for chapter_list in year_chapter[year]: 
                    part = chapter_list[0]
                    chap = chapter_list[1]
                    with open("%s/part%s/chapter%s.txt"%(autobio, part, chap), 'r', encoding='utf-8') as f:
                        corpus_autobio += f.read().replace('\n', ' ')

        with open("json_files/%s/year_chapter_chaptername_dict.json"%bio, 'r', encoding="utf-8") as content:
            year_chapter = json.load(content)

        for year in year_chapter.keys():
            if int(year) >= start_year and int(year) <= end_year:
                for chapter_list in year_chapter[year]: 
                    part = chapter_list[0]
                    chap = chapter_list[1]
                    with open("%s/part%s/chapter%s.txt"%(bio, part, chap), 'r', encoding='utf-8') as f:
                        corpus_bio += f.read().replace('\n', ' ')

        result_file.write("Similarity autobio: %s \n"%get_avg_embedding_score(type='autobio', corpus_autobio=corpus_autobio))
        result_file.write("Similarity bio: %s \n"%get_avg_embedding_score(type='bio', corpus_bio=corpus_bio))
        result_file.write("cross similarity %s \n"%get_avg_embedding_score(type='both', corpus_autobio=corpus_autobio, corpus_bio=corpus_bio))
        print(get_avg_embedding_score(type='autobio', corpus_autobio=corpus_autobio))
        print(get_avg_embedding_score(type='bio', corpus_bio=corpus_bio))
        print(get_avg_embedding_score(type='both', corpus_autobio=corpus_autobio, corpus_bio=corpus_bio))

# def remove_punctuation(txt):
#     return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

# def  clean_text(txt):
#     tmp = [remove_punctuation(t) for t in txt]
#     # print(tmp)
#     tmp = [t.lower().split() for t in tmp]
    
#     tmp = [[w for w in t if not w in stop_words]
#               for t in tmp]
#     tmp = [[w for w in t if not w in ['gandhi']]
#                      for t in tmp]
    
#     tmp = list(itertools.chain(*tmp))
#     tmp = collections.Counter(tmp)
#     return tmp


# import shifterator as sh
# from shifterator import shifts as ss

# for names in ['Sachin', 'Lincoln', 'Lenin', 'Nelson', 'Nehru', 'Gandhi2', 'Gandhi1']:

#     print("####################################### %s ###############################################\n"%names)
#     selected_person = config[names] ## Change the person name accordingly

#     autobio = selected_person['autobiography']
#     bio = selected_person['biography']
#     start = selected_person['start_year']
#     end = selected_person['end_year']
#     year_window = selected_person['year_window']
#     start_year_list = [x for x in range(start, end, year_window)]
#     end_year_list = [x+year_window-1 for x in start_year_list]

#     corpus_autobio = ''
#     corpus_bio = ''
#     for start_year, end_year in zip(start_year_list, end_year_list):
        
        
#         with open("json_files/%s/year_chapter_chaptername_dict.json"%autobio, 'r', encoding="utf-8") as content:
#             year_chapter = json.load(content)

#         for year in year_chapter.keys():
#             if int(year) >= start_year and int(year) <= end_year:
#                 for chapter_list in year_chapter[year]: 
#                     part = chapter_list[0]
#                     chap = chapter_list[1]
#                     with open("%s/part%s/chapter%s.txt"%(autobio, part, chap), 'r', encoding='utf-8') as f:
#                         corpus_autobio += f.read().replace('\n', ' ')

#         with open("json_files/%s/year_chapter_chaptername_dict.json"%bio, 'r', encoding="utf-8") as content:
#             year_chapter = json.load(content)

#         for year in year_chapter.keys():
#             if int(year) >= start_year and int(year) <= end_year:
#                 for chapter_list in year_chapter[year]: 
#                     part = chapter_list[0]
#                     chap = chapter_list[1]
#                     with open("%s/part%s/chapter%s.txt"%(bio, part, chap), 'r', encoding='utf-8') as f:
#                         corpus_bio += f.read().replace('\n', ' ')

#     sentences_autobio = re.sub(r'[0-9]', '', corpus_autobio)
#     sentences_bio = re.sub(r'[0-9]', '', corpus_bio)
#     text1 = clean_text(sentences_autobio.split("."))
#     text2 = clean_text(sentences_bio.split("."))

#     jsd_shift = ss.JSDivergenceShift(type2freq_1=text1,
#                                     type2freq_2=text2)

#     ax = jsd_shift.get_shift_graph(top_n=35, show_plot=False)
#     filename = 'word_shift_graph_%s.png'%(names)
#     plt.savefig(filename)