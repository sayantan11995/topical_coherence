import json
import matplotlib.pyplot as plt
from nltk.corpus.reader.comparative_sents import Comparison
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import itertools
import collections
# import tensorflow as tf
# import tensorflow_hub as hub
import numpy as np

# bio1 =  ['Walden', 'Jekyll', 'Rabbi Joseph Krauskopf', 'Laxmidas', 'Henry Polak', 'John Ruskin', 'Harilal', 'Devadas', 'Habib', 'Maganlalbhai', 'Lawley', 'Ramdas', 'Anderson Streets', 'Chamney', 'Hyde', 'Jan Christian Smuts', 'Joseph Chamberlain', 'Kachhalia', 'Rissik', 'Chertkov', 'Thomas G. Masaryk', 'Buller', 'Olive Schreiner', 'Leo Tolstoy', 'Lutavasinh', 'Alexander Herzen', 'Albert West', 'Chanchi', 'Dadabhai Naoroji', 'Jane Addams', 'Botha', 'Manilal', 'Anna Karenina', 'Sorabji Shapurji Adajania', 'Herman Kallenbach', 'Annie Besant', 'Brahmacharya', 'Sonya Schlesin', 'Max Mueller', 'William Lloyd Garrison', 'William Jennings Bryan', 'Kasturbai', 'J. J. Doke', 'Sheik Mehtab', 'Badri', 'Ralph Waldo Emerson', 'Albert Cartwright', 'Doke', 'Lokamanya Tilak', 'Mir Alam', 'Gani', 'Maganlal', 'Willie', 'Elgin', 'Manilal Gandhi']
# bio2 = ['Namboodiripad', 'Albert Cartwright', 'Edward Carpenter', 'Abraham Lincoln', 'Raymond Aron', 'J. C. Smuts', 'Mahadev Govind Ranade', 'Shyamaji Krishnavarma', 'Jameson', 'Jayshanker Govindji', 'Bhagawan', 'Jayakunwar', 'Merriman', 'Maulvi Mukhtiar', 'Dadabhai Naoroji', 'Joan', 'Maulvi Sahib', 'Narajana Apanna', 'Wolstenholme', 'Nanalal Shah', 'Thambi', 'Shivaji', 'Tolstoyans', 'Pillay', 'Booker T. Washington', 'Taraknath Das', 'Swami Shankeranand', 'Fingo', 'Thomas Carlyle', 'Manilal Doctor', 'Charles Phillips', 'Ahmed Mahomed Cachalia', 'Lewis Ritch', 'Laxmidas', 'Adolf', 'Chanchal Gandhi', 'Arnott', 'Vijaya Dashami', 'Gregorowski', 'Rabindranath Tagore', 'Bloemhof', 'Percy Fitzpatrick', 'Winston Churchill', 'Curzon Wyllie', 'Madan Lal Dhingra', 'Sheikh Mehtab', 'Ananda', 'Cape Colony', 'Bal Gangadhar Tilak', 'John Dube', 'Rosa Luxemburg', 'Table Mountain', 'Kaka', 'Bada Bhai', 'Henry Cotton', 'Nazar', 'Madanjit Vyavaharik', 'Savarkar', 'Het Volk', 'Xiabao', 'Mohandas K. Gandhi', 'Chhaganlal', 'Bapu', 'Harilal Mohandas Gandhi', 'Dawad Mahomed', 'Purushottamdas Desai', 'Chhota Bhai', 'Kaba Gandhi', 'Mudholkar', 'Shapurji Sorabjee', 'Lords Morley', 'Ampthill', 'Gujarati Hindus', 'Akbar', 'Nagappen', 'Pixley Seme', 'Gandhi Abdurahman', 'Alfred Milner', 'Gujarati Muslim', 'Polaks', 'Tata', 'Naidoo', 'Adam Mahomed', 'Wybergh', 'Mazharul', 'Chessell', 'Kabir', 'Laxman', 'Aswat', 'Lord Milner', 'George Washington', 'Narayanaswamy', 'Imam Abdul Kadir', 'Hind Swaraj', 'George Birdwood', 'Maxim Gorky', 'John L. Dube', 'Ramabhai Sodha', 'Abdullah Abdurahman', 'Punditji', 'Aligarh', 'Sorabji', 'Saraswati', 'Gulam Mahomed', 'Ranade', 'Ernest Howard Crosby', 'Manilal Gandhi', 'Sydney Webb', 'African Chronicle', 'Aylmer Maude', 'Karsandas', 'Jamshedji Tata', 'Selborne', 'Abdurrahman', 'Devadas', 'Hatem', 'Gandhiji', 'Raychandbhai', 'Eleanor Marx', 'Hetereodox', 'Alfred Lyttelton', 'Khamisa', 'Ram Sundar Pandit', 'Edgar Snow', 'William Hosken', 'Jan H. Hofmeyr', 'Sri Aurobindo', 'Ahmed Mahommed Cachalia', 'Miss Mayo', 'Bhai', 'Henry David Thoreau', 'Kasturba Gandhi', 'Bharatavarsha', 'Curzon', 'Ritch', 'Gautama Buddha', 'Edward Dallow', 'Mahavira', 'Maganlal Gandhi', 'Lawson', 'Tamil William Godfrey', 'Elgin', 'Patrick Duncan', 'Karl Marx', 'John Bunyan', 'Harold Cox', 'Haque', 'Jan Christian Smuts', 'John Buchan', 'Rustomjee', 'Lady Margaret Hospital', 'Hassim Jooma', 'Henry Salt', 'Satyavan', 'Lourenço Marques', 'Anna Kingsford', 'Abdul Gani', 'Parsee Rustomjee', 'Moulvi Saheb Ahmed Mukhtiar', 'John Cordes', 'Mrs Sodha', 'Sorabji Adajania', 'Madras Polak', 'Adam Smith', 'Nadeshir Cama', 'Chanchal', 'Mrs Packirsamy', 'Ramsamy Moodlai', 'Rana Pratap', 'David Pollock', 'Joseph Chamberlain', 'Petit', 'Mrs Vogt', 'Khune', 'Parcere', 'Neame', 'Mahomedan', 'Lajpat Rai', 'Imam Abdul Kadir Bawazeer', 'Nizam', 'Jesus Christ', 'Cecil', 'Barindranath', 'Hindu Maharajas', 'Aiyar', 'Gertrude', 'Maganlal', 'Essop Mia', 'Mrs Nanji', 'Meer Allam Khan', 'Dinizulu', 'Joseph Royeppen', 'Lepel', 'George Allen', 'Captain Fowle', 'Pranjivan Mehta', 'Mohammed Ali Jinnah', 'Jeki', 'Millie Graham', 'Easton', 'Mahomedans', 'Lord Crewe', 'Govardhanram Tripathi', 'Modh Banias', 'Alfred Lawley', 'Joseph Doke', 'Natesan', 'Sammy Marks', 'Harilal Gandhi', 'Rustamjee', 'Savitri', 'Spion Kop', 'Isabella Fyvie Mayo', 'Maud Polak', 'Louis Botha', 'Montford Chamney', 'Meyer', 'Henry Polak', 'Kasturba', 'Jan Smuts', 'Vinayak Damodar Savarkar', 'Millie Polak', 'William Vogl', 'Rustomjee Jeevanjee', 'Habib Motan', 'Frederick Lely', 'Chanchi', 'Madanlal Dhingra', 'Klerksdorf', 'Liu', 'Leung Quinn', 'Lala Bahadur Singh', 'Eastern Europe', 'Mrs Amacanoo', 'Sonja Schlesin', 'Harilal', 'Friedrich Engels', 'Cape Comorin', 'Flora Shaw', 'Fox Street', 'Aurobindo Ghose', 'Draft Ordinance', 'Khushalchand', 'Mohandas Gandhi', 'Herbert Spencer', 'Amir Ali', 'Ravan', 'Nawab Khan', 'John Ruskin', 'Asari', 'Albert West', 'Gokuldas', 'James D. Hunt', 'Dokes', 'Raja Bhoja', 'Banias', 'Ramdas', 'Dawood Mahomed', 'Abraham Fischer', 'Haridas Vora', 'Bhishma', 'Volksrust Prison', 'Besant', 'Veerammal', 'Ghandi', 'John Stuart Mill', 'Vyas', 'Madame Blavatsky', 'Henry Solomon Leon Polak', 'Chhaganlal Gandhi', 'Vartaman', 'Olive Schreiner', 'Mohandas Karamchand Gandhi', 'Saddarshan Samuccaya', 'Gopal Krishna Gokhale', 'Narmadashanker', 'Mancherjee Bhownaggree', 'Leo Tolstoy', 'Gabriel Isaacs', 'Joseph J. Doke', 'Hermann Kallenbach', 'Mohanchand', 'Vogl', 'Mao Zedong', 'Saul Dubow', 'Ratan Tata', 'Martin Luther', 'Hajee Habib', 'Mrs Gandhi', 'Tulsidas', 'Sigmund Freud', 'Nanji', 'Josiah Oldfield', 'Ishwarchandra Vidyasagar', 'George Bernard Shaw', 'Maulvi Ahmed Mukhtiar', 'Jamshetjee', 'Ramdas Gandhi', 'Ram Sundar Pundit', 'Gabriel I. Isaac', 'Adajania']

