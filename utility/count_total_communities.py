import json

books = ['Lenin_Selected_Works', 'Lenin_a_Political_Life']

for book in books:
    with open('json_files/%s/word_temporal_communities.json'%book, 'r') as content:
        temporal_community_dict = json.load(content)

    count = 0

    for year, commmunity in temporal_community_dict.items():
        count += len(commmunity)

    print(book)
    print("===========Number of Community: %s"%(count))