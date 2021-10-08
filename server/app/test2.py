from fuzzywuzzy import fuzz

autobio_nodes = ['Shankarlal Parikh', 'Brajkishorebabu', 'Hasrat Saheb', 'Shrimatis Avantikabai', 'Kalelkar', 'Abbas', 'Shrimati Anandibai', 'Jehangir Petit', 'Thakkar Bapa', 'Ambalal Sarabhai', 'Deshabandhu', 'Gaya Babu', 'Crewe', 'Jivanlal', 'Gorakhbabu', 'Devdas', 'Jagadanandbabu', 'Kripalani', 'Shrimati Durga Desai', 'Jivraj Mehta', "Michael O'Dwyer", 'Kakasaheb', 'Patwardhan', 'Satyapal', 'Babu Dharanidhar Prasad', 'Rajkumar Shukla', 'Phadke', 'Sinha', 'Ramibai Kamdar', 'Chhaganlal Gandhi', 'Chintaman', 'Lakshmidas', 'Kasturbai', 'Ramnavmi Prasad', 'Punjabhai', 'Mahadev Desai', 'Maulana Mazharul Haq', 'Amritlal Thakkar', 'Manilal', 'Motilalji', 'Babasaheb Soman', 'Yashvantprasad Desai', 'Rajendra Babu', 'Chhotalal', 'Mahatma Munshiramji', 'Keshavrao Deshpande', 'Vaidyanathadham', 'Mohanlal', 'Kelkar', 'Sushil Rudra', 'Gangadharrao', 'Dada Abdulla', 'Sharadbabu', 'Shrimati Vasumatibehn', 'Ramdas', 'Chelmsford', 'Maulana Abdul Bari Saheb', 'Hakim Saheb', 'Malkani', 'Brajkishore Babu', 'Pearson', 'Polak', 'Janakdharibabu', 'Choithram', 'Jayakar', 'Kaul', 'Umar Sobani', 'Malaviyaji', 'Edward Gait', 'Danibehn', 'Brijkishore', 'Lala Harkishanlal', 'Jeramdas', 'Gokhale', 'Bepin', 'Harihar Sharma', 'Shambhaubabu', 'Acharya Ramadevji', 'Shivji', 'Sorabji Adajania', 'Kitchlu', 'Babu Brajkishore Prasad', 'Kuhne', 'Babu Bhupendranath Basu', 'Nagenbabu', 'Gangabehn Majmundar', 'Hakim Ajmal Khan Saheb']
bio1_nodes =  ['Walden', 'Jekyll', 'Rabbi Joseph Krauskopf', 'Laxmidas', 'Henry Polak', 'John Ruskin', 'Harilal', 'Devadas', 'Habib', 'Maganlalbhai', 'Lawley', 'Ramdas', 'Anderson Streets', 'Chamney', 'Hyde', 'Jan Christian Smuts', 'Joseph Chamberlain', 'Kachhalia', 'Rissik', 'Chertkov', 'Thomas G. Masaryk', 'Buller', 'Olive Schreiner', 'Leo Tolstoy', 'Lutavasinh', 'Alexander Herzen', 'Albert West', 'Chanchi', 'Dadabhai Naoroji', 'Jane Addams', 'Botha', 'Manilal', 'Anna Karenina', 'Sorabji Shapurji Adajania', 'Herman Kallenbach', 'Annie Besant', 'Brahmacharya', 'Sonya Schlesin', 'Max Mueller', 'William Lloyd Garrison', 'William Jennings Bryan', 'Kasturbai', 'J. J. Doke', 'Sheik Mehtab', 'Badri', 'Ralph Waldo Emerson', 'Albert Cartwright', 'Doke', 'Lokamanya Tilak', 'Mir Alam', 'Gani', 'Maganlal', 'Willie', 'Elgin', 'Manilal Gandhi']
bio2_nodes = ['Namboodiripad', 'Albert Cartwright', 'Edward Carpenter', 'Abraham Lincoln', 'Raymond Aron', 'J. C. Smuts', 'Mahadev Govind Ranade', 'Shyamaji Krishnavarma', 'Jameson', 'Jayshanker Govindji', 'Bhagawan', 'Jayakunwar', 'Merriman', 'Maulvi Mukhtiar', 'Dadabhai Naoroji', 'Joan', 'Maulvi Sahib', 'Narajana Apanna', 'Wolstenholme', 'Nanalal Shah', 'Thambi', 'Shivaji', 'Tolstoyans', 'Pillay', 'Booker T. Washington', 'Taraknath Das', 'Swami Shankeranand', 'Fingo', 'Thomas Carlyle', 'Manilal Doctor', 'Charles Phillips', 'Ahmed Mahomed Cachalia', 'Lewis Ritch', 'Laxmidas', 'Adolf', 'Chanchal Gandhi', 'Arnott', 'Vijaya Dashami', 'Gregorowski', 'Rabindranath Tagore', 'Bloemhof', 'Percy Fitzpatrick', 'Winston Churchill', 'Curzon Wyllie', 'Madan Lal Dhingra', 'Sheikh Mehtab', 'Ananda', 'Cape Colony', 'Bal Gangadhar Tilak', 'John Dube', 'Rosa Luxemburg', 'Table Mountain', 'Kaka', 'Bada Bhai', 'Henry Cotton', 'Nazar', 'Madanjit Vyavaharik', 'Savarkar', 'Het Volk', 'Xiabao', 'Mohandas K. Gandhi', 'Chhaganlal', 'Bapu', 'Harilal Mohandas Gandhi', 'Dawad Mahomed', 'Purushottamdas Desai', 'Chhota Bhai', 'Kaba Gandhi', 'Mudholkar', 'Shapurji Sorabjee', 'Lords Morley', 'Ampthill', 'Gujarati Hindus', 'Akbar', 'Nagappen', 'Pixley Seme', 'Gandhi Abdurahman', 'Alfred Milner', 'Gujarati Muslim', 'Polaks', 'Tata', 'Naidoo', 'Adam Mahomed', 'Wybergh', 'Mazharul', 'Chessell', 'Kabir', 'Laxman', 'Aswat', 'Lord Milner', 'George Washington', 'Narayanaswamy', 'Imam Abdul Kadir', 'Hind Swaraj', 'George Birdwood', 'Maxim Gorky', 'John L. Dube', 'Ramabhai Sodha', 'Abdullah Abdurahman', 'Punditji', 'Aligarh', 'Sorabji', 'Saraswati', 'Gulam Mahomed', 'Ranade', 'Ernest Howard Crosby', 'Manilal Gandhi', 'Sydney Webb', 'African Chronicle', 'Aylmer Maude', 'Karsandas', 'Jamshedji Tata', 'Selborne', 'Abdurrahman', 'Devadas', 'Hatem', 'Gandhiji', 'Raychandbhai', 'Eleanor Marx', 'Hetereodox', 'Alfred Lyttelton', 'Khamisa', 'Ram Sundar Pandit', 'Edgar Snow', 'William Hosken', 'Jan H. Hofmeyr', 'Sri Aurobindo', 'Ahmed Mahommed Cachalia', 'Miss Mayo', 'Bhai', 'Henry David Thoreau', 'Kasturba Gandhi', 'Bharatavarsha', 'Curzon', 'Ritch', 'Gautama Buddha', 'Edward Dallow', 'Mahavira', 'Maganlal Gandhi', 'Lawson', 'Tamil William Godfrey', 'Elgin', 'Patrick Duncan', 'Karl Marx', 'John Bunyan', 'Harold Cox', 'Haque', 'Jan Christian Smuts', 'John Buchan', 'Rustomjee', 'Lady Margaret Hospital', 'Hassim Jooma', 'Henry Salt', 'Satyavan', 'Lourenço Marques', 'Anna Kingsford', 'Abdul Gani', 'Parsee Rustomjee', 'Moulvi Saheb Ahmed Mukhtiar', 'John Cordes', 'Mrs Sodha', 'Sorabji Adajania', 'Madras Polak', 'Adam Smith', 'Nadeshir Cama', 'Chanchal', 'Mrs Packirsamy', 'Ramsamy Moodlai', 'Rana Pratap', 'David Pollock', 'Joseph Chamberlain', 'Petit', 'Mrs Vogt', 'Khune', 'Parcere', 'Neame', 'Mahomedan', 'Lajpat Rai', 'Imam Abdul Kadir Bawazeer', 'Nizam', 'Jesus Christ', 'Cecil', 'Barindranath', 'Hindu Maharajas', 'Aiyar', 'Gertrude', 'Maganlal', 'Essop Mia', 'Mrs Nanji', 'Meer Allam Khan', 'Dinizulu', 'Joseph Royeppen', 'Lepel', 'George Allen', 'Captain Fowle', 'Pranjivan Mehta', 'Mohammed Ali Jinnah', 'Jeki', 'Millie Graham', 'Easton', 'Mahomedans', 'Lord Crewe', 'Govardhanram Tripathi', 'Modh Banias', 'Alfred Lawley', 'Joseph Doke', 'Natesan', 'Sammy Marks', 'Harilal Gandhi', 'Rustamjee', 'Savitri', 'Spion Kop', 'Isabella Fyvie Mayo', 'Maud Polak', 'Louis Botha', 'Montford Chamney', 'Meyer', 'Henry Polak', 'Kasturba', 'Jan Smuts', 'Vinayak Damodar Savarkar', 'Millie Polak', 'William Vogl', 'Rustomjee Jeevanjee', 'Habib Motan', 'Frederick Lely', 'Chanchi', 'Madanlal Dhingra', 'Klerksdorf', 'Liu', 'Leung Quinn', 'Lala Bahadur Singh', 'Eastern Europe', 'Mrs Amacanoo', 'Sonja Schlesin', 'Harilal', 'Friedrich Engels', 'Cape Comorin', 'Flora Shaw', 'Fox Street', 'Aurobindo Ghose', 'Draft Ordinance', 'Khushalchand', 'Mohandas Gandhi', 'Herbert Spencer', 'Amir Ali', 'Ravan', 'Nawab Khan', 'John Ruskin', 'Asari', 'Albert West', 'Gokuldas', 'James D. Hunt', 'Dokes', 'Raja Bhoja', 'Banias', 'Ramdas', 'Dawood Mahomed', 'Abraham Fischer', 'Haridas Vora', 'Bhishma', 'Volksrust Prison', 'Besant', 'Veerammal', 'Ghandi', 'John Stuart Mill', 'Vyas', 'Madame Blavatsky', 'Henry Solomon Leon Polak', 'Chhaganlal Gandhi', 'Vartaman', 'Olive Schreiner', 'Mohandas Karamchand Gandhi', 'Saddarshan Samuccaya', 'Gopal Krishna Gokhale', 'Narmadashanker', 'Mancherjee Bhownaggree', 'Leo Tolstoy', 'Gabriel Isaacs', 'Joseph J. Doke', 'Hermann Kallenbach', 'Mohanchand', 'Vogl', 'Mao Zedong', 'Saul Dubow', 'Ratan Tata', 'Martin Luther', 'Hajee Habib', 'Mrs Gandhi', 'Tulsidas', 'Sigmund Freud', 'Nanji', 'Josiah Oldfield', 'Ishwarchandra Vidyasagar', 'George Bernard Shaw', 'Maulvi Ahmed Mukhtiar', 'Jamshetjee', 'Ramdas Gandhi', 'Ram Sundar Pundit', 'Gabriel I. Isaac', 'Adajania']