# autobio = ['Shankarlal Parikh', 'Brajkishorebabu', 'Hasrat Saheb', 'Shrimatis Avantikabai', 'Kalelkar', 'Abbas', 'Shrimati Anandibai', 'Jehangir Petit', 'Thakkar Bapa', 'Ambalal Sarabhai', 'Deshabandhu', 'Gaya Babu', 'Crewe', 'Jivanlal', 'Gorakhbabu', 'Devdas', 'Jagadanandbabu', 'Kripalani', 'Shrimati Durga Desai', 'Jivraj Mehta', "Michael O'Dwyer", 'Kakasaheb', 'Patwardhan', 'Satyapal', 'Babu Dharanidhar Prasad', 'Rajkumar Shukla', 'Phadke', 'Sinha', 'Ramibai Kamdar', 'Chhaganlal Gandhi', 'Chintaman', 'Lakshmidas', 'Kasturbai', 'Ramnavmi Prasad', 'Punjabhai', 'Mahadev Desai', 'Maulana Mazharul Haq', 'Amritlal Thakkar', 'Manilal', 'Motilalji', 'Babasaheb Soman', 'Yashvantprasad Desai', 'Rajendra Babu', 'Chhotalal', 'Mahatma Munshiramji', 'Keshavrao Deshpande', 'Vaidyanathadham', 'Mohanlal', 'Kelkar', 'Sushil Rudra', 'Gangadharrao', 'Dada Abdulla', 'Sharadbabu', 'Shrimati Vasumatibehn', 'Ramdas', 'Chelmsford', 'Maulana Abdul Bari Saheb', 'Hakim Saheb', 'Malkani', 'Brajkishore Babu', 'Pearson', 'Polak', 'Janakdharibabu', 'Choithram', 'Jayakar', 'Kaul', 'Umar Sobani', 'Malaviyaji', 'Edward Gait', 'Danibehn', 'Brijkishore', 'Lala Harkishanlal', 'Jeramdas', 'Gokhale', 'Bepin', 'Harihar Sharma', 'Shambhaubabu', 'Acharya Ramadevji', 'Shivji', 'Sorabji Adajania', 'Kitchlu', 'Babu Brajkishore Prasad', 'Kuhne', 'Babu Bhupendranath Basu', 'Nagenbabu', 'Gangabehn Majmundar', 'Hakim Ajmal Khan Saheb']

