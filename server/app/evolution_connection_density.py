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




def get_connection_density_data(year_window):

    connection_density_data = {}
    N=10

    for book in book_list:
        with open('app/static/json_files/%s/date_person_list.json' % book) as handle:
            date_to_person_list = json.load(handle)

        connection_density = []
        for year in range(start_year, end_year, year_window):
            dic = {}
            
            graph_person = helper.returnGraph(date_to_person_list, year, year+year_window-1)

            dic['date'] = '%s-%s'%(year, year+year_window-1)
            dic['conn_den'] = nx.density(graph_person)
            dic['nodes'] = len(graph_person.nodes())
            connection_density.append(dic)

        connection_density_data[book] = connection_density

    return connection_density_data