event_nodes_autobio = ["Pearson",
        "Kasturbai",
        "C.F. Andrews",
        "Gandhi",
        "Kallenbach",
        "Mr Hult",
        "Bill",
        "Gopal Krishna Gokhale",
        "Laxmi",
        "Gokhale",
        "Gandhi",
        "Jawaharlal Nehru",
        "Dharnidhar Prasad",
        "Acharya Kriplani",
        "Gandhi",
        "Anugrah Narayan Singh",
        "Simon",
        "Mahatma Gandhi",
        "Frank Shy",
        "C. F. Andrews",
        "Motihari",
        "Raj Kishore Prasad",
        "Mahadev Desai",
        "Rajkumar Shukla",
        "Rajendra Prasad",
        "H. S. Pollock"]

event_nodes_bio = ["Ruskin",
        "Gandhi",
        "Jan Christiaan Smuts",
        "Smuts",
        "Mir Alam",
        "Tolstoy",
        "Kallenbach"]

def get_intersection(list1, list2):
    inter_nodes = []

    for node in list1:
        for member in list2:
            if fuzz.partial_ratio(node, member) > 75:
                inter_nodes.append(node)

    if len(list1) <= 0:
        return 0
    else:
        return len(set(inter_nodes)) / len(set(list1))

# inter = len(list(set(autobio_nodes) & set(event_nodes_autobio)))
# print(inter / len(list(set(event_nodes_autobio))) * 100)

# inter = len(list(set(bio1_nodes) & set(event_nodes_bio)))
# print(inter / len(list(set(event_nodes_bio))) * 100)

# inter = len(list(set(bio2_nodes) & set(event_nodes_bio)))
# print(inter / len(list(set(event_nodes_bio))) * 100)
print(get_intersection(event_nodes_autobio, autobio_nodes))
print(get_intersection(event_nodes_bio, bio1_nodes))
print(get_intersection(event_nodes_bio, bio2_nodes))