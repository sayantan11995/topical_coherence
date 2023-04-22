from networkx.readwrite import json_graph
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import itertools
import community
import os, os.path
import fnmatch
import random as rand
import json
import matplotlib.colors as colors
import matplotlib.cm as cmx
from community import community_louvain
from time import time  # To time our operations
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords


books = ['nelson_autobiography', 'nelson_mandela_biography']
start=1939
end=1994
year_window=7


start_year_list = [x for x in range(start, end, year_window)]
end_year_list = [x+year_window-1 for x in start_year_list]


def returnGraph(date_dict, start_year, end_year, window_size=1):
    mygraph = nx.Graph()
    for year1 in date_dict.keys():
        if int(year1) < start_year or int(year1) > end_year:
            continue
        #first creating edges in the same year
        for node1 in date_dict[year1]:
            for node2 in date_dict[year1]:
                if node1 != node2:
                    mygraph.add_edge(node1,node2)
                    
        # now creating edges as per window
        for year2 in date_dict.keys():
            if int(year2) < start_year or int(year2) > end_year:
                continue
            if int(year2) <= int(year1) or int(year2) > int(year1) + window_size:
                continue
            for node1 in date_dict[year1]:
                for node2 in date_dict[year2]:
                    if node1 != node2:
                        mygraph.add_edge(node1,node2)
    
    return mygraph

bio_temporal_communities = {}
autobio_temporal_communities = {}

for book in books:
    i = 0
    total_community = 0
    for start_year, end_year in zip(start_year_list, end_year_list):
        t = time()
        with open('json_files/%s/date_person_list.json' % book) as handle:
            date_person_list= json.load(handle)

        G = returnGraph(date_person_list, start_year, end_year)

        part_graph = community_louvain.best_partition(G)
        communities = [part_graph.get(node) for node in G.nodes()]
        # print("Number of communities: %s"%len(list(set(communities))))
        total_community += len(list(set(communities)))
        yrange = str(start_year) + '-' + str(end_year)

        if books.index(book) == 0:
            autobio_temporal_communities[yrange] = {}
            for ne, com in part_graph.items():
                try:
                    autobio_temporal_communities[yrange][com].append(ne)
                except:
                    autobio_temporal_communities[yrange][com] = [ne]
        else:
            bio_temporal_communities[yrange] = {}
            for ne, com in part_graph.items():
                try:
                    bio_temporal_communities[yrange][com].append(ne)
                except:
                    bio_temporal_communities[yrange][com] = [ne]

        i += 1
        
        print('Time to detect community {} : {} mins'.format(i+1, round((time() - t) / 60, 2)))
    print("Total number of communities: %s"%total_community)

result_file = open("NE_temporal_networks_%s.txt"%books[1].split('_')[0], "w+")
def evaluation_topic_modelling(NE_list1, NE_list2, phi=0.5):

    instability = len(set(NE_list2))/ len(set(NE_list1)) - 1

    # print(instability)
    if instability < - phi:
        return "Contract"
    elif instability >= - phi and instability <= phi:
        return "Survive"
    elif instability > phi:
        return "Grow"


autobio_temporal_communities_list = [values for values in autobio_temporal_communities.values()]
bio_temporal_communities_list = [values for values in bio_temporal_communities.values()]
threshold = 0.15

# result_file.write("####################################### Autobiography ###############################################\n")

# links = 0

# number_of_snap = len(autobio_temporal_communities_list)
# i = 0

# while i < number_of_snap-1:
#     for com1, NE_list1 in autobio_temporal_communities_list[i].items():
#         for com2, NE_list2 in autobio_temporal_communities_list[i+1].items():
#             intersection = set(NE_list1).intersection(set(NE_list2))
#             union = set(NE_list1).union(set(NE_list2))
#             similarity = min(len(intersection)/len(NE_list1), len(intersection)/(len(NE_list2)))
#             if similarity > threshold:
#                 links += 1
#                 result_file.write("snap%s Community%s NEs %s -> snap%s community%s NEs %s\n"%(i+1, com1, NE_list1, i+2, com2, NE_list2))
#                 # print("snap%s Community%s NEs %s -> snap%s community%s NEs %s"%(i+1, com1, NE_list1, i+2, com2, NE_list2))
#                 result_file.write("Evolution = %s\n"%evaluation_topic_modelling(NE_list1, NE_list2))
#                 # print("Evolution = %s"%evaluation_topic_modelling(NE_list1, NE_list2))
#     i += 1


# result_file.write("\n\n\n\n")

# result_file.write("####################################### Biography ###############################################\n")

# links = 0
# number_of_snap = len(bio_temporal_communities_list)
# i = 0

# while i < number_of_snap-1:
#     for com1, NE_list1 in bio_temporal_communities_list[i].items():
#         for com2, NE_list2 in bio_temporal_communities_list[i+1].items():
#             intersection = set(NE_list1).intersection(set(NE_list2))
#             union = set(NE_list1).union(set(NE_list2))
#             similarity = min(len(intersection)/len(NE_list1), len(intersection)/(len(NE_list2)))
#             if similarity > threshold:
#                 links += 1
#                 result_file.write("snap%s Community%s NEs %s -> snap%s community%s NEs %s\n"%(i+1, com1, NE_list1, i+2, com2, NE_list2))
#                 # print("snap%s Community%s NEs %s -> snap%s community%s NEs %s"%(i+1, com1, NE_list1, i+2, com2, NE_list2))
#                 result_file.write("Evolution = %s\n"%evaluation_topic_modelling(NE_list1, NE_list2))
#                 # print("Evolution = %s"%evaluation_topic_modelling(NE_list1, NE_list2))
#     i += 1


links = 0
threshold = 0.15
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

    i += 1

links = 0
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



stop_words = set(stopwords.words('english'))
stop_words.update(["second", "swaraj", "hindus", "joy", "compromise", "Love", "Lovejoy", "Nebraska", "Missourie", "Dept", "Home", "HomeDept", "First", "Africanists"])
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