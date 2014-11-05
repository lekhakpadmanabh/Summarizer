###################
# Author: Padmanabh
# License: GPLv3
###################

from goose import Goose
import networkx as nx
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_kernels
from utilities import memoize

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
sentence_tokenizer = sent_detector.tokenize
stemmer = nltk.stem.porter.PorterStemmer()

@memoize
def goose_extractor(url):
    '''webpage extraction using
       Goose Library'''

    article = Goose().extract(url=url)
    return article.title, article.meta_description,\
                              article.cleaned_text

class ArticleExtractionFail(Exception):
    pass

def _tokenize(sentence):
    '''Tokenizer and Stemmer'''

    _tokens = nltk.word_tokenize(sentence)
    tokens = [stemmer.stem(tk) for tk in _tokens]
    return tokens

def _normalize(sentences):
    '''returns tf-idf matrix
       (unigrams+bigrams)'''

    tfidf = TfidfVectorizer(tokenizer=_tokenize,
                            stop_words='english',
                            decode_error='ignore',
                            ngram_range=(1,2))
    return tfidf.fit_transform(sentences)

def _textrank(matrix):
    '''returns principal eigenvector
       of the adjacency matrix'''

    graph = nx.from_numpy_matrix(matrix)
    return nx.pagerank(graph)


def _summarize(full_text, title='', num_sentences=4):
    '''returns tuple of scored sentences
       in order of appearance
       Note: Doing an A/B test to
       compare results, reverting to 
       original algorithm.'''

    sentences = sentence_tokenizer(full_text)
    norm = _normalize(sentences)
    similarity_matrix = pairwise_kernels(norm, metric='cosine')
    scores = _textrank(similarity_matrix)
    scored_sentences = []
    for i, s in enumerate(sentences):
        scored_sentences.append((scores[i],i,s))
    top_scorers = sorted(scored_sentences,
                         key=lambda tup: tup[0], 
                         reverse=True)[:num_sentences]
    return sorted(top_scorers, key=lambda tup: tup[1])

def _format(key_points):
    '''returns markdown formatted
       string for keypoints'''

    num_pts = len(key_points)
    fmt = u""
    for i in xrange(num_pts):
        fmt += ">* {{{}}}\n".format(i)
    return fmt.format(*[p[2] for p in key_points])


def summarize_url(url, num_sentences=4, fmt=None):
    '''returns: tuple containing
       * human summary if contained
         in article's meta description 
       * tuple with score, index indicating
         order in document, sentence string
       fmt='md' returns human summary and markdown
       formatted keypoints
    '''

    title, hsumm, full_text = goose_extractor(url)
    if not full_text:
        raise ArticleExtractionFail("Couldn't extract: {}".format(url))
    if fmt == "md":
        return hsumm, _format(_summarize(full_text, title, num_sentences))
    return hsumm, _summarize(full_text, title, num_sentences)


def summarize_text(full_text, title='', num_sentences=4, fmt=None):
    '''returns tuple with score, index indicating
       order in document, sentence string
       fmt='md' returns markdown formatted keypoints
    '''

    if fmt == "md":
        return _format(_summarize(full_text, title, num_sentences))
    return _summarize(full_text, title, num_sentences)
