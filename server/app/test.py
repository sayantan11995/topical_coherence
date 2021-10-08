import json
import matplotlib.pyplot as plt
from nltk.corpus.reader.comparative_sents import Comparison
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import itertools
import collections
from fuzzywuzzy import fuzz

# bio1 =  ['Walden', 'Jekyll', 'Rabbi Joseph Krauskopf', 'Laxmidas', 'Henry Polak', 'John Ruskin', 'Harilal', 'Devadas', 'Habib', 'Maganlalbhai', 'Lawley', 'Ramdas', 'Anderson Streets', 'Chamney', 'Hyde', 'Jan Christian Smuts', 'Joseph Chamberlain', 'Kachhalia', 'Rissik', 'Chertkov', 'Thomas G. Masaryk', 'Buller', 'Olive Schreiner', 'Leo Tolstoy', 'Lutavasinh', 'Alexander Herzen', 'Albert West', 'Chanchi', 'Dadabhai Naoroji', 'Jane Addams', 'Botha', 'Manilal', 'Anna Karenina', 'Sorabji Shapurji Adajania', 'Herman Kallenbach', 'Annie Besant', 'Brahmacharya', 'Sonya Schlesin', 'Max Mueller', 'William Lloyd Garrison', 'William Jennings Bryan', 'Kasturbai', 'J. J. Doke', 'Sheik Mehtab', 'Badri', 'Ralph Waldo Emerson', 'Albert Cartwright', 'Doke', 'Lokamanya Tilak', 'Mir Alam', 'Gani', 'Maganlal', 'Willie', 'Elgin', 'Manilal Gandhi']
# bio2 = ['Namboodiripad', 'Albert Cartwright', 'Edward Carpenter', 'Abraham Lincoln', 'Raymond Aron', 'J. C. Smuts', 'Mahadev Govind Ranade', 'Shyamaji Krishnavarma', 'Jameson', 'Jayshanker Govindji', 'Bhagawan', 'Jayakunwar', 'Merriman', 'Maulvi Mukhtiar', 'Dadabhai Naoroji', 'Joan', 'Maulvi Sahib', 'Narajana Apanna', 'Wolstenholme', 'Nanalal Shah', 'Thambi', 'Shivaji', 'Tolstoyans', 'Pillay', 'Booker T. Washington', 'Taraknath Das', 'Swami Shankeranand', 'Fingo', 'Thomas Carlyle', 'Manilal Doctor', 'Charles Phillips', 'Ahmed Mahomed Cachalia', 'Lewis Ritch', 'Laxmidas', 'Adolf', 'Chanchal Gandhi', 'Arnott', 'Vijaya Dashami', 'Gregorowski', 'Rabindranath Tagore', 'Bloemhof', 'Percy Fitzpatrick', 'Winston Churchill', 'Curzon Wyllie', 'Madan Lal Dhingra', 'Sheikh Mehtab', 'Ananda', 'Cape Colony', 'Bal Gangadhar Tilak', 'John Dube', 'Rosa Luxemburg', 'Table Mountain', 'Kaka', 'Bada Bhai', 'Henry Cotton', 'Nazar', 'Madanjit Vyavaharik', 'Savarkar', 'Het Volk', 'Xiabao', 'Mohandas K. Gandhi', 'Chhaganlal', 'Bapu', 'Harilal Mohandas Gandhi', 'Dawad Mahomed', 'Purushottamdas Desai', 'Chhota Bhai', 'Kaba Gandhi', 'Mudholkar', 'Shapurji Sorabjee', 'Lords Morley', 'Ampthill', 'Gujarati Hindus', 'Akbar', 'Nagappen', 'Pixley Seme', 'Gandhi Abdurahman', 'Alfred Milner', 'Gujarati Muslim', 'Polaks', 'Tata', 'Naidoo', 'Adam Mahomed', 'Wybergh', 'Mazharul', 'Chessell', 'Kabir', 'Laxman', 'Aswat', 'Lord Milner', 'George Washington', 'Narayanaswamy', 'Imam Abdul Kadir', 'Hind Swaraj', 'George Birdwood', 'Maxim Gorky', 'John L. Dube', 'Ramabhai Sodha', 'Abdullah Abdurahman', 'Punditji', 'Aligarh', 'Sorabji', 'Saraswati', 'Gulam Mahomed', 'Ranade', 'Ernest Howard Crosby', 'Manilal Gandhi', 'Sydney Webb', 'African Chronicle', 'Aylmer Maude', 'Karsandas', 'Jamshedji Tata', 'Selborne', 'Abdurrahman', 'Devadas', 'Hatem', 'Gandhiji', 'Raychandbhai', 'Eleanor Marx', 'Hetereodox', 'Alfred Lyttelton', 'Khamisa', 'Ram Sundar Pandit', 'Edgar Snow', 'William Hosken', 'Jan H. Hofmeyr', 'Sri Aurobindo', 'Ahmed Mahommed Cachalia', 'Miss Mayo', 'Bhai', 'Henry David Thoreau', 'Kasturba Gandhi', 'Bharatavarsha', 'Curzon', 'Ritch', 'Gautama Buddha', 'Edward Dallow', 'Mahavira', 'Maganlal Gandhi', 'Lawson', 'Tamil William Godfrey', 'Elgin', 'Patrick Duncan', 'Karl Marx', 'John Bunyan', 'Harold Cox', 'Haque', 'Jan Christian Smuts', 'John Buchan', 'Rustomjee', 'Lady Margaret Hospital', 'Hassim Jooma', 'Henry Salt', 'Satyavan', 'Lourenço Marques', 'Anna Kingsford', 'Abdul Gani', 'Parsee Rustomjee', 'Moulvi Saheb Ahmed Mukhtiar', 'John Cordes', 'Mrs Sodha', 'Sorabji Adajania', 'Madras Polak', 'Adam Smith', 'Nadeshir Cama', 'Chanchal', 'Mrs Packirsamy', 'Ramsamy Moodlai', 'Rana Pratap', 'David Pollock', 'Joseph Chamberlain', 'Petit', 'Mrs Vogt', 'Khune', 'Parcere', 'Neame', 'Mahomedan', 'Lajpat Rai', 'Imam Abdul Kadir Bawazeer', 'Nizam', 'Jesus Christ', 'Cecil', 'Barindranath', 'Hindu Maharajas', 'Aiyar', 'Gertrude', 'Maganlal', 'Essop Mia', 'Mrs Nanji', 'Meer Allam Khan', 'Dinizulu', 'Joseph Royeppen', 'Lepel', 'George Allen', 'Captain Fowle', 'Pranjivan Mehta', 'Mohammed Ali Jinnah', 'Jeki', 'Millie Graham', 'Easton', 'Mahomedans', 'Lord Crewe', 'Govardhanram Tripathi', 'Modh Banias', 'Alfred Lawley', 'Joseph Doke', 'Natesan', 'Sammy Marks', 'Harilal Gandhi', 'Rustamjee', 'Savitri', 'Spion Kop', 'Isabella Fyvie Mayo', 'Maud Polak', 'Louis Botha', 'Montford Chamney', 'Meyer', 'Henry Polak', 'Kasturba', 'Jan Smuts', 'Vinayak Damodar Savarkar', 'Millie Polak', 'William Vogl', 'Rustomjee Jeevanjee', 'Habib Motan', 'Frederick Lely', 'Chanchi', 'Madanlal Dhingra', 'Klerksdorf', 'Liu', 'Leung Quinn', 'Lala Bahadur Singh', 'Eastern Europe', 'Mrs Amacanoo', 'Sonja Schlesin', 'Harilal', 'Friedrich Engels', 'Cape Comorin', 'Flora Shaw', 'Fox Street', 'Aurobindo Ghose', 'Draft Ordinance', 'Khushalchand', 'Mohandas Gandhi', 'Herbert Spencer', 'Amir Ali', 'Ravan', 'Nawab Khan', 'John Ruskin', 'Asari', 'Albert West', 'Gokuldas', 'James D. Hunt', 'Dokes', 'Raja Bhoja', 'Banias', 'Ramdas', 'Dawood Mahomed', 'Abraham Fischer', 'Haridas Vora', 'Bhishma', 'Volksrust Prison', 'Besant', 'Veerammal', 'Ghandi', 'John Stuart Mill', 'Vyas', 'Madame Blavatsky', 'Henry Solomon Leon Polak', 'Chhaganlal Gandhi', 'Vartaman', 'Olive Schreiner', 'Mohandas Karamchand Gandhi', 'Saddarshan Samuccaya', 'Gopal Krishna Gokhale', 'Narmadashanker', 'Mancherjee Bhownaggree', 'Leo Tolstoy', 'Gabriel Isaacs', 'Joseph J. Doke', 'Hermann Kallenbach', 'Mohanchand', 'Vogl', 'Mao Zedong', 'Saul Dubow', 'Ratan Tata', 'Martin Luther', 'Hajee Habib', 'Mrs Gandhi', 'Tulsidas', 'Sigmund Freud', 'Nanji', 'Josiah Oldfield', 'Ishwarchandra Vidyasagar', 'George Bernard Shaw', 'Maulvi Ahmed Mukhtiar', 'Jamshetjee', 'Ramdas Gandhi', 'Ram Sundar Pundit', 'Gabriel I. Isaac', 'Adajania']

