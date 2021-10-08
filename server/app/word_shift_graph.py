import json, os
import matplotlib.pyplot as plt
from nltk.corpus.reader.comparative_sents import Comparison
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import itertools
import collections

books = ['SOMEWT', 'Life_of_Mahatma_Gandhi', 'Gandhi_Before_India', 'Jawaharlal_Nehru_Autobiography', 'Jawaharlal_Nehru_a_Biography']

stop_words = set(stopwords.words('english'))
# word_tokens = word_tokenize(sentences_autobio)

stop_words.update(["'s","u", "sometimes", "firom", "g", "even", "many", "p", "pp", "w", "us", "said", "told", "came", "come", "became", "dr", "go", "sjt", "co", "un", "one", "might", "must", 
'january','feb','march','april','may','june','july','august','september','october','november','december', 'vol', 'mr', 'k', 'self', 'thy', 'thus', 'west',
'end', 'tion', 'th', 'used', 'location', 'indians', 'indian', 'wrote', 'already', 'con', 'ment', 'whils', 'work', 'also', 'could', 'know', 'learnt', 'spite',
'see', 'get', 'beginning', 'ing', 'east', 'felt', 'take', 'tie'])


# filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
# print(filtered_sentence)
# word_cloud = WordCloud(collocations = True).generate(" ".join(filtered_sentence))
# plt.imshow(word_cloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()



def remove_punctuation(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

def  clean_text(txt):
    tmp = [remove_punctuation(t) for t in txt]
    print(tmp)
    tmp = [t.lower().split() for t in tmp]
    
    tmp = [[w for w in t if not w in stop_words]
              for t in tmp]
    tmp = [[w for w in t if not w in ['gandhi']]
                     for t in tmp]
    
    tmp = list(itertools.chain(*tmp))
    tmp = collections.Counter(tmp)
    return tmp

def create_word_shift(start_year, end_year):
    
    sentences_autobio = ""
    with open("app/static/json_files/%s/year_chapter_chaptername_dict.json"%books[0], 'r', encoding="utf-8") as content:
        year_chapter = json.load(content)

    for year in year_chapter.keys():
        if int(year) >= start_year and int(year) <= end_year:
            for chapter_list in year_chapter[year]: 
                part = chapter_list[0]
                chap = chapter_list[1]
                with open("app/static/text_books/%s/part%s/chapter%s.txt"%(books[0], part, chap), 'r', encoding='utf-8') as f:
                    sentences_autobio += " " + f.read()

    sentences_bio = ""

    with open("app/static/json_files/%s/year_chapter_chaptername_dict.json"%books[1], 'r', encoding="utf-8") as content:
        year_chapter = json.load(content)

    for year in year_chapter.keys():
        if int(year) >= start_year and int(year) <= end_year:
            for chapter_list in year_chapter[year]: 
                part = chapter_list[0]
                chap = chapter_list[1]
                with open("app/static/text_books/%s/part%s/chapter%s.txt"%(books[1], part, chap), 'r', encoding='utf-8') as f:
                    sentences_bio += " " + f.read()

    
    sentences_autobio = re.sub(r'[0-9]', '', sentences_autobio)
    sentences_bio = re.sub(r'[0-9]', '', sentences_bio)
    text1 = clean_text(sentences_autobio.split("."))
    text2 = clean_text(sentences_bio.split("."))

    import shifterator as sh
    from shifterator import shifts as ss

    jsd_shift = ss.JSDivergenceShift(type2freq_1=text1,
                                    type2freq_2=text2)

    ax = jsd_shift.get_shift_graph(top_n=50, show_plot=False)
    filename = 'word_shift_graph_%s_%s.png'%(start_year, end_year)
    plt.savefig(os.path.join('app/static/images', filename))
    return filename

# print(type(pic))
# plt.show()
# pic.figure