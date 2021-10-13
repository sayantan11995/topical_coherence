Contains Gandhipedia related codes 

Chapters related to Story of My Experiments With Truth are in SOMEWT/

Chapters related to Hind Swaraj are in hind_swaraj/

config.json is used to: </br>
1.select book </br>
2.number of parts </br>
3.window size for temporal graphs </br>


=> Instruction for creating temporal network:

1.entity recognition nltk - identify entities using nltk
2.entity recognition polyglot - identify entities using polyglot
3.entity recognition spacy - identify entities using spacy
4.pickle combiner -> combine all entities according to majority algorithm [has manual filtering part]
	4.1 run pickle combiner to generate initial_person_list and initial_place_list
	4.2 copy/rename initial_person_list to final_person_list
	4.3 run final_list_filterer
	4.4 manually filter remaining entities inside final_person_list
	4.5 run pickle combiner again(uncommenting final_person_list section)
5.chapter time mapper -> maps chapters and entities to years
6.temporal graph creator(before running this create name_to_fullname.json) -> creates temporal graphs
7.temporal graph community detections
8.search for webapp and then search graph creator -> creates files used for search

=> Update web portal using newly created temporal network files:
Copy the required json_files, temporal_graph_files, books&chapters to gandhipedia-web

