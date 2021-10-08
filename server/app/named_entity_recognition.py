import spacy
import pickle
from pprint import pprint 
from spacy import displacy
from collections import Counter
import en_core_web_sm
import os, os.path
import fnmatch
import json

nlp = en_core_web_sm.load()
chapter_entities_map = {}
entity_list_map = {}
notation_int_map = {}

# 0 = PERSON 1 = PLACE
notation_int_map['PERSON'] = 0
notation_int_map['GPE'] = 1
notation_int_map['FAC'] = 1
notation_int_map['LOC'] = 1

with open("app/static/json_files/year_event.json", 'r', encoding="utf-8") as content:
    year_event = json.load(content)

year_event_person = {}

for year, events in year_event.items():
    doc = nlp(" ".join(events)) 
    year_event_person[year] = set()
    for ent in doc.ents:
        # print(ent.text, ent.start_char, ent.end_char, ent.label_)

        if ent.label_ not in notation_int_map.keys():
            continue
        if ent.label_ == "PERSON":
            year_event_person[year].add(ent.text)
    year_event_person[year] = list(year_event_person[year])
        # print(ent.text, ent.start_char, ent.end_char, ent.label_)
    #     chapter_entities_map[part][i].add(ent.text)
    #     if ent.text not in entity_list_map[part].keys():
    #         entity_list_map[part][ent.text] = []  
    #     entity_list_map[part][ent.text].append(notation_int_map[ent.label_])
    # chapter_entities_map[part][i] = list(chapter_entities_map[part][i])

with open("app/static/json_files/year_event_person.json", 'w') as content:
    json.dump(year_event_person, content, indent=4 )