import pandas as pd
import numpy as np
import json
import networkx as nx
import os
from operator import itemgetter
from fuzzywuzzy import fuzz
import math

window_size = 1
year_window = 3

# Comparison 1 setup
book_list = ['SOMEWT', 'Life_of_Mahatma_Gandhi']
start_year = 1888
end_year = 1924

# # Comparison 2 setup
# book_list = ['SOMEWT', 'Gandhi_Before_India']
# start_year = 1888
# end_year = 1914


# # Comparison 3 setup
# book_list = ['Jawaharlal_Nehru_Autobiography', 'Jawaharlal_Nehru_a_Biography']
# start_year = 1912
# end_year = 1939

# # Comparison 4 setup
# book_list = ['Abraham_Lincoln_Autobiography', 'Life_of_Abraham_Lincoln']
# start_year = 1830
# end_year = 1865

# # Comparison 5 setup
# book_list = ['Lenin_Selected_Works', 'Lenin_a_Political_Life']
# start_year = 1870
# end_year = 1920

# start_year = 1913
# end_year = 1917

Na = book_list[0]
Nb = book_list[1]


# Storing family data
family_list = []
with open("app/static/gandhi_relatives.txt", 'r', encoding="utf-8") as content:
    txt_file = content.read()

for line in txt_file.split('\n'):
    family_list.append(line) 

#
def getFractionRelative(node_list):

    common_members = []

    for node in node_list:
        for member in family_list:
            # print(fuzz.ratio(node, member))
            # print(member)
            if fuzz.partial_ratio(node, member) > 85:
                common_members.append(node)
                
    print(set(common_members))
    if len(node_list) <= 0:
        return 0
    else:
        return len(set(common_members)) / len(set(node_list))



# given date dict creates and returns temporal graph
def returnGraph(date_dict, start_year, end_year):
    mygraph = nx.Graph()
    print("creating graph with start year:" + str(start_year))
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

def returnTopMentionList(date_dict_with_mention, start_year, end_year, N=10):
    
    mydict = {}
    
    for year in date_dict_with_mention.keys():
        if int(year) < start_year or int(year) > end_year:
            continue
   
        for entity, mention in date_dict_with_mention[year].items():
            try:
                mydict[entity] += mention
            except:
                mydict[entity] = mention
                    
    res = dict(sorted(mydict.items(), key = itemgetter(1), reverse = True)[:N])
    
    return res

def Jaccard_score(lista_1, lista_2):    
    inter = len(list(set(lista_1) & set(lista_2)))
    union = len(list(set(lista_1) | set(lista_2)))
    if union <=0:
        return 0
    else:
        return inter/union

def get_connection_density_data(year_window):

    connection_density_data = {}
    N=10

    cumulative_connection_density_data = []
    for book in book_list:
        with open('app/static/json_files/%s/date_person_list.json' % book) as handle:
            date_to_person_list = json.load(handle)

        connection_density = []
        for year in range(start_year, end_year, year_window):
            dic = {}
            
            graph_person = returnGraph(date_to_person_list, year, year+year_window-1)

            dic['date'] = '%s-%s'%(year, year+year_window-1)
            dic['conn_den'] = nx.density(graph_person)
            dic['nodes'] = len(graph_person.nodes())
            connection_density.append(dic)

        connection_density_data[book] = connection_density

        print(connection_density_data)

    return connection_density_data

def get_cummulative_connection_density_data(year_window):

    cumulative_connection_density_data = []

    with open('app/static/json_files/%s/date_person_list.json' % Na) as handle:
        Na_date_to_person_list = json.load(handle)

    with open('app/static/json_files/%s/date_person_list.json' % Nb) as handle:
        Nb_date_to_person_list = json.load(handle)

    for year in range(start_year, end_year, year_window):
        Na_dic = {}
        Nb_dic = {}
        dic = {}
        Na_graph_person = returnGraph(Na_date_to_person_list, year, year+year_window-1)
        Nb_graph_person = returnGraph(Nb_date_to_person_list, year, year+year_window-1)

        dic['date'] = '%s-%s'%(year, year+year_window-1)
        dic['Na_conn_den'] = nx.density(Na_graph_person)
        dic['Nb_conn_den'] = nx.density(Nb_graph_person)
        cumulative_connection_density_data.append(dic)

        print(cumulative_connection_density_data)

    return cumulative_connection_density_data


