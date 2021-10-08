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




def get_core_periphery_data(year_window):

    core_periphery_data = {}
    N=10

    for book in book_list:
        with open('app/static/json_files/%s/date_person_list.json' % book) as handle:
            date_to_person_list = json.load(handle)

        connection_density = []
        for year in range(start_year, end_year, year_window):
            dic = {}
            
            dic['date'] = '%s-%s'%(year, year+year_window-1)
            graph_person = helper.returnGraph(date_to_person_list, year, year+year_window-1)

            if len(graph_person.nodes()) < 1:
                dic['core_den'] = 0
                dic['core_nodes'] = 0
            else:
                core = nx.k_core(graph_person)
                dic['core_den'] = nx.density(core)
                dic['core_nodes'] = len(core.nodes())

            connection_density.append(dic)

        core_periphery_data[book] = connection_density

    Na = book_list[0]
    Nb = book_list[1]
    with open('app/static/json_files/%s/date_person_list.json' % Na) as handle:
        Na_date_to_person_list = json.load(handle)
    
    with open('app/static/json_files/%s/date_person_list.json' % Nb) as handle:
        Nb_date_to_person_list = json.load(handle)

    core_jaccard_data = []
    for year in range(start_year, end_year, year_window):
        core_jaccard_dic = {}
        yrange = '%s-%s'%(year, year+year_window-1)

        core_jaccard_dic['date'] = yrange

        Na_graph = helper.returnGraph(Na_date_to_person_list, year, year+year_window-1)
        Nb_graph = helper.returnGraph(Nb_date_to_person_list, year, year+year_window-1)

        Na_core_nodes = []
        Nb_core_nodes = []
        if len(Na_graph.nodes()) > 0:
            Na_core = nx.k_core(Na_graph)
            Na_core_nodes = list(Na_core.nodes().keys())

        if len(Nb_graph.nodes()) > 0:
            Nb_core = nx.k_core(Nb_graph)
            Nb_core_nodes = list(Nb_core.nodes().keys())

        core_jaccard_dic['jaccard_coeff'] = helper.Jaccard_score(Na_core_nodes, Nb_core_nodes)

        core_jaccard_dic['overlap'] = list(set(Na_core_nodes).intersection(set(Nb_core_nodes)))

        core_jaccard_data.append(core_jaccard_dic)

    return core_periphery_data, core_jaccard_data