# autobio = ['Shankarlal Parikh', 'Brajkishorebabu', 'Hasrat Saheb', 'Shrimatis Avantikabai', 'Kalelkar', 'Abbas', 'Shrimati Anandibai', 'Jehangir Petit', 'Thakkar Bapa', 'Ambalal Sarabhai', 'Deshabandhu', 'Gaya Babu', 'Crewe', 'Jivanlal', 'Gorakhbabu', 'Devdas', 'Jagadanandbabu', 'Kripalani', 'Shrimati Durga Desai', 'Jivraj Mehta', "Michael O'Dwyer", 'Kakasaheb', 'Patwardhan', 'Satyapal', 'Babu Dharanidhar Prasad', 'Rajkumar Shukla', 'Phadke', 'Sinha', 'Ramibai Kamdar', 'Chhaganlal Gandhi', 'Chintaman', 'Lakshmidas', 'Kasturbai', 'Ramnavmi Prasad', 'Punjabhai', 'Mahadev Desai', 'Maulana Mazharul Haq', 'Amritlal Thakkar', 'Manilal', 'Motilalji', 'Babasaheb Soman', 'Yashvantprasad Desai', 'Rajendra Babu', 'Chhotalal', 'Mahatma Munshiramji', 'Keshavrao Deshpande', 'Vaidyanathadham', 'Mohanlal', 'Kelkar', 'Sushil Rudra', 'Gangadharrao', 'Dada Abdulla', 'Sharadbabu', 'Shrimati Vasumatibehn', 'Ramdas', 'Chelmsford', 'Maulana Abdul Bari Saheb', 'Hakim Saheb', 'Malkani', 'Brajkishore Babu', 'Pearson', 'Polak', 'Janakdharibabu', 'Choithram', 'Jayakar', 'Kaul', 'Umar Sobani', 'Malaviyaji', 'Edward Gait', 'Danibehn', 'Brijkishore', 'Lala Harkishanlal', 'Jeramdas', 'Gokhale', 'Bepin', 'Harihar Sharma', 'Shambhaubabu', 'Acharya Ramadevji', 'Shivji', 'Sorabji Adajania', 'Kitchlu', 'Babu Brajkishore Prasad', 'Kuhne', 'Babu Bhupendranath Basu', 'Nagenbabu', 'Gangabehn Majmundar', 'Hakim Ajmal Khan Saheb']