def get_mention_overlap(year_window, method='frequency', Na=Na, Nb=Nb):
    N=15


    with open('app/static/json_files/%s/date_person_with_mentions.json' % Na) as handle:
        Na_date_to_person_list_with_mention = json.load(handle)
    
    with open('app/static/json_files/%s/date_person_with_mentions.json' % Nb) as handle:
        Nb_date_to_person_list_with_mention = json.load(handle)

    with open('app/static/json_files/%s/date_person_list.json' % Na) as handle:
        Na_date_to_person_list = json.load(handle)
    
    with open('app/static/json_files/%s/date_person_list.json' % Nb) as handle:
        Nb_date_to_person_list = json.load(handle)

    dic = {}
    node_dic = {}
    if method == 'frequency':
        for year in range(start_year, end_year, year_window):
            yrange = '%s-%s'%(year, year+year_window-1)
            Na_top_mention = returnTopMentionList(Na_date_to_person_list_with_mention, year, year+year_window-1)
            Nb_top_mention = returnTopMentionList(Nb_date_to_person_list_with_mention, year, year+year_window-1)
            dic[yrange] = list(set(Na_top_mention).intersection(set(Nb_top_mention)))

            if node_dic.get(yrange) is None:
                node_dic[yrange] = {}
            node_dic[yrange][Na] = Na_top_mention
            node_dic[yrange][Nb] = Nb_top_mention

    elif method == 'close_cen':
        for year in range(start_year, end_year, year_window):
            yrange = '%s-%s'%(year, year+year_window-1)

            Na_graph = returnGraph(Na_date_to_person_list, year, year+year_window-1)
            Na_close_cen = nx.core_number(Na_graph)
            Na_top_close = dict(sorted(Na_close_cen.items(), key = itemgetter(1), reverse = True)[:N])

            Nb_graph = returnGraph(Nb_date_to_person_list, year, year+year_window-1)
            Nb_close_cen = nx.core_number(Nb_graph)
            Nb_top_close = dict(sorted(Nb_close_cen.items(), key = itemgetter(1), reverse = True)[:N])

            dic[yrange] = list(set(Na_top_close).intersection(set(Nb_top_close)))

            if node_dic.get(yrange) is None:
                node_dic[yrange] = {}
            node_dic[yrange][Na] = Na_top_close
            node_dic[yrange][Nb] = Nb_top_close

    elif method == 'between_cen':
        for year in range(start_year, end_year, year_window):
            yrange = '%s-%s'%(year, year+year_window-1)

            Na_graph = returnGraph(Na_date_to_person_list, year, year+year_window-1)
            Na_between_cen = nx.closeness_centrality(Na_graph)
            Na_top_between = dict(sorted(Na_between_cen.items(), key = itemgetter(1), reverse = True)[:N])

            Nb_graph = returnGraph(Nb_date_to_person_list, year, year+year_window-1)
            Nb_between_cen = nx.closeness_centrality(Nb_graph)
            Nb_top_between = dict(sorted(Nb_between_cen.items(), key = itemgetter(1), reverse = True)[:N])

            dic[yrange] = list(set(Na_top_between).intersection(set(Nb_top_between)))

            if node_dic.get(yrange) is None:
                node_dic[yrange] = {}
            node_dic[yrange][Na] = Na_top_between
            node_dic[yrange][Nb] = Nb_top_between

    return dic, node_dic

def get_core_periphery_data(year_window):

    core_periphery_data = {}
    core_nodes = {} # {y: {book1: [], }}
    N=10

    for book in book_list:
        with open('app/static/json_files/%s/date_person_list.json' % book) as handle:
            date_to_person_list = json.load(handle)

        connection_density = []
        
        for year in range(start_year, end_year, year_window):
            dic = {}
            yrange = '%s-%s'%(year, year+year_window-1)
            dic['date'] = yrange

            if core_nodes.get(yrange) is None:
                core_nodes[yrange] = {}
            graph_person = returnGraph(date_to_person_list, year, year+year_window-1)

            if len(graph_person.nodes()) < 1:
                dic['core_den'] = 0
                dic['core_nodes'] = 0
                core_nodes[yrange][book] = []
            else:
                core = nx.k_core(graph_person)
                dic['core_den'] = nx.density(core)
                dic['core_nodes'] = len(core.nodes())
                core_nodes[yrange][book] = list(core.nodes())

            connection_density.append(dic)
            

        core_periphery_data[book] = connection_density

    with open('app/static/json_files/%s/date_person_list.json' % Na) as handle:
        Na_date_to_person_list = json.load(handle)
    
    with open('app/static/json_files/%s/date_person_list.json' % Nb) as handle:
        Nb_date_to_person_list = json.load(handle)

    core_jaccard_data = []
    for year in range(start_year, end_year, year_window):
        core_jaccard_dic = {}
        yrange = '%s-%s'%(year, year+year_window-1)

        core_jaccard_dic['date'] = yrange

        Na_graph = returnGraph(Na_date_to_person_list, year, year+year_window-1)
        Nb_graph = returnGraph(Nb_date_to_person_list, year, year+year_window-1)

        Na_core_nodes = []
        Nb_core_nodes = []
        if len(Na_graph.nodes()) > 0:
            Na_core = nx.k_core(Na_graph)
            Na_core_nodes = list(Na_core.nodes().keys())

        if len(Nb_graph.nodes()) > 0:
            Nb_core = nx.k_core(Nb_graph)
            Nb_core_nodes = list(Nb_core.nodes().keys())

        core_jaccard_dic['jaccard_coeff'] = Jaccard_score(Na_core_nodes, Nb_core_nodes)

        core_jaccard_dic['overlap'] = list(set(Na_core_nodes).intersection(set(Nb_core_nodes)))

        core_jaccard_data.append(core_jaccard_dic)

    

    return core_periphery_data, core_jaccard_data, core_nodes


