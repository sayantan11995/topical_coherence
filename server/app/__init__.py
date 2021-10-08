from flask import Flask, request, g, redirect, url_for, session, send_from_directory
from flask_babel import Babel
import os
# import pymysql as PyMySQL
# import pymysql.cursors

app = Flask(__name__)

from app import index, routes,  timeline_chordials, evolution_connection_density, helper, \
stability_measurement, core_periphery_analysis, word_shift_graph