def Jaccard_score(lista_1, lista_2):    
    inter = len(list(set(lista_1) & set(lista_2)))
    union = len(list(set(lista_1) | set(lista_2)))
    print(list(set(lista_1) & set(lista_2)))
    if union <=0:
        return 0
    else:
        return inter/union

autobio = {'Rajkumar Shukla': 85, 'Babu Brajkishore Prasad': 85, 'Rajendra Babu': 85, 'Babu Bhupendranath Basu': 85, 'Kasturbai': 85, 'Jehangir Petit': 85, 'Yashvantprasad Desai': 85, "Michael O'Dwyer": 85, 'Kelkar': 85, 'Chhaganlal Gandhi': 85}
bio1 = {'Kasturba': 31, 'Botha': 31, 'Jan Christian Smuts': 31, 'Henry Polak': 31, 'Manilal': 31, 'Ramdas': 31, 'Devadas': 31, 'Harilal': 31, 'Walden': 31, 'Albert Cartwright': 31, 'Herman Kallenbach': 31}
bio2 = {'Kasturba': 150, 'Rustomjee': 150, 'Joseph Chamberlain': 150, 'Lord Milner': 150, 'Albert West': 150, 'Josiah Oldfield': 150, 'Henry Polak': 150, 'Chhaganlal': 150, 'Sheikh Mehtab': 150, 'Herman Kallenbach': 150}