def network_growth(year_window, Na=Na, Nb=Nb):

    network_growth_data = {}
    Na_data = []
    Nb_data = []
    family_frac_data = []
    with open('app/static/json_files/%s/date_person_list.json' % Na) as handle:
            Na_date_to_person_list = json.load(handle)

    with open('app/static/json_files/%s/date_person_list.json' % Nb) as handle:
            Nb_date_to_person_list = json.load(handle)

    Na_old_graph = nx.empty_graph()
    Nb_old_graph = nx.empty_graph()

    N=10

    for year in range(start_year, end_year, year_window):
        Na_dic = {}
        Nb_dic = {}
        family_dic = {}
        year_range = str(year) + '-' + str(year+year_window-1)
        
        Na_graph_person = returnGraph(Na_date_to_person_list, start_year, year+year_window-1)
        Nb_graph_person = returnGraph(Nb_date_to_person_list, start_year, year+year_window-1)
        
        Na_new_nodes = list(set(Na_graph_person.nodes()) - set(Na_old_graph.nodes()))
        Nb_new_nodes = list(set(Nb_graph_person.nodes()) - set(Nb_old_graph.nodes()))

        Na_new_edges = list(set(Na_graph_person.edges()) - set(Na_old_graph.edges()))
        Nb_new_edges = list(set(Nb_graph_person.edges()) - set(Nb_old_graph.edges()))
        
        Na_old_graph = Na_graph_person.copy()
        Nb_old_graph = Nb_graph_person.copy()

        if len(Na_graph_person.nodes()) > 0:
            Na_node_growth = len(Na_new_nodes) / len(Na_graph_person.nodes())  
            Na_edge_growth = len(Na_new_edges) / len(Na_graph_person.edges())
        else:
            Na_node_growth = 0
            Na_edge_growth = 0
        
        if len(Nb_graph_person.nodes()) > 0:
            Nb_node_growth = len(Nb_new_nodes) / len(Nb_graph_person.nodes())  
            Nb_edge_growth = len(Nb_new_edges) / len(Nb_graph_person.edges())
        else:
            Nb_node_growth = 0
            Nb_edge_growth = 0

        Na_dic['date'] = year_range
        Na_dic['nodes'] = Na_node_growth
        Na_dic['edges'] = Na_edge_growth
        Na_dic['node_list'] = Na_new_nodes
        # Na_dic['fraction_relative'] = getFractionRelative(Na_new_nodes)

        Nb_dic['date'] = year_range
        Nb_dic['nodes'] = Nb_node_growth
        Nb_dic['edges'] = Nb_edge_growth
        Nb_dic['node_list'] = Nb_new_nodes
        # Nb_dic['fraction_relative'] = getFractionRelative(Nb_new_nodes)

        family_dic['date'] = year_range
        family_dic['Na_frac'] = getFractionRelative(Na_new_nodes)
        family_dic['Nb_frac'] = getFractionRelative(Nb_new_nodes)


        Na_data.append(Na_dic)
        Nb_data.append(Nb_dic)
        family_frac_data.append(family_dic)
        
    network_growth_data['Na'] = Na_data
    network_growth_data['Nb'] = Nb_data
    network_growth_data['family_frac_data'] = family_frac_data

    return network_growth_data


# given date dict creates and returns temporal graph
def returnWeightedGraph(date_mention_dict, start_year, end_year):
    mygraph = nx.Graph()
    for year1 in date_mention_dict.keys():
        if int(year1) < start_year or int(year1) > end_year:
            continue
        #first creating edges in the same year
        for node1 in date_mention_dict[year1]:
            for node2 in date_mention_dict[year1]:
                if node1 != node2:
                    mygraph.add_edge(node1,node2)


                    
        # now creating edges as per window
        for year2 in date_mention_dict.keys():
            if int(year2) < start_year or int(year2) > end_year:
                continue
            if int(year2) <= int(year1) or int(year2) > int(year1) + window_size:
                continue
            for node1 in date_mention_dict[year1]:
                for node2 in date_mention_dict[year2]:
                    if node1 != node2:
                        mygraph.add_edge(node1,node2)

    data = []
    for items in mygraph.edges():
        dic = {"from": items[0], "to": items[1], "value": 1}
        data.append(dic)
    return data


def get_alluvial_data(book, year_range):

    alluvial_data = {}
    N=10
    start_year = int(year_range.split('-')[0])
    end_year = int(year_range.split('-')[1])

    with open('app/static/json_files/%s/date_person_list.json' % book) as handle:
        date_to_person_list = json.load(handle)

    dic = {}
    
    graph_person = returnWeightedGraph(date_to_person_list, start_year, end_year)
    alluvial_data['date'] = year_range
    alluvial_data['alluvial'] = graph_person


    return alluvial_data