autobio =['Govind BaUabh Pant', 'Khudai Khidmatgar', 'Frederick Cooper', 'Chauri', 'Dutt', 'Tasadduq Ahmad Khan Sherwani', 'Madeleine Slade', 'Sardar Vallabhbhai Patel', 'Iwer', 'Jayakar', 'Qiauri Chaura', 'Jairamdas Doulatram', 'Garhwalis', 'Chloe', 'Thar', 'Glorney Bolton', 'Cowasji', 'Govind Ballabh Pant', 'Khan Abdul Ghaffar Khan', 'Abdul Ghaffor Khan', 'Gustave Dora', 'Avas', 'Ganeshji', 'Bharat Bhushan', 'Irwm', 'Plindi', 'Lewis Carroll', 'Abdul GhafFar Khan', 'Bhagat Singh', 'Bhai', 'Kemal Pasha', 'Bailway', 'Thomas Moore', 'Jambusar', 'Etawah', 'Queen Victoria', 'Eleven Points', 'Sardar Ajit Singh', 'Miraben', 'Govermnent', 'Marariii', 'Saprii', 'Lafeadio Hearn', 'Sri Prakasa', 'Shiva Prasad Gupta', 'Annie Besant', 'Lewis E. Lawes', 'Syed Mahmud', 'Syed Mahmucl', 'Ibbetson', 'Kirkee', 'Raja Narendra Nath', 'Apollonius', 'Hakim Ajmal Khan', 'Sardar VaUabhbhai Patel', 'Blavatsky', 'Hakimji', 'Olrott', 'Redshirts', 'Marshal Foch', 'Purushottan', 'Maulana Abul Kalam Azad', 'Chandrashekhar Azad', 'Venkatesh Narayan Tewary', 'Bernard Shaw', 'Sahab', 'Umar Sobani', 'Narmada Prasad', 'Pushtu', 'Bryce', 'Malcolm Hailey', 'Ramsay MacDonald', 'Keith', 'Jhanda', 'Rafi Ahmad Kidwai', 'Hijli', 'Jatindranath Das', 'Don Quixote']

