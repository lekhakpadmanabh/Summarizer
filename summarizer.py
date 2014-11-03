###################
# Author: Padmanabh
# License: GPLv3
###################

from goose import Goose
import networkx as nx
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_kernels

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
sentence_tokenizer = sent_detector.tokenize
stemmer = PorterStemmer()

def goose_extractor(url):
    '''get article contents'''

    article = Goose().extract(url=url)
    return article.title, article.meta_description,\
                              article.cleaned_text
    
def tokenize(sentence):
    '''Tokenizer and Stemmer'''

    tokens = nltk.word_tokenize(sentence)
    tokens = [stemmer.stem(tk) for tk in tokens]
    return tokens

def textrank(matrix):
    '''return textrank vector'''

    nx_graph = nx.from_scipy_sparse_matrix(sparse.csr_matrix(matrix))
    return nx.pagerank(nx_graph)

def _summarize(full_text, num_sentences=4):
    sentences = sentence_tokenizer(full_text)
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english', ngram_range=(1,2))
    norm = tfidf.fit_transform(sentences)
    similarity_matrix = pairwise_kernels(norm, metric='cosine')
    scores = textrank(similarity_matrix)
    scored_sentences = []
    for i, s in enumerate(sentences):
        scored_sentences.append((scores[i],i,s))
    top_scorers = sorted(scored_sentences, key=lambda tup: tup[0], 
                         reverse=True)[:num_sentences]
    return sorted(top_scorers, key=lambda tup: tup[1])

def summarize_url(url, num_sentences=4):
    '''returns: tuple containing
       * human summary if contained
         in article's meta description 
       * tuple with score, index indicating
         order in document, sentence string
    '''

    title, hsumm, full_text = goose_extractor(url)
    return hsumm, _summarize(full_text, num_sentences)

def summarize_text(full_text, num_sentences=4):
    '''returns: tuple with score, index indicating
       order in document, sentence string
    '''

    return _summarize(full_text)

def format_keypoints(key_points):
    '''returns markdown formatted
    string for keypoints'''

    num_pts = len(key_points)
    fmt = u""
    for i in xrange(num_pts):
        fmt += ">* {{{}}}\n".format(i)
    return fmt.format(*[p[2] for p in key_points])
