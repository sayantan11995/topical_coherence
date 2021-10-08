import json
biography_words = ['hailey', 'league', 'motilal', 'dept', 'pol', 'imperialism', 'aicc', 'independence', 'organization',
'papers', 'secretary', 'british', 'soviet', 'communist', 'china', 'fight', 'kisans', 'chinese', 'emerson', 'support',
'willingdon', 'jail', 'settlement', 'union', 'brussels', 'capitalism']

autobiography_word = ['Gandhiji', 'Gaol', 'Organisation', 'people', 'physical', 'peasantry', 'prison', 'languages']

books = ['SOMEWT', 'Life_of_Mahatma_Gandhi', 'Gandhi_Before_India', 
'Jawaharlal_Nehru_Autobiography', 'Jawaharlal_Nehru_a_Biography',
'Abraham_Lincoln_Autobiography', 'Life_of_Abraham_Lincoln',
'Lenin_Selected_Works', 'Lenin_a_Political_Life']

bio_topic_text = []

start_year = 1927
end_year = 1931
with open("app/static/json_files/%s/year_chapter_chaptername_dict.json"%books[3], 'r', encoding="utf-8") as content:
    year_chapter = json.load(content)

for year in year_chapter.keys():
    if int(year) >= start_year and int(year) <= end_year:
        for chapter_list in year_chapter[year]: 
            part = chapter_list[0]
            chap = chapter_list[1]
            with open("app/static/text_books/%s/part%s/chapter%s.txt"%(books[3], part, chap), 'r', encoding='utf-8') as f:
                sentences = f.read().split(".")
            
            for word in biography_words:
                for sent in sentences:
                    if word in sent: 
                        bio_topic_text.append(sent)

print(bio_topic_text)


import nltk

sent_tok = nltk.sent_tokenize(bio_topic_text)

sent_tok