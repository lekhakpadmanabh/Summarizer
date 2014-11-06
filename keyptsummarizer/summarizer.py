###################
# Author: Padmanabh
# License: GPLv3
###################

from better_sentences import better_sentences
from exceptions import ArticleExtractionFail
from formatters import Formatter
from goose import Goose
import networkx as nx
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_kernels
from utilities import memoize

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = nltk.stem.porter.PorterStemmer()

@better_sentences
def sentence_tokenizer(text):
    return sent_detector.tokenize(text)

@memoize
def goose_extractor(url):
    '''webpage extraction using
       Goose Library'''

    article = Goose().extract(url=url)
    return article.title, article.meta_description,\
                              article.cleaned_text

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


def _intertext_score(full_text, title='', num_sentences=4):
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
                         reverse=True)
    return top_scorers
    #return sorted(top_scorers, key=lambda tup: tup[1])

def _title_similarity_score(full_text, title='', num_sentences=4):
    """Similarity scores for sentences with
       title in descending order"""

    sentences = sentence_tokenizer(full_text)
    norm = _normalize([title]+sentences)
    similarity_matrix = pairwise_kernels(norm, metric='cosine')
    return sorted(zip(
                     similarity_matrix[0,1:],
                     range(len(similarity_matrix)),
                     sentences
                     ),
                 key = lambda tup: tup[0],
                 reverse=True
                 )

def _remove_title_from_tuples(its, tss):
    index = None
    for i,el in enumerate(its):
        if el[2] == tss[0][2]:
            index = i
    if index is None: 
        raise Exception("Something fatal: tss and its don't align")
    del its[index]
    del tss[0]
    return its, tss

def _aggregrate_scores(its,tss,num_sentences):
    """rerank the two vectors by
    min aggregrate rank, reorder"""
    final = []
    for i,el in enumerate(its):
        for j, le in enumerate(tss):
            if el[2] == le[2]:
                assert el[1] == le[1]
                final.append((el[1],i+j,el[2]))
    _final = sorted(final, key = lambda tup: tup[1])[:num_sentences]
    return sorted(_final, key = lambda tup: tup[0])


def _eval_meta_as_summary(meta):
    """return type bool"""
    if meta == '':
        return False
    if len(meta)>500:
        # http://www.reddit.com/r/worldnews/comments/2lf4te
        return False
    if 'login' in meta:
        return False
    return True



def summarize_url(url, num_sentences=4, fmt=None):
    '''returns: tuple containing
       * human summary if contained
         in article's meta description 
       * tuple with score, index indicating
         order in document, sentence string
       fmt='md' returns human summary and markdown
       formatted keypoints
    '''

    title, meta, full_text = goose_extractor(url)

    if not full_text:
        raise ArticleExtractionFail("Couldn't extract: {}".format(url))

    intertext_scores = _intertext_score(full_text, title, num_sentences)
    title_similarity_scores = _title_similarity_score(full_text, 
                                                      title, num_sentences)

    if _eval_meta_as_summary(meta):
        summ = meta
    else:
        summ = title_similarity_scores[0][2]
        intertext_scores, title_similarity_scores = \
            _remove_title_from_tuples(intertext_scores, title_similarity_scores)

    scores = _aggregrate_scores(intertext_scores, title_similarity_scores, num_sentences)

    if fmt:
        formatted = Formatter(scores, fmt).frmt()
        return summ, formatted

    return summ, scores