bio = ['Tbg Ltadtr', 'Winston Churchill', 'Vallabhbhai Patel', 'Edo Fimmen', 'Indira', 'Harry Pollitt', 'Wehave', 'Willi Muenzenberg', 'Muutffar Ahmad', 'Jharia', 'Jamie Millie', 'Gopichand', 'Jagdish Prasad', 'Hoare', 'Maharai Singh', 'Jekyll', 'Allahabad9 March', 'Verney Lovett', 'Hyde', 'Govind Ballabh Pant', 'Frank Brown', 'Hewas', 'Stephani', 'Sitla Sahai', 'Bapu', 'Roger Baldwin', 'Maulona', 'Tbs BombayCbnmicls', 'Bally Kkmaitd', 'Mohammed Hatta', 'Kapil Deva Maiaviya', 'Homiman', 'Lloyd George', 'Cierar', 'Unao', 'Bardoli', 'Cheoki', 'James Maxton', 'Onkar Nath Verma', 'Mudie', 'Meerut Conspiracy Case', 'Brandi', 'Mutobiagnpby', 'Shea', 'Abdul Gaffar Khan', 'Mitter', 'Wecannot', 'Ernst Toller', 'Haig', 'Kamla', 'Hedid', 'Shivaprasad Gupta', 'Dhan Gopal Mukherji', 'Viscount Halifax', 'Montmorency', 'Ariel', 'XJnUtdProvinces', 'Tassaduq Sherwani', 'Willingdon', 'Tbt Leader', 'Norman Leys', 'Kulkarni', 'Ellen Wilkinson', 'Jagdiah Praaad', 'Vithalbhai Patel', 'Henri Barbusse', 'Jagdiah Prasad', 'Bardoll', 'Hatley', 'Irwin', 'Fraadom', 'Alarge', 'Edward Thompson', 'Haileyism', 'IMotilal', 'Thosewho', 'Reginald Bridgman', 'Findlater Stewart', 'Langford', 'Nambiar', 'Subhas Bose', 'Sarojini Naidu', 'Lala Shankarlai', 'Joshi', 'Lenin Gandhi', 'Benn', 'Wedgwood Batin', 'Anjani Kumar', 'Jawahar Lai Nehru', 'Coiltcttd Works', 'Indiaissolikeawoman', 'Keyserling']
def Jaccard_score(lista_1, lista_2):    
    inter = len(list(set(lista_1) & set(lista_2)))
    union = len(list(set(lista_1) | set(lista_2)))
    print(list(set(lista_1) & set(lista_2)))
    if union <=0:
        return 0
    else:
        return inter/union

