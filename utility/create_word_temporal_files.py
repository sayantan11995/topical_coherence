import re  # For preprocessing
import json
import pandas as pd  # For data handling
from time import time  # To time our operations
from collections import defaultdict  # For word frequency



# books = ['SOMEWT', 'Gandhi_Before_India']
# start_year_list, end_year_list = [1888, 1893, 1898, 1903, 1908, 1913, 1918], [1892, 1897, 1902, 1907, 1912, 1917, 1922]

books = ['Lenin_Selected_Works', 'Lenin_a_Political_Life']
start=1890
end=1914
year_window=5


start_year_list = [x for x in range(start, end, year_window)]
end_year_list = [x+year_window-1 for x in start_year_list]

bio_dic = {}
autobio_dic = {}
for start_year, end_year in zip(start_year_list, end_year_list):
    sentences_autobio = ""
    with open("json_files/%s/year_chapter_chaptername_dict.json"%books[0], 'r', encoding="utf-8") as content:
        year_chapter = json.load(content)

    for year in year_chapter.keys():
        if int(year) >= start_year and int(year) <= end_year:
            for chapter_list in year_chapter[year]: 
                part = chapter_list[0]
                chap = chapter_list[1]
                with open("%s/part%s/chapter%s.txt"%(books[0], part, chap), 'r', encoding='utf-8') as f:
                    sentences_autobio += " " + f.read()

    sentences_bio = ""

    with open("json_files/%s/year_chapter_chaptername_dict.json"%books[1], 'r', encoding="utf-8") as content:
        year_chapter = json.load(content)

    for year in year_chapter.keys():
        if int(year) >= start_year and int(year) <= end_year:
            for chapter_list in year_chapter[year]: 
                part = chapter_list[0]
                chap = chapter_list[1]
                with open("%s/part%s/chapter%s.txt"%(books[1], part, chap), 'r', encoding='utf-8') as f:
                    sentences_bio += " " + f.read()


    sentences_autobio = re.sub(r'[0-9]', '', sentences_autobio)
    sentences_bio = re.sub(r'[0-9]', '', sentences_bio)

    bio_dic[str(start_year)+ '-' + str(end_year)] = sentences_bio
    autobio_dic[str(start_year)+ '-' + str(end_year)] = sentences_autobio


with open("json_files/%s/temporal_word_list.json"%books[0], 'w', encoding="utf-8") as content:
    json.dump(autobio_dic, content, indent=4)
with open("json_files/%s/temporal_word_list.json"%books[1], 'w', encoding="utf-8") as content:
    json.dump(bio_dic, content, indent=4)