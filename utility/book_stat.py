import nltk
import os
import fnmatch
import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

stop = set( list(string.punctuation))


with open('config.json') as handle:
    config = json.load(handle)
book = config['book_name']
Parts = config['number_of_parts']
dir_path = './%s/part'% book

txt = ''
total_chapters = 0

for part in range(1,Parts+1):
    
    x = 1
    print(dir_path + str(part) + '/')
    no_of_chapters = len(fnmatch.filter(os.listdir(dir_path + str(part) + '/'), '*.txt'))
    print('no.of_chapters:' + str(no_of_chapters))
    print('part:' + str(part))
    total_chapters += no_of_chapters
    while x <= no_of_chapters:
        
        target_x = no_of_chapters+1
        # print('chapters' + str(x) + ' to ' + str(target_x) )
        for i in range(x,target_x):
            with open(dir_path + str(part) + '/chapter'+ str(i) + '.txt', 'r', encoding='utf-8') as content_file:
                content = content_file.read()
            
            txt += content
                    
            

        
        x = target_x

sentences = nltk.sent_tokenize(txt)
words = [i for i in word_tokenize(txt.lower()) if i not in stop]

# print(sentences[:5])
print("Chapters: %s"%total_chapters)
print("Number of sentences: %s" %len(sentences))
# print(words[:10])
print("Number of words: %s" %len(words))
print("Unique words: %s"%len(set(words)))