from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import spacy
import re
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from scipy.special import psi, polygamma, gammaln
import numpy as np
import matplotlib.pyplot as plt

vectorizer = CountVectorizer()

books = ['nelson_autobiography', 'nelson_mandela_biography']
start=1939
end=1994
year_window=7
num_gibbs = 200

start_year_list = [x for x in range(start, end, year_window)]
end_year_list = [x+year_window-1 for x in start_year_list]


stop_words = set(stopwords.words('english'))
stop_words.update(["'s","u", "sometimes", "firom", "g", "even", "many", "p", "pp", "w", "us", "said", "told", "came", "come", "became", "dr", "go", "sjt", "co", "un", "one", "might", "must", 
'january','feb','march','april','may','june','july','august','september','october','november','december', 'vol', 'mr', 'k', 'self', 'thy', 'thus', 'west','sw',
'end', 'tion', 'th', 'used', 'location', 'indians', 'indian', 'wrote', 'already', 'con', 'ment', 'whils', 'work', 'also', 'could', 'know', 'learnt', 'spite',
'see', 'get', 'beginning', 'ing', 'east', 'felt', 'take', 'tie',',','.','in','and','this','we','they','way','I','The','11','22','1947','1969','1943','?',';','he','this','we','in','but','would',
'it','1942','1945','1970','’','‘','*',')','(','4','2','sr','sc','ov','z', 'time', 'moment', 'day', 'hour', 'evening', 'night', 'month', 'day', 'year', 'large', 'small', 'begin', 'start', 'week',
'like', 'say',  'thing', 'low', 'high', 'ji', 'stn', 'tell','weekly', 'daily', 'thirteen', 'seven', 'eighteen', 'nineteen', 'twenty', 'seventeen', 'true', 'truth',
'bene', 'te', 'su', 'xe', 'di', 'l', 'ection', 'cient', 'n', 'dence', 'erence', 'h', 'ort', 'speci', 'r', 'ter', 'ght', 'ected', 'erence', 'ort', 'ere', 'dre', "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",    "below", "beside", "besides", "between", "beyond", "bill", "both",    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",    "find", "fire", "first", "five", "for", "former", "formerly", "forty",    "found", "four", "from", "front", "full", "further", "get", "give", "go",    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",    "latterly", "least", "less", "ltd", "made", "many", "may", "me",    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",    "move", "much", "must", "my", "myself", "name", "namely", "neither",    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",    "please", "put", "rather", "re", "same", "see", "seem", "seemed",    "seeming", "seems", "serious", "several", "she", "should", "show", "side",    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",    "something", "sometime", "sometimes", "somewhere", "still", "such",    "system", "take", "ten", "than", "that", "the", "their", "them",    "themselves", "then", "thence", "there", "thereafter", "thereby",    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",    "third", "this", "those", "though", "three", "through", "throughout",    "thru", "thus", "to", "together", "too", "top", "toward", "towards",    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",    "whence", "whenever", "where", "whereafter", "whereas", "whereby",    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",    "within", "without", "would", "yet", "you", "your", "yours", "yourself",    "yourselves", ".", "!", "?", ",", ";", ":", "[", "]", "{", "}", "-", "+",     "_", "/", "@", "#", "$", "%", "^", "&", "*", "(", ")", "<", ">", "|", "=",
    ".-", ".,", "'", '"', ',"', 'aa', 'aaj', 'aakash', 'aam', 'aamer', 'aap', 'aaqib', 'aare', 'aata', 'aaye', 'aayi', 'ab', 'aback', 'abey'
])

nlp = spacy.load("en_core_web_sm", disable=['ner', 'parser']) # disabling Named Entity Recognition for speed
def cleaning(doc):
    # Lemmatizes and removes stopwords
    # doc needs to be a spacy Doc object
    txt = [token.lemma_ for token in doc if not token.is_stop]
    # Word2Vec uses context words to learn the vector representation of a target word,
    # if a sentence is only one or two words long,
    # the benefit for the training is very small
    if len(txt) > 2:
        return ' '.join(txt)


with open("json_files/%s/temporal_word_list.json"%books[0], 'r') as content:
    autobio = json.load(content)
with open("json_files/%s/temporal_word_list.json"%books[1], 'r') as content:
    bio = json.load(content)

