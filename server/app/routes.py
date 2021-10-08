from app.helper import network_growth
from flask import render_template, request, redirect, session, jsonify, url_for, Blueprint, g, current_app, abort
# from flask_paginate import Pagination, get_page_parameter
from app import app, helper, evolution_connection_density, stability_measurement, core_periphery_analysis, word_shift_graph
import json
import matplotlib.pyplot as plt

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html', title="index")

@app.route('/<book>/temporal_entity_diff', methods=['GET', 'POST'])
def get_bar_plot(book):
    with open('app/static/json_files/%s/bar_chart_nodes_edges.json'%book, 'r', encoding='utf-8') as content:
        chart_data = json.load(content)
    return render_template('temporal_entity_diff.html', chart_data=chart_data)

@app.route('/<book>/graph_category', methods=['GET', 'POST'])
def get_graph_category(book):
    
    return render_template('graph_category.html', book=book)

@app.route('/connection_density', methods=['GET', 'POST'])
def get_connection_density_evolution():
    
    year_range = 5
    if request.form.get("yearWindowConnDen"):
        year_range = request.form.get("yearWindowConnDen")

    connection_density_data = helper.get_connection_density_data(year_window=int(year_range))
    cumulative_connection_density_data = helper.get_cummulative_connection_density_data(year_window=int(year_range))
    return render_template('evolution_connection_density.html', connection_density_data=connection_density_data,
     cumulative_connection_density_data=cumulative_connection_density_data, year_range=year_range)

@app.route('/stability_measurement/<method>', methods=['GET', 'POST'])
def get_stability_measurement(method):
    
    year_range = 5
    print(request.form)
    if request.form.get("yearWindowStab"):
        year_range = request.form.get("yearWindowStab")
        # return redirect('/connection_density')

    stability_measurement_data, stability_measurement_nodes = helper.get_mention_overlap(year_window=int(year_range), method=method)
    return render_template('stability_measurement.html', stability_measurement_data=stability_measurement_data,
    stability_measurement_nodes=stability_measurement_nodes, year_range=year_range, method=method)

@app.route('/core_periphery_analysis', methods=['GET', 'POST'])
def get_core_periphery_analysis():
    
    year_range = 5
    if request.form.get("yearWindowCorePeri"):
        year_range = request.form.get("yearWindowCorePeri")

    core_periphery_data, core_jaccard_data, core_nodes = helper.get_core_periphery_data(year_window=int(year_range))

    return render_template('core_periphery_analysis.html', core_periphery_data=core_periphery_data, core_jaccard_data = core_jaccard_data,
     core_nodes=core_nodes, year_range=year_range)

@app.route('/network_growth', methods=['GET', 'POST'])
def get_network_growth():
    
    year_range = 5
    if request.form.get("yearWindowNetGrowth"):
        year_range = request.form.get("yearWindowNetGrowth")

    network_growth_data = helper.network_growth(year_window=int(year_range))
    return render_template('network_growth.html', network_growth_data=network_growth_data,
     year_range=year_range)

@app.route('/alluvial/<book>/<year_range>', methods=['GET', 'POST'])
def get_alluvial_diagram(book, year_range):
    
    # year_range = 5
    # if request.form.get("yearWindowConnDen"):
    #     year_range = request.form.get("yearWindowConnDen")

    alluvial_data = helper.get_alluvial_data(book, year_range)
    return render_template('alluvial.html', book=book, alluvial_data=alluvial_data,
     year_range=year_range)

@app.route('/word_shift/<year_range>', methods=['GET', 'POST'])
def get_word_shift_graph(year_range):
    start_year = int(year_range.split('-')[0])
    end_year = int(year_range.split('-')[1])

    filename = word_shift_graph.create_word_shift(start_year, end_year)
    
    return render_template('word_shift.html', year_range=year_range, filename=filename)