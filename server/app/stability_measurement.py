import pandas as pd
import numpy as np
import json
import networkx as nx
import os
from operator import itemgetter
import math


from app import helper


# book_list = ['SOMEWT', 'Life_of_Mahatma_Gandhi']
book_list = ['SOMEWT', 'Gandhi_Before_India']
year_window = 3
start_year = 1888
end_year = 1924




def get_mention_overlap(year_window, method='frequency', Na='SOMEWT', Nb='Gandhi_Before_India'):

    
    N=10


    with open('app/static/json_files/%s/date_person_list_with_mention.json' % Na) as handle:
        Na_date_to_person_list_with_mention = json.load(handle)
    
    with open('app/static/json_files/%s/date_person_list_with_mention.json' % Nb) as handle:
        Nb_date_to_person_list_with_mention = json.load(handle)

    with open('app/static/json_files/%s/date_person_list.json' % Na) as handle:
        Na_date_to_person_list = json.load(handle)
    
    with open('app/static/json_files/%s/date_person_list.json' % Nb) as handle:
        Nb_date_to_person_list = json.load(handle)

    dic = {}
    if method == 'frequency':
        for year in range(start_year, end_year, year_window):
            yrange = '%s-%s'%(year, year+year_window-1)
            Na_top_mention = helper.returnTopMentionList(Na_date_to_person_list_with_mention, year, year+year_window-1)
            Nb_top_mention = helper.returnTopMentionList(Nb_date_to_person_list_with_mention, year, year+year_window-1)
            dic[yrange] = list(set(Na_top_mention).intersection(set(Nb_top_mention)))

    elif method == 'close_cen':
        for year in range(start_year, end_year, year_window):
            yrange = '%s-%s'%(year, year+year_window-1)

            Na_graph = helper.returnGraph(Na_date_to_person_list, year, year+year_window-1)
            Na_close_cen = nx.closeness_centrality(Na_graph)
            Na_top_close = dict(sorted(Na_close_cen.items(), key = itemgetter(1), reverse = True)[:N])

            Nb_graph = helper.returnGraph(Nb_date_to_person_list, year, year+year_window-1)
            Nb_close_cen = nx.closeness_centrality(Nb_graph)
            Nb_top_close = dict(sorted(Nb_close_cen.items(), key = itemgetter(1), reverse = True)[:N])

            dic[yrange] = list(set(Na_top_close).intersection(set(Nb_top_close)))

    elif method == 'between_cen':
        for year in range(start_year, end_year, year_window):
            yrange = '%s-%s'%(year, year+year_window-1)

            Na_graph = helper.returnGraph(Na_date_to_person_list, year, year+year_window-1)
            Na_between_cen = nx.closeness_centrality(Na_graph)
            Na_top_between = dict(sorted(Na_between_cen.items(), key = itemgetter(1), reverse = True)[:N])

            Nb_graph = helper.returnGraph(Nb_date_to_person_list, year, year+year_window-1)
            Nb_between_cen = nx.closeness_centrality(Nb_graph)
            Nb_top_between = dict(sorted(Nb_between_cen.items(), key = itemgetter(1), reverse = True)[:N])

            dic[yrange] = list(set(Na_top_between).intersection(set(Nb_top_between)))

    return dic

    # for book in book_list:
    #     with open('app/static/json_files/%s/date_person_list_with_mention.json' % book) as handle:
    #         date_to_person_list = json.load(handle)

    #     connection_density = []
    #     for year in range(start_year, end_year, year_window):
    #         dic = {}
            
    #         graph_person = helper.returnGraph(date_to_person_list, year, year+year_window-1)