# print(list(set(bio2).intersection(set(bio1))))

# print(Jaccard_score(autobio.keys(), bio1.keys()))
# print(Jaccard_score(autobio.keys(), bio2.keys()))
# print(Jaccard_score(bio1.keys(), bio2.keys()))

common_name = ['Ramdas', 'Kasturbai', 'Manilal']
new_nodes_autobio =  ['Shankarlal Parikh', 'Brajkishorebabu', 'Hasrat Saheb', 'Shrimatis Avantikabai', 'Kalelkar', 'Abbas', 'Shrimati Anandibai', 'Jehangir Petit', 'Thakkar Bapa', 'Ambalal Sarabhai', 'Deshabandhu', 'Gaya Babu', 'Crewe', 'Jivanlal', 'Gorakhbabu', 'Devdas', 'Jagadanandbabu', 'Kripalani', 'Shrimati Durga Desai', 'Jivraj Mehta', "Michael O'Dwyer", 'Kakasaheb', 'Patwardhan', 'Satyapal', 'Babu Dharanidhar Prasad', 'Rajkumar Shukla', 'Phadke', 'Sinha', 'Ramibai Kamdar', 'Chhaganlal Gandhi', 'Chintaman', 'Lakshmidas', 'Kasturbai', 'Ramnavmi Prasad', 'Punjabhai', 'Mahadev Desai', 'Maulana Mazharul Haq', 'Amritlal Thakkar', 'Manilal', 'Motilalji', 'Babasaheb Soman', 'Yashvantprasad Desai', 'Rajendra Babu', 'Chhotalal', 'Mahatma Munshiramji', 'Keshavrao Deshpande', 'Vaidyanathadham', 'Mohanlal', 'Kelkar', 'Sushil Rudra', 'Gangadharrao', 'Dada Abdulla', 'Sharadbabu', 'Shrimati Vasumatibehn', 'Ramdas', 'Chelmsford', 'Maulana Abdul Bari Saheb', 'Hakim Saheb', 'Malkani', 'Brajkishore Babu', 'Pearson', 'Polak', 'Janakdharibabu', 'Choithram', 'Jayakar', 'Kaul', 'Umar Sobani', 'Malaviyaji', 'Edward Gait', 'Danibehn', 'Brijkishore', 'Lala Harkishanlal', 'Jeramdas', 'Gokhale', 'Bepin', 'Harihar Sharma', 'Shambhaubabu', 'Acharya Ramadevji', 'Shivji', 'Sorabji Adajania', 'Kitchlu', 'Babu Brajkishore Prasad', 'Kuhne', 'Babu Bhupendranath Basu', 'Nagenbabu', 'Gangabehn Majmundar', 'Hakim Ajmal Khan Saheb']

books = ['SOMEWT', 'Life_of_Mahatma_Gandhi', 'Gandhi_Before_India', 
'Jawaharlal_Nehru_Autobiography', 'Jawaharlal_Nehru_a_Biography',
'Abraham_Lincoln_Autobiography', 'Life_of_Abraham_Lincoln',
'Lenin_Selected_Works', 'Lenin_a_Political_Life']

sentences = ""

start_year = 1913
end_year = 1917
with open("app/static/json_files/%s/year_chapter_chaptername_dict.json"%books[3], 'r', encoding="utf-8") as content:
    year_chapter = json.load(content)

for year in year_chapter.keys():
    if int(year) >= start_year and int(year) <= end_year:
        for chapter_list in year_chapter[year]: 
            part = chapter_list[0]
            chap = chapter_list[1]
            with open("app/static/text_books/%s/part%s/chapter%s.txt"%(books[3], part, chap), 'r', encoding='utf-8') as f:
                sentences += " " + f.read()

stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(sentences)

stop_words.update(["'s","u", "sometimes", "firom", "g", "even", "many", "p", "pp", "w", "us", "said", "told", "came", "come", "became", "dr", "go", "sjt", "co", "un", "one", "might", "must", 
'january','feb','march','april','may','june','july','august','september','october','november','december', 'vol',
'th', 'thoreau'])
filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
# print(filtered_sentence)
# word_cloud = WordCloud(collocations = True).generate(" ".join(filtered_sentence))
# plt.imshow(word_cloud, interpolation='bilinear')
# plt.axis("off")
# plt.show()