def fuzzy_Jaccard(list_1, list_2):
    union = len(list(set(list_1) | set(list_2)))
    if union <=0:
        return 0 
    inter_set = set()
    for item1 in set(list_1):
        for item2 in set(list_2):
            print("%s-%s: %s"%(item1, item2, fuzz.partial_ratio(item1, item2)))
            if fuzz.partial_ratio(item1, item2) > 45:
                inter_set.add(item1)
    return len(inter_set)/ union

autobio = {'Rajkumar Shukla': 85, 'Babu Brajkishore Prasad': 85, 'Rajendra Babu': 85, 'Babu Bhupendranath Basu': 85, 'Kasturbai': 85, 'Jehangir Petit': 85, 'Yashvantprasad Desai': 85, "Michael O'Dwyer": 85, 'Kelkar': 85, 'Chhaganlal Gandhi': 85}
bio1 = {'Kasturba': 31, 'Botha': 31, 'Jan Christian Smuts': 31, 'Henry Polak': 31, 'Manilal': 31, 'Ramdas': 31, 'Devadas': 31, 'Harilal': 31, 'Walden': 31, 'Albert Cartwright': 31, 'Herman Kallenbach': 31}
bio2 = {'Kasturba': 150, 'Rustomjee': 150, 'Joseph Chamberlain': 150, 'Lord Milner': 150, 'Albert West': 150, 'Josiah Oldfield': 150, 'Henry Polak': 150, 'Chhaganlal': 150, 'Sheikh Mehtab': 150, 'Herman Kallenbach': 150}

# print(list(set(bio2).intersection(set(bio1))))

# print(Jaccard_score(autobio.keys(), bio1.keys()))
# print(Jaccard_score(autobio.keys(), bio2.keys()))
# print(Jaccard_score(bio1.keys(), bio2.keys()))

print(fuzzy_Jaccard(bio, autobio))