def init_lda(docs, vocab, n_topic, gibbs=False, random_state=100):
    if gibbs:
        global V, k, N, M, alpha, eta, n_iw, n_di
    else:
        global V, k, N, M, alpha, beta, gamma, phi
        
    np.random.seed(random_state)

    V = len(vocab) + 1
    k = n_topic  # number of topics
    N = np.array([doc.shape[0] for doc in docs])
    M = len(docs)

    print(f"V: {V}\nk: {k}\nN: {N[:10]}...\nM: {M}")

    # initialize α, β
    
    if gibbs:
        alpha = np.random.gamma(shape=100, scale=0.01, size=1)  # one for all k
        eta = np.random.gamma(shape=100, scale=0.01, size=1)  # one for all V
        print(f"α: {alpha}\nη: {eta}")
        
        n_iw = np.zeros((k, V), dtype=int)
        n_di = np.zeros((M, k), dtype=int)
        print(f"n_iw: dim {n_iw.shape}\nn_di: dim {n_di.shape}")
    else:
        alpha = np.random.gamma(shape=100, scale=0.01, size=k) #np.random.rand(k)
        beta = np.random.dirichlet(np.ones(V), k)
        print(f"α: dim {alpha.shape}\nβ: dim {beta.shape}")

        # initialize ϕ, γ
        ## ϕ: (M x max(N) x k) arrays with zero paddings on the right
        gamma = alpha + np.ones((M, k)) * N.reshape(-1, 1) / k

        phi = np.ones((M, max(N), k)) / k
        for m, N_d in enumerate(N):
            phi[m, N_d:, :] = 0  # zero padding for vectorized operations

        print(f"γ: dim {gamma.shape}\nϕ: dim ({len(phi)}, N_d, {phi[0].shape[1]})")

def _init_gibbs(docs, vocab, n_topic, n_gibbs=2000):
    """
    Initialize t=0 state for Gibbs sampling.
    Replace initial word-topic assignment ndarray (M, N, N_GIBBS) in-place.
    """
    # initialize variables
    init_lda(docs, vocab, n_topic=n_topic, gibbs=True)
    
    # word-topic assignment
    global assign
    N_max = max(N)
    assign = np.zeros((M, N_max, n_gibbs+1), dtype=int)
    print(f"assign: dim {assign.shape}")
    
    # initial assignment
    for d in range(M):
        for n in range(N[d]):
            # randomly assign topic to word w_{dn}
            w_dn = docs[d][n]
            assign[d, n, 0] = np.random.randint(k)

            # increment counters
            i = assign[d, n, 0]
            n_iw[i, w_dn] += 1
            n_di[d, i] += 1

def _conditional_prob(w_dn, d):
    """
    P(z_{dn}^i=1 | z_{(-dn)}, w)
    """
    prob = np.empty(k)
    
    for i in range(k):
        # P(w_dn | z_i)
        _1 = (n_iw[i, w_dn] + eta) / (n_iw[i, :].sum() + V*eta)
        # P(z_i | d)
        _2 = (n_di[d, i] + alpha) / (n_di[d, :].sum() + k*alpha)
        
        prob[i] = _1 * _2
    
    return prob / prob.sum()

def run_gibbs(docs, vocab, n_topic, n_gibbs=2000, verbose=True):
    """
    Run collapsed Gibbs sampling
    """
    # initialize required variables
    _init_gibbs(docs, vocab, n_topic, n_gibbs)
    
    if verbose:
        print("\n", "="*10, "START SAMPLER", "="*10)
    
    # run the sampler
    for t in range(n_gibbs):
        for d in range(M):
            for n in range(N[d]):
                w_dn = docs[d][n]
                
                # decrement counters
                i_t = assign[d, n, t]  # previous assignment
                n_iw[i_t, w_dn] -= 1
                n_di[d, i_t] -= 1

                # assign new topics
                prob = _conditional_prob(w_dn, d)
                i_tp1 = np.argmax(np.random.multinomial(1, prob))

                # increment counter according to new assignment
                n_iw[i_tp1, w_dn] += 1
                n_di[d, i_tp1] += 1
                assign[d, n, t+1] = i_tp1
        
        # print out status
        if verbose & ((t+1) % 10 == 0):
            print(f"Sampled {t+1}/{n_gibbs}")



def n_most_important(vocab, beta_i, n=30):
    """
    find the index of the largest `n` values in a list
    """
    # print(beta_i)
    max_values = beta_i.argsort()[-n:][::-1]
    # print(max_values)
    if len(vocab) == 0:
        return [0]*n
    max_values = list(map(lambda x: x if x != len(vocab) else len(vocab)-1, max_values))
    return np.array(vocab)[max_values]


autobio_topics = {}
for yrange, sentences in autobio.items():
    autobio_words = ''
    vocab = []
    brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in sentences.split('.'))
    sent = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000)]
    sent = [x for x in sent if x is not None]
    tokens = word_tokenize(' '.join(sent))
    tokens = [x for x in tokens if x not in stop_words]
    cleaned_doc = ' '.join(tokens)
    vocab += tokens
    # tokens_autobio[range] = tokens
    autobio_words+=cleaned_doc

    # print(autobio_words)
    # print(tokens)
    # X = vectorizer.fit_transform(autobio_words)
    # docs = X.toarray()
    # vocab = vectorizer.get_feature_names()

    vocab = list(set(vocab))
    word_to_ix = {w: i for i, w in enumerate(vocab)}

    def seq_to_ix(seq, vocab=vocab):
        # len(vocab), which is the last index, is for the <unk> (unknown) token
        unk_idx = len(vocab)
        return np.array(list(map(lambda w: word_to_ix.get(w, unk_idx), seq)))

    docs = list(map(seq_to_ix, [autobio_words.split(' ')]))

    # print(docs[:5])
    # print(X.toarray())
    run_gibbs(docs, vocab, n_topic=5, n_gibbs=num_gibbs)

    beta_hat= np.empty((k, V))
    theta_hat = np.empty((M, k))

    for j in range(V):
        for i in range(k):
            beta_hat[i, j] = (n_iw[i, j] + eta) / (n_iw[i, :].sum() + V*eta)

    for d in range(M):
        for i in range(k):
            theta_hat[d, i] = (n_di[d, i] + alpha) / (n_di[d, :].sum() + k*alpha)

    _topics = []
    for i in range(k):
        num_words = 500
        # print(f"TOPIC {i:02}: {n_most_important(vocab, beta_hat[i], num_words)}")
        _topics.append(n_most_important(vocab, beta_hat[i], num_words))
    autobio_topics[yrange] = _topics

bio_topics = {}
for yrange, sentences in bio.items():
    bio_words = ''
    vocab = []
    brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in sentences.split('.'))
    sent = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000)]
    sent = [x for x in sent if x is not None]
    tokens = word_tokenize(' '.join(sent))
    tokens = [x for x in tokens if x not in stop_words]
    cleaned_doc = ' '.join(tokens)
    vocab += tokens
    # tokens_autobio[range] = tokens
    bio_words+=cleaned_doc

    vocab = list(set(vocab))
    word_to_ix = {w: i for i, w in enumerate(vocab)}

    def seq_to_ix(seq, vocab=vocab):
        # len(vocab), which is the last index, is for the <unk> (unknown) token
        unk_idx = len(vocab)
        return np.array(list(map(lambda w: word_to_ix.get(w, unk_idx), seq)))

    docs = list(map(seq_to_ix, [bio_words.split(' ')]))


    # print(X.toarray())
    run_gibbs(docs, vocab, n_topic=5, n_gibbs=num_gibbs)

    beta_hat= np.empty((k, V))
    theta_hat = np.empty((M, k))

    for j in range(V):
        for i in range(k):
            beta_hat[i, j] = (n_iw[i, j] + eta) / (n_iw[i, :].sum() + V*eta)

    for d in range(M):
        for i in range(k):
            theta_hat[d, i] = (n_di[d, i] + alpha) / (n_di[d, :].sum() + k*alpha)

    _topics = []
    for i in range(k):
        num_words = 100
        # print(f"TOPIC {i:02}: {n_most_important(vocab, beta_hat[i], num_words)}")
        _topics.append(n_most_important(vocab, beta_hat[i], num_words))
    bio_topics[yrange] = _topics

upper_threshold = 0.25
lower_threshold = 0.25

_file = open("cdtm_%s.txt"%books[0].split('_')[0], "w+")
for yrange in bio.keys():
    write_str = "------------------------%s--------------------------\n"%yrange
    print(write_str)
    _file.write(write_str)
    common_topics = []
    distinctive_topic_autobio = []
    distinctive_topic_bio = []
    for topic1 in autobio_topics[yrange]:
        for topic2 in bio_topics[yrange]:
            intersection = set(topic1).intersection(set(topic2))
            similarity = min(len(intersection)/len(topic1), len(intersection)/(len(topic2)))
            print(similarity)
            _file.write(str(similarity) + '\n')
            if similarity > upper_threshold:
                common_topics += list(intersection)
                write_str = "------------------------Common Topic--------------------------\n"
                print(write_str)
                _file.write(write_str)
                write_str = topic1[:100] 
                print(write_str)
                _file.write(str(write_str) + '\n')
                write_str=topic2[:100]
                print(write_str)
                _file.write(str(write_str) + '\n')
            if similarity < lower_threshold:
                distinctive_topic_autobio += list(topic1) 
                distinctive_topic_bio += list(topic2)
                write_str="------------------------Distinctive Topic--------------------------"
                print(write_str)
                _file.write(str(write_str) + '\n')
                write_str=topic1[:15]
                print(write_str)
                _file.write(str(write_str) + '\n')
                write_str=topic2[:15]
                print(write_str)
                _file.write(str(write_str) + '\n')

print("------------------------Common Topic--------------------------")
# print(common_topics)

print("------------------------Distinctive Topic--------------------------")
# print(distinctive_topic_autobio)

# print(distinctive_topic_bio)