sentences1 = ""

start_year = 1903
end_year = 1912
with open("app/static/json_files/%s/year_chapter_chaptername_dict.json"%books[4], 'r', encoding="utf-8") as content:
    year_chapter = json.load(content)

for year in year_chapter.keys():
    if int(year) >= start_year and int(year) <= end_year:
        for chapter_list in year_chapter[year]: 
            part = chapter_list[0]
            chap = chapter_list[1]
            with open("app/static/text_books/%s/part%s/chapter%s.txt"%(books[4], part, chap), 'r', encoding='utf-8') as f:
                sentences1 += " " + f.read()

def remove_punctuation(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

def  clean_text(txt):
    tmp = [remove_punctuation(t) for t in txt]
    # print(tmp)
    tmp = [t.lower().split() for t in tmp]
    
    tmp = [[w for w in t if not w in stop_words]
              for t in tmp]
    tmp = [[w for w in t if not w in ['gandhi']]
                     for t in tmp]
    
    tmp = list(itertools.chain(*tmp))
    tmp = collections.Counter(tmp)
    return tmp

sentences = re.sub(r'[0-9]', '', sentences)
sentences1 = re.sub(r'[0-9]', '', sentences1)
text1 = clean_text(sentences.split("."))
text2 = clean_text(sentences1.split("."))

import shifterator as sh
from shifterator import shifts as ss

jsd_shift = ss.JSDivergenceShift(type2freq_1=text1,
                                type2freq_2=text2)

pic = jsd_shift.get_shift_graph(top_n=50, show_plot=False)

print(type(pic))
# plt.show()
# pic.plot(range(5), range(5), "ro-")

# plot_path = 'app/static/images/word_shift_graph_%s_%s.png'%(start_year, end_year)
# plt.savefig(plot_path)

# module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
# model = hub.load(module_url)

from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
# from sentence_transformers import SentenceTransformer
# sbert_model = SentenceTransformer('bert-base-nli-max-tokens' )


# auto_bio_embedding = sbert_model.encode(sentences)
# bio_embedding = sbert_model.encode(sentences1)

# print(cosine_similarity(auto_bio_embedding, bio_embedding))

# print(1 - spatial.distance.cosine(auto_bio_embedding, bio_embedding))

with open('sent.txt', 'w', encoding='utf-8') as content:
    content.write(sentences)
# print(sentences)

from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

# vectorizer = TfidfVectorizer(stop_words='english')
# X = vectorizer.fit_transform(word_tokenize(sentences))
# X = X.todense()
# print(X)
# X = sbert_model.encode([sentences, sentences1])


# from sklearn.cluster import KMeans

# NUMBER_OF_CLUSTERS = 2
# km = KMeans(
#     n_clusters=NUMBER_OF_CLUSTERS, 
#     init='k-means++', 
#     max_iter=500)
# km.fit(X)

# pca = PCA(n_components=2)
# two_dim = pca.fit_transform(X)

# scatter_x = two_dim[:, 0] # first principle component
# scatter_y = two_dim[:, 1] # second principle component
# print(scatter_x)


# plt.style.use('ggplot')

# fig, ax = plt.subplots()
# fig.set_size_inches(20,10)

# # color map for NUMBER_OF_CLUSTERS we have
# cmap = {0: 'green', 1: 'blue'}

# # First: for every document we get its corresponding cluster
# clusters = km.predict(X)

# # group by clusters and scatter plot every cluster
# # with a colour and a label
# for group in np.unique(clusters):
#     ix = np.where(clusters == group)
#     ax.scatter(scatter_x[ix], scatter_y[ix], c=cmap[group], label=group)

# ax.legend()
# plt.xlabel("PCA 0")
# plt.ylabel("PCA 1")
# plt.show()

# order_centroids = km.cluster_centers_.argsort()[:, ::-1]

# terms = vectorizer.get_feature_names()
# for i in range(NUMBER_OF_CLUSTERS):
#     print("Cluster %d:" % i, end='')
#     for ind in order_centroids[i, :10]:
#         print(' %s' % terms[ind], end='')
#     print()