# common_name_autobio_bio1 = ['Ramdas', 'Kasturbai', 'Manilal']
# common_name_autobio_bio2 = ['Ramdas', 'Sorabji Adajania', 'Chhaganlal Gandhi']
# common_name_bio1_bio2 = ['Jan Christian Smuts', 'Chanchi', 'Manilal Gandhi', 'Albert Cartwright', 'Laxmidas', 'Elgin', 'Henry Polak', 'Joseph Chamberlain', 'Ramdas', 'Harilal', 'Olive Schreiner', 'Dadabhai Naoroji', 'Albert West', 'Leo Tolstoy', 'Maganlal', 'Devadas', 'John Ruskin']
# new_nodes_autobio =  ['Shankarlal Parikh', 'Brajkishorebabu', 'Hasrat Saheb', 'Shrimatis Avantikabai', 'Kalelkar', 'Abbas', 'Shrimati Anandibai', 'Jehangir Petit', 'Thakkar Bapa', 'Ambalal Sarabhai', 'Deshabandhu', 'Gaya Babu', 'Crewe', 'Jivanlal', 'Gorakhbabu', 'Devdas', 'Jagadanandbabu', 'Kripalani', 'Shrimati Durga Desai', 'Jivraj Mehta', "Michael O'Dwyer", 'Kakasaheb', 'Patwardhan', 'Satyapal', 'Babu Dharanidhar Prasad', 'Rajkumar Shukla', 'Phadke', 'Sinha', 'Ramibai Kamdar', 'Chhaganlal Gandhi', 'Chintaman', 'Lakshmidas', 'Kasturbai', 'Ramnavmi Prasad', 'Punjabhai', 'Mahadev Desai', 'Maulana Mazharul Haq', 'Amritlal Thakkar', 'Manilal', 'Motilalji', 'Babasaheb Soman', 'Yashvantprasad Desai', 'Rajendra Babu', 'Chhotalal', 'Mahatma Munshiramji', 'Keshavrao Deshpande', 'Vaidyanathadham', 'Mohanlal', 'Kelkar', 'Sushil Rudra', 'Gangadharrao', 'Dada Abdulla', 'Sharadbabu', 'Shrimati Vasumatibehn', 'Ramdas', 'Chelmsford', 'Maulana Abdul Bari Saheb', 'Hakim Saheb', 'Malkani', 'Brajkishore Babu', 'Pearson', 'Polak', 'Janakdharibabu', 'Choithram', 'Jayakar', 'Kaul', 'Umar Sobani', 'Malaviyaji', 'Edward Gait', 'Danibehn', 'Brijkishore', 'Lala Harkishanlal', 'Jeramdas', 'Gokhale', 'Bepin', 'Harihar Sharma', 'Shambhaubabu', 'Acharya Ramadevji', 'Shivji', 'Sorabji Adajania', 'Kitchlu', 'Babu Brajkishore Prasad', 'Kuhne', 'Babu Bhupendranath Basu', 'Nagenbabu', 'Gangabehn Majmundar', 'Hakim Ajmal Khan Saheb']
# new_nodes_bio1 = ['Walden', 'Jekyll', 'Rabbi Joseph Krauskopf', 'Laxmidas', 'Henry Polak', 'John Ruskin', 'Harilal', 'Devadas', 'Habib', 'Maganlalbhai', 'Lawley', 'Ramdas', 'Anderson Streets', 'Chamney', 'Hyde', 'Jan Christian Smuts', 'Joseph Chamberlain', 'Kachhalia', 'Rissik', 'Chertkov', 'Thomas G. Masaryk', 'Buller', 'Olive Schreiner', 'Leo Tolstoy', 'Lutavasinh', 'Alexander Herzen', 'Albert West', 'Chanchi', 'Dadabhai Naoroji', 'Jane Addams', 'Botha', 'Manilal', 'Anna Karenina', 'Sorabji Shapurji Adajania', 'Herman Kallenbach', 'Annie Besant', 'Brahmacharya', 'Sonya Schlesin', 'Max Mueller', 'William Lloyd Garrison', 'William Jennings Bryan', 'Kasturbai', 'J. J. Doke', 'Sheik Mehtab', 'Badri', 'Ralph Waldo Emerson', 'Albert Cartwright', 'Doke', 'Lokamanya Tilak', 'Mir Alam', 'Gani', 'Maganlal', 'Willie', 'Elgin', 'Manilal Gandhi']
# new_nodes_bio2 = ['Namboodiripad', 'Albert Cartwright', 'Edward Carpenter', 'Abraham Lincoln', 'Raymond Aron', 'J. C. Smuts', 'Mahadev Govind Ranade', 'Shyamaji Krishnavarma', 'Jameson', 'Jayshanker Govindji', 'Bhagawan', 'Jayakunwar', 'Merriman', 'Maulvi Mukhtiar', 'Dadabhai Naoroji', 'Joan', 'Maulvi Sahib', 'Narajana Apanna', 'Wolstenholme', 'Nanalal Shah', 'Thambi', 'Shivaji', 'Tolstoyans', 'Pillay', 'Booker T. Washington', 'Taraknath Das', 'Swami Shankeranand', 'Fingo', 'Thomas Carlyle', 'Manilal Doctor', 'Charles Phillips', 'Ahmed Mahomed Cachalia', 'Lewis Ritch', 'Laxmidas', 'Adolf', 'Chanchal Gandhi', 'Arnott', 'Vijaya Dashami', 'Gregorowski', 'Rabindranath Tagore', 'Bloemhof', 'Percy Fitzpatrick', 'Winston Churchill', 'Curzon Wyllie', 'Madan Lal Dhingra', 'Sheikh Mehtab', 'Ananda', 'Cape Colony', 'Bal Gangadhar Tilak', 'John Dube', 'Rosa Luxemburg', 'Table Mountain', 'Kaka', 'Bada Bhai', 'Henry Cotton', 'Nazar', 'Madanjit Vyavaharik', 'Savarkar', 'Het Volk', 'Xiabao', 'Mohandas K. Gandhi', 'Chhaganlal', 'Bapu', 'Harilal Mohandas Gandhi', 'Dawad Mahomed', 'Purushottamdas Desai', 'Chhota Bhai', 'Kaba Gandhi', 'Mudholkar', 'Shapurji Sorabjee', 'Lords Morley', 'Ampthill', 'Gujarati Hindus', 'Akbar', 'Nagappen', 'Pixley Seme', 'Gandhi Abdurahman', 'Alfred Milner', 'Gujarati Muslim', 'Polaks', 'Tata', 'Naidoo', 'Adam Mahomed', 'Wybergh', 'Mazharul', 'Chessell', 'Kabir', 'Laxman', 'Aswat', 'Lord Milner', 'George Washington', 'Narayanaswamy', 'Imam Abdul Kadir', 'Hind Swaraj', 'George Birdwood', 'Maxim Gorky', 'John L. Dube', 'Ramabhai Sodha', 'Abdullah Abdurahman', 'Punditji', 'Aligarh', 'Sorabji', 'Saraswati', 'Gulam Mahomed', 'Ranade', 'Ernest Howard Crosby', 'Manilal Gandhi', 'Sydney Webb', 'African Chronicle', 'Aylmer Maude', 'Karsandas', 'Jamshedji Tata', 'Selborne', 'Abdurrahman', 'Devadas', 'Hatem', 'Gandhiji', 'Raychandbhai', 'Eleanor Marx', 'Hetereodox', 'Alfred Lyttelton', 'Khamisa', 'Ram Sundar Pandit', 'Edgar Snow', 'William Hosken', 'Jan H. Hofmeyr', 'Sri Aurobindo', 'Ahmed Mahommed Cachalia', 'Miss Mayo', 'Bhai', 'Henry David Thoreau', 'Kasturba Gandhi', 'Bharatavarsha', 'Curzon', 'Ritch', 'Gautama Buddha', 'Edward Dallow', 'Mahavira', 'Maganlal Gandhi', 'Lawson', 'Tamil William Godfrey', 'Elgin', 'Patrick Duncan', 'Karl Marx', 'John Bunyan', 'Harold Cox', 'Haque', 'Jan Christian Smuts', 'John Buchan', 'Rustomjee', 'Lady Margaret Hospital', 'Hassim Jooma', 'Henry Salt', 'Satyavan', 'Lourenço Marques', 'Anna Kingsford', 'Abdul Gani', 'Parsee Rustomjee', 'Moulvi Saheb Ahmed Mukhtiar', 'John Cordes', 'Mrs Sodha', 'Sorabji Adajania', 'Madras Polak', 'Adam Smith', 'Nadeshir Cama', 'Chanchal', 'Mrs Packirsamy', 'Ramsamy Moodlai', 'Rana Pratap', 'David Pollock', 'Joseph Chamberlain', 'Petit', 'Mrs Vogt', 'Khune', 'Parcere', 'Neame', 'Mahomedan', 'Lajpat Rai', 'Imam Abdul Kadir Bawazeer', 'Nizam', 'Jesus Christ', 'Cecil', 'Barindranath', 'Hindu Maharajas', 'Aiyar', 'Gertrude', 'Maganlal', 'Essop Mia', 'Mrs Nanji', 'Meer Allam Khan', 'Dinizulu', 'Joseph Royeppen', 'Lepel', 'George Allen', 'Captain Fowle', 'Pranjivan Mehta', 'Mohammed Ali Jinnah', 'Jeki', 'Millie Graham', 'Easton', 'Mahomedans', 'Lord Crewe', 'Govardhanram Tripathi', 'Modh Banias', 'Alfred Lawley', 'Joseph Doke', 'Natesan', 'Sammy Marks', 'Harilal Gandhi', 'Rustamjee', 'Savitri', 'Spion Kop', 'Isabella Fyvie Mayo', 'Maud Polak', 'Louis Botha', 'Montford Chamney', 'Meyer', 'Henry Polak', 'Kasturba', 'Jan Smuts', 'Vinayak Damodar Savarkar', 'Millie Polak', 'William Vogl', 'Rustomjee Jeevanjee', 'Habib Motan', 'Frederick Lely', 'Chanchi', 'Madanlal Dhingra', 'Klerksdorf', 'Liu', 'Leung Quinn', 'Lala Bahadur Singh', 'Eastern Europe', 'Mrs Amacanoo', 'Sonja Schlesin', 'Harilal', 'Friedrich Engels', 'Cape Comorin', 'Flora Shaw', 'Fox Street', 'Aurobindo Ghose', 'Draft Ordinance', 'Khushalchand', 'Mohandas Gandhi', 'Herbert Spencer', 'Amir Ali', 'Ravan', 'Nawab Khan', 'John Ruskin', 'Asari', 'Albert West', 'Gokuldas', 'James D. Hunt', 'Dokes', 'Raja Bhoja', 'Banias', 'Ramdas', 'Dawood Mahomed', 'Abraham Fischer', 'Haridas Vora', 'Bhishma', 'Volksrust Prison', 'Besant', 'Veerammal', 'Ghandi', 'John Stuart Mill', 'Vyas', 'Madame Blavatsky', 'Henry Solomon Leon Polak', 'Chhaganlal Gandhi', 'Vartaman', 'Olive Schreiner', 'Mohandas Karamchand Gandhi', 'Saddarshan Samuccaya', 'Gopal Krishna Gokhale', 'Narmadashanker', 'Mancherjee Bhownaggree', 'Leo Tolstoy', 'Gabriel Isaacs', 'Joseph J. Doke', 'Hermann Kallenbach', 'Mohanchand', 'Vogl', 'Mao Zedong', 'Saul Dubow', 'Ratan Tata', 'Martin Luther', 'Hajee Habib', 'Mrs Gandhi', 'Tulsidas', 'Sigmund Freud', 'Nanji', 'Josiah Oldfield', 'Ishwarchandra Vidyasagar', 'George Bernard Shaw', 'Maulvi Ahmed Mukhtiar', 'Jamshetjee', 'Ramdas Gandhi', 'Ram Sundar Pundit', 'Gabriel I. Isaac', 'Adajania']


