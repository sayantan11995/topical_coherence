from flask import render_template, request, redirect, session, jsonify, url_for, Blueprint, g, current_app, abort
# from flask_paginate import Pagination, get_page_parameter
from app import app
import json
import os

year_window = 3
start_year = 1888
end_year = 1924

@app.route('/<book>/timeline_chordials', methods=['GET', 'POST'])
def get_timeline_chordials(book):
    graph_data_path = 'app/static/graph_data/%s/' % book
    chart_data_list = []
    year_range_list = []
    for year in range(start_year, end_year, year_window):
        
        file_name = 'graph_person_startyear_' + str(year) + '_endyear_' + str(year+year_window-1) + '.json'

        with open(os.path.join(graph_data_path, file_name), 'r', encoding='utf-8') as content:
            chart_data = json.load(content)

        chart_data_list.append(chart_data) 
        year_range_list.append('%s-%s'%(year, year+year_window-1))
    return render_template('chord.html', chart_data_list=chart_data_list, year_range_list=year_range_list)