from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from string import punctuation
from nltk.stem import WordNetLemmatizer
from lxml import etree
from collections import defaultdict, Counter
import os

xml = etree.parse(os.path.join(os.getcwd(), 'news.xml'))
test = xml.xpath('//news')
freq = defaultdict(str)
for i in test:
    head = [j.text for j in i if j.get('name') == 'head']
    text = [k.text for k in i if k.get('name') == 'text']
    for h, t in zip(head, text):
        freq[h] = t


def most_comm(seq):
    return [round(v, 3) for v in seq]


def word_process(para):
    lemma = WordNetLemmatizer()
    temp = word_tokenize(para.lower())
    stem = [lemma.lemmatize(word) for word in temp]
    noun = [word for word in stem if pos_tag([word])[0][1] == 'NN']
    seq = [word for word in noun if word not in punctuation and word not in stopwords.words('english')]
    return seq


def td_idf_scores(s):
    dataset = [' '.join(word_process(v)) for v in s]
    vector = TfidfVectorizer()
    matrix = vector.fit_transform(dataset)
    last = []
    terms = vector.get_feature_names_out()
    for lst in matrix.toarray():
        best = defaultdict(list)
        for word, weigh in zip(terms, most_comm(lst)):
            best[weigh].append(word)
        last.append(dict(best))
    return [dict(sorted(d.items(), reverse=True)) for d in list(last)]


def best_five(seq):
    comm = []
    for w in list(seq.items())[:5]:
        for j in sorted(w[1], reverse=True):
            comm.append(j)
    return comm[:5]


for title, dic in zip(freq.keys(), td_idf_scores(freq.values())):
    print(f'{title}:')
    print(*best_five(dic))