# books = ['SOMEWT', 'Life_of_Mahatma_Gandhi', 'Gandhi_Before_India']

# sentences = ""
# with open("app/static/json_files/%s/mentions.json"%books[0], 'r', encoding="utf-8") as content:
#     mentions = json.load(content)

# for name in common_name_autobio_bio2:
#     if name in mentions.keys():
#         for  part, chapters in mentions[name].items():
#             for chap, mention_texts in chapters.items():
#                 sentences += " " + " ".join(mention_texts)
#         sentences = sentences.replace(name, " ")
# # print(sentences)
# stop_words = set(stopwords.words('english'))
# word_tokens = word_tokenize(sentences)

# stop_words.add("'s")
# filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
# print(filtered_sentence)
# word_cloud = WordCloud(collocations = False).generate(" ".join(filtered_sentence))
# # plt.imshow(word_cloud, interpolation='bilinear')
# # plt.axis("off")
# # plt.show()



# sentences1 = ""
# with open("app/static/json_files/%s/mentions.json"%books[2], 'r', encoding="utf-8") as content:
#     mentions = json.load(content)

# for name in common_name_autobio_bio2:
#     if name in mentions.keys():
#         for  part, chapters in mentions[name].items():
#             for chap, mention_texts in chapters.items():
#                 sentences1 += " " + " ".join(mention_texts)
#         sentences1 = sentences1.replace(name, " ")


# def remove_punctuation(txt):
#     return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", txt).split())

# def  clean_text(txt):
#     tmp = [remove_punctuation(t) for t in txt]
#     print(tmp)
#     tmp = [t.lower().split() for t in tmp]
    
#     tmp = [[w for w in t if not w in stop_words]
#               for t in tmp]
#     tmp = [[w for w in t if not w in ['gandhi']]
#                      for t in tmp]
    
#     tmp = list(itertools.chain(*tmp))
#     tmp = collections.Counter(tmp)
#     return tmp

# text1 = clean_text(sentences.split("."))
# text2 = clean_text(sentences1.split("."))

# import shifterator as sh
# from shifterator import shifts as ss
# # entropy_shift = sh.EntropyShift(type2freq_1=text1,
# #                                 type2freq_2=text2,
# #                                 base=2,
# #                                 alpha=0.8)
# # entropy_shift.get_shift_graph(system_names = ['Book1', 'Book2'])

# jsd_shift = ss.JSDivergenceShift(type2freq_1=text1,
#                                 type2freq_2=text2)
# jsd_shift.get_shift_graph(top_